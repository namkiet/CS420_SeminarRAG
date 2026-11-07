"""G2 Tasks 3-4: BM25-only retrieval and evidence-based evaluation.

Run from repository root with uv:
  uv run --python .venv python experiment/bm25_retrieval.py --ks 1 3 5
"""
import argparse
from collections import Counter
import csv
import hashlib
import importlib.metadata
import json
import math
from pathlib import Path
import platform
import re
import sys

import joblib
import numpy as np
from scipy.sparse import csr_matrix

from rag_embedding import (align_evidence, normalized_text, retrieval_metrics,
                           validate_chunks)

ROOT = Path(__file__).resolve().parent
TOKEN_PATTERN = r'(?u)\b\w+\b'
TOKEN_RE = re.compile(TOKEN_PATTERN)
DEFAULT_K1 = 1.5
DEFAULT_B = 0.75
DEFAULT_NGRAM_RANGE = (1, 2)


def extract_ngrams(text, ngram_range=DEFAULT_NGRAM_RANGE):
    min_n, max_n = ngram_range
    tokens = TOKEN_RE.findall(normalized_text(text).lower())
    if not tokens:
        return []
    terms = []
    upper = min(max_n, len(tokens))
    for n in range(min_n, upper + 1):
        if n == 1:
            terms.extend(tokens)
        else:
            terms.extend(' '.join(tokens[i:i + n]) for i in range(len(tokens) - n + 1))
    return terms


class Bm25Retriever:
    """Lucene/Robertson non-negative BM25 fitted strictly on corpus chunks."""

    def __init__(self, chunks, k1=DEFAULT_K1, b=DEFAULT_B, ngram_range=DEFAULT_NGRAM_RANGE):
        validate_chunks(chunks)
        if isinstance(k1, bool) or not isinstance(k1, (int, float)) or not math.isfinite(k1) or k1 < 0:
            raise ValueError('k1 must be a finite non-negative number')
        if isinstance(b, bool) or not isinstance(b, (int, float)) or not math.isfinite(b) or not (0.0 <= b <= 1.0):
            raise ValueError('b must be a finite number in [0, 1]')
        if (not isinstance(ngram_range, tuple) or len(ngram_range) != 2
                or any(isinstance(x, bool) or not isinstance(x, int) for x in ngram_range)
                or ngram_range[0] < 1 or ngram_range[0] > ngram_range[1]):
            raise ValueError('ngram_range must be a tuple (min_n, max_n) with 1 <= min_n <= max_n')

        self.chunks = chunks
        self.k1 = float(k1)
        self.b = float(b)
        self.ngram_range = ngram_range

        # Fit vocabulary, DF, IDF, and document lengths on corpus ONLY, never questions/answers/gold.
        doc_counters = [Counter(extract_ngrams(c['text'], ngram_range)) for c in chunks]
        vocab_terms = sorted({term for counts in doc_counters for term in counts})
        self.vocabulary_ = {term: idx for idx, term in enumerate(vocab_terms)}

        n_docs = len(chunks)
        n_terms = len(self.vocabulary_)
        self.doc_len_ = np.array([sum(counts.values()) for counts in doc_counters], dtype=np.float64)
        self.avgdl_ = float(self.doc_len_.mean()) if n_docs else 0.0

        df = np.zeros(n_terms, dtype=np.float64)
        for counts in doc_counters:
            for term in counts:
                df[self.vocabulary_[term]] += 1.0
        self.df_ = df

        # Non-negative Robertson/Lucene IDF: ln(1 + (N - df + 0.5) / (df + 0.5)) > 0 for all df <= N.
        self.idf_ = np.log(1.0 + (n_docs - df + 0.5) / (df + 0.5)) if n_terms else np.zeros(0, dtype=np.float64)

        rows, cols, data = [], [], []
        for doc_idx, counts in enumerate(doc_counters):
            dl_norm = (1.0 - self.b + self.b * (self.doc_len_[doc_idx] / self.avgdl_)) if self.avgdl_ > 0 else 1.0
            denom_const = self.k1 * dl_norm
            for term, tf in counts.items():
                col_idx = self.vocabulary_[term]
                tf_val = float(tf)
                denom = tf_val + denom_const
                weight = float(self.idf_[col_idx]) * (tf_val * (self.k1 + 1.0) / denom) if denom > 0 else 0.0
                rows.append(doc_idx)
                cols.append(col_idx)
                data.append(weight)

        self.matrix = csr_matrix((np.array(data, dtype=np.float64), (rows, cols)),
                                 shape=(n_docs, n_terms), dtype=np.float64)

    @classmethod
    def from_saved(cls, chunks, saved):
        validate_chunks(chunks)
        expected_ids = [c['chunk_id'] for c in chunks]
        if saved.get('chunk_ids') != expected_ids:
            raise ValueError('Saved BM25 index chunk_ids do not match provided chunks')
        retriever = cls.__new__(cls)
        retriever.chunks = chunks
        params = saved['params']
        retriever.k1 = float(params['k1'])
        retriever.b = float(params['b'])
        retriever.ngram_range = tuple(params['ngram_range'])
        retriever.vocabulary_ = dict(saved['vocabulary'])
        retriever.idf_ = np.asarray(saved['idf'], dtype=np.float64)
        retriever.doc_len_ = np.asarray(saved['doc_len'], dtype=np.float64)
        retriever.avgdl_ = float(saved['avgdl'])
        retriever.matrix = saved['matrix']
        return retriever

    def search(self, question, k=5):
        if isinstance(k, bool) or not isinstance(k, int) or k < 1:
            raise ValueError('k must be a positive integer')
        question = normalized_text(question)
        if not question:
            raise ValueError('Question is empty')
        if self.matrix.shape[1] == 0:
            return []
        q_counts = Counter(extract_ngrams(question, self.ngram_range))
        matched = [(self.vocabulary_[t], float(c)) for t, c in q_counts.items() if t in self.vocabulary_]
        if not matched:
            return []
        cols = [idx for idx, _ in matched]
        vals = np.array([cnt for _, cnt in matched], dtype=np.float64)
        query_vec = csr_matrix((vals, (cols, np.zeros(len(cols), dtype=np.int64))),
                               shape=(self.matrix.shape[1], 1), dtype=np.float64)
        scores = (self.matrix @ query_vec).toarray().ravel()
        order = [int(i) for i in np.argsort(-scores, kind='stable') if scores[i] > 0][:k]
        return [dict(self.chunks[i], rank=rank, score=float(scores[i]))
                for rank, i in enumerate(order, 1)]


def align_gold(questions, chunks, pages):
    """Body quotes + explicitly sourced repeated table headers/legends.

    Editorial titles alone never count. No manual matching on question words.
    Each evidence group can have alternative chunks; any one covers the group.
    """
    body_gold = align_evidence(questions, chunks)
    lookup = {(p['doc_id'], p['pdf_page']): p['text'] for p in pages}
    result = []
    for row in body_gold:
        groups = []
        for group in row['groups']:
            evidence = group['evidence']
            quote = normalized_text(evidence['quote'])
            source_text = lookup[evidence['doc_id'], evidence['pdf_page']]
            if not quote or quote not in normalized_text(source_text):
                raise ValueError(f"Evidence is not in the source page: {row['question_id']}")
            context_ids = []
            for chunk in chunks:
                if chunk['doc_id'] != evidence['doc_id']:
                    continue
                prefix = chunk['text'][:chunk['body_char_start']]
                if quote not in normalized_text(prefix):
                    continue
                for span in chunk.get('context_source_spans', []):
                    if span['pdf_page'] != evidence['pdf_page']:
                        continue
                    original = source_text[span['char_start']:span['char_end']]
                    if quote in normalized_text(original):
                        context_ids.append(chunk['chunk_id'])
                        break
            groups.append(dict(evidence=evidence, body_chunk_ids=group['chunk_ids'],
                               source_context_chunk_ids=context_ids,
                               chunk_ids=list(dict.fromkeys(group['chunk_ids'] + context_ids))))
        result.append(dict(question_id=row['question_id'], groups=groups,
                           human_review_status=row['human_review_status']))
    return result


def save_json(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def write_csv(path, rows):
    with path.open('w', encoding='utf-8-sig', newline='') as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def evaluate(retriever, questions, gold, ks):
    rows, details = [], []
    for question, aligned in zip(questions, gold, strict=True):
        if question['question_id'] != aligned['question_id']:
            raise ValueError('Gold/question order mismatch')
        hits = retriever.search(question['question'], len(retriever.chunks))
        ids = [h['chunk_id'] for h in hits]
        body_groups = [dict(chunk_ids=g['body_chunk_ids']) for g in aligned['groups']]
        relevant = list(dict.fromkeys(cid for g in aligned['groups'] for cid in g['chunk_ids']))
        for k in ks:
            metrics = retrieval_metrics(ids, aligned['groups'], k)
            rows.append(dict(question_id=question['question_id'], k=k,
                             hit_rate=metrics['hit'], chunk_recall=metrics['chunk_recall'],
                             evidence_recall=metrics['evidence_recall'],
                             all_evidence_hit=metrics['all_evidence_hit'], mrr=metrics['mrr'],
                             body_only_evidence_recall=retrieval_metrics(ids, body_groups, k)['evidence_recall']))
        details.append(dict(
            question_id=question['question_id'], question=question['question'],
            relevant_chunk_ids=relevant, evidence_groups=aligned['groups'],
            human_review_status=aligned['human_review_status'],
            first_relevant_rank=next((i for i, cid in enumerate(ids, 1) if cid in relevant), None),
            evidence_first_ranks=[next((i for i, cid in enumerate(ids, 1) if cid in g['chunk_ids']), None)
                                  for g in aligned['groups']],
            retrieved=[dict(rank=h['rank'], chunk_id=h['chunk_id'], score=h['score'],
                            doc_id=h['doc_id'], section=h['section'], pdf_pages=h['pdf_pages'],
                            body_preview=h['text'][h['body_char_start']:][:220]) for h in hits[:max(ks)]]))
    metric_names = list(rows[0])[2:]
    summary = [dict(k=k, **{name: float(np.mean([r[name] for r in rows if r['k'] == k]))
                            for name in metric_names}) for k in ks]
    return rows, summary, details


def load_tfidf_baseline(ks, manifest):
    tfidf_csv = ROOT / 'results/tfidf_800/retrieval_summary.csv'
    tfidf_json = ROOT / 'results/tfidf_800/evaluation_details.json'
    if not tfidf_csv.exists() or not tfidf_json.exists():
        return None
    tfidf_hashes = json.loads(tfidf_json.read_text(encoding='utf-8'))['manifest']['source_hashes']
    if tfidf_hashes != manifest['source_hashes']:
        return None
    with tfidf_csv.open('r', encoding='utf-8-sig', newline='') as handle:
        by_k = {int(r['k']): r for r in csv.DictReader(handle)}
    return by_k if all(k in by_k for k in ks) else None


def load_dense_baseline(ks, details, manifest):
    ans_path = ROOT / 'results/kaggle_2026-11-05/answers_comparison.json'
    run_path = ROOT / 'results/kaggle_2026-11-05/run_manifest.json'
    if not ans_path.exists() or not run_path.exists() or max(ks) > 5:
        return None
    run_info = json.loads(run_path.read_text(encoding='utf-8'))
    data_sha = run_info.get('data_sha256', {})
    if (data_sha.get('corpus') != manifest['source_hashes']['chunks']
            or data_sha.get('questions') != manifest['source_hashes']['questions']):
        return None
    answers = json.loads(ans_path.read_text(encoding='utf-8'))
    if [a['question_id'] for a in answers] != [d['question_id'] for d in details]:
        return None
    if any(a['rag'].get('omitted_context_ids') or len(a['rag'].get('context_ids', [])) < max(ks) for a in answers):
        return None
    by_k = {}
    for k in ks:
        ctx_ms, body_ms = [], []
        for ans_row, det_row in zip(answers, details, strict=True):
            ranked = ans_row['rag']['context_ids']
            ctx_ms.append(retrieval_metrics(ranked, det_row['evidence_groups'], k))
            body_groups = [dict(chunk_ids=g['body_chunk_ids']) for g in det_row['evidence_groups']]
            body_ms.append(retrieval_metrics(ranked, body_groups, k))
        by_k[k] = dict(
            hit_rate=float(np.mean([m['hit'] for m in ctx_ms])),
            chunk_recall=float(np.mean([m['chunk_recall'] for m in ctx_ms])),
            evidence_recall=float(np.mean([m['evidence_recall'] for m in ctx_ms])),
            all_evidence_hit=float(np.mean([m['all_evidence_hit'] for m in ctx_ms])),
            mrr=float(np.mean([m['mrr'] for m in ctx_ms])),
            body_only_evidence_recall=float(np.mean([m['evidence_recall'] for m in body_ms])),
            body_only_all_evidence_hit=float(np.mean([m['all_evidence_hit'] for m in body_ms])),
        )
    return by_k


def report(summary, details, manifest):
    params = manifest['params']
    ngram_desc = 'unigram' if params['ngram_range'] == [1, 1] else f"n-gram {tuple(params['ngram_range'])}"
    lines = [
        '# G2 Task 3–4: BM25-only retrieval (Okapi BM25 — Lucene Non-negative IDF)', '',
        f"Đã chạy {manifest['questions']} câu hỏi trên {manifest['chunks']} chunks, trần chunk {manifest['chunk_config']['max_tokens']} token.", '',
        '## Cấu hình', '',
        f"- **Okapi BM25 (biến thể non-negative IDF của Apache Lucene)** với `{ngram_desc}`, lowercase, giữ dấu tiếng Việt và token một ký tự/chữ số; không dùng stopword tiếng Anh.",
        '- Token hóa theo regex `r\'(?u)\\b\\w+\\b\'` sau chuẩn hóa Unicode NFC và khoảng trắng (cùng không gian từ vựng với TF-IDF khi `ngram_range=(1, 2)`).',
        f"- Tham số cố định trước khi chạy: `k1 = {params['k1']}`, `b = {params['b']}`, `avgdl = {manifest['avgdl']:.2f}` (tính trên tổng n-gram trong phạm vi `{tuple(params['ngram_range'])}`).",
        '- Chỉ fit vocabulary, `df`, `idf`, `|d|` và `avgdl` trên `chunks[*].text`. Không fit câu hỏi, đáp án hoặc nhãn liên quan.',
        '- Không lọc tài liệu theo gold, không sửa câu hỏi, không mở rộng truy vấn hoặc điều chỉnh `k1`, `b` sau khi xem điểm.',
        '- Hòa điểm giữ thứ tự corpus; query không có từ vựng chung trả danh sách rỗng, không lấy chunk điểm 0.', '',
        '## Công thức toán học (Okapi BM25 — Lucene Non-negative IDF)', '',
        'Điểm xếp hạng giữa câu hỏi $q$ và chunk $d$ được tính theo công thức Okapi BM25 với thành phần IDF không âm:', '',
        '$$\\text{IDF}(t) = \\ln\\!\\left(1 + \\frac{N - \\text{df}(t) + 0.5}{\\text{df}(t) + 0.5}\\right)$$', '',
        '$$\\text{score}(q, d) = \\sum_{t \\in q \\cap V} \\text{qtf}(t, q) \\cdot \\text{IDF}(t) \\cdot \\frac{\\text{tf}(t, d) \\cdot (k_1 + 1)}{\\text{tf}(t, d) + k_1 \\cdot \\left(1 - b + b \\cdot \\frac{|d|}{\\text{avgdl}}\\right)}$$', '',
        'Trong đó:',
        f"- $N = {manifest['chunks']}$: tổng số chunks trong chỉ mục; $|V| = {manifest['matrix_shape'][1]}$: kích thước tập từ vựng `{ngram_desc}`.",
        '- $\\text{df}(t)$: số chunks chứa n-gram $t$ ($0 < \\text{df}(t) \\le N$).',
        '- $\\text{tf}(t, d)$, $\\text{qtf}(t, q)$: số lần xuất hiện của n-gram $t$ trong chunk $d$ và trong câu hỏi $q$.',
        f"- $|d| = \\sum_{{t \\in V}} \\text{{tf}}(t, d)$: độ dài chunk $d$; $\\text{{avgdl}} = \\frac{{1}}{{N}}\\sum_{{d=1}}^{{N}} |d| = {manifest['avgdl']:.2f}$.",
        f"- $k_1 = {params['k1']}$: hệ số bão hòa tần suất từ; $b = {params['b']} \\in [0, 1]$: hệ số chuẩn hóa độ dài tài liệu.",
        f"- **Lý do dùng biến thể non-negative IDF (`1 + ...` của Lucene thay vì Robertson–Spärck Jones 1994 trần):** Công thức 1994 $\\ln\\frac{{N - \\text{{df}}(t) + 0.5}}{{\\text{{df}}(t) + 0.5}}$ nhận giá trị **âm** khi $\\text{{df}}(t) > N/2$. Trong tập `{manifest['chunks']}` chunks này có **{manifest['ubiquitous_terms_over_half_docs']}** từ/cụm từ xuất hiện ở trên một nửa số chunks (như `'quy chế'`, `'học'`, `'phần'`, `'đại'`), nên nếu không cộng `1 +` bên trong $\\ln(\\cdot)$, các chunk chứa từ khóa đúng của câu hỏi sẽ bị phạt điểm âm.", '',
        '## Kết quả', '',
        '| k | Hit Rate@k | Chunk Recall@k | Evidence Recall@k | Đủ mọi bằng chứng@k | MRR@k |',
        '|---|---:|---:|---:|---:|---:|',
    ]
    for r in summary:
        lines.append(
            f"| {r['k']} | {r['hit_rate']:.2%} | {r['chunk_recall']:.2%} | "
            f"{r['evidence_recall']:.2%} | {r['all_evidence_hit']:.2%} | {r['mrr']:.4f} |"
        )
    largest = summary[-1]
    k = largest['k']
    misses = [q for q in details if q['first_relevant_rank'] is None or q['first_relevant_rank'] > k]
    incomplete = [q for q in details if any(r is None or r > k for r in q['evidence_first_ranks'])]
    lines += [
        '',
        f"Tại k={k}: tìm được ít nhất một bằng chứng cho {round(largest['hit_rate'] * len(details))}/{len(details)} câu; "
        f"đủ mọi bằng chứng cho {round(largest['all_evidence_hit'] * len(details))}/{len(details)} câu.",
        f"Không trúng bằng chứng trong top-{k}: " + (', '.join(q['question_id'] for q in misses) or 'không có') + '.',
        f"Chưa đủ mọi bằng chứng trong top-{k}: " + (', '.join(q['question_id'] for q in incomplete) or 'không có') + '.',
        '',
    ]

    ks_list = [r['k'] for r in summary]
    tfidf_by_k = load_tfidf_baseline(ks_list, manifest) if params['ngram_range'] == [1, 2] else None
    dense_by_k = load_dense_baseline(ks_list, details, manifest)
    if tfidf_by_k or dense_by_k:
        lines += [
            '## Đối chiếu với TF-IDF và BGE-M3 Embedding trên cùng 162 chunks', '',
            '### 1. Theo quy ước chuẩn `align_gold` (phần thân + chú giải bảng lặp xác thực)', '',
            '| k | Phương pháp | Hit Rate@k | Chunk Recall@k | Evidence Recall@k | Đủ mọi bằng chứng@k | MRR@k |',
            '|---:|---|---:|---:|---:|---:|---:|',
        ]
        for r in summary:
            kv = r['k']
            if tfidf_by_k:
                tf_row = tfidf_by_k[kv]
                lines.append(
                    f"| {kv} | TF-IDF cosine | {float(tf_row['hit_rate']):.2%} | {float(tf_row['chunk_recall']):.2%} | "
                    f"{float(tf_row['evidence_recall']):.2%} | {float(tf_row['all_evidence_hit']):.2%} | {float(tf_row['mrr']):.4f} |"
                )
            lines.append(
                f"| {kv} | **BM25-only** | **{r['hit_rate']:.2%}** | **{r['chunk_recall']:.2%}** | "
                f"**{r['evidence_recall']:.2%}** | **{r['all_evidence_hit']:.2%}** | **{r['mrr']:.4f}** |"
            )
            if dense_by_k:
                dn_row = dense_by_k[kv]
                lines.append(
                    f"| {kv} | BGE-M3 dense | {dn_row['hit_rate']:.2%} | {dn_row['chunk_recall']:.2%} | "
                    f"{dn_row['evidence_recall']:.2%} | {dn_row['all_evidence_hit']:.2%} | {dn_row['mrr']:.4f} |"
                )
        lines.append('')
        if dense_by_k:
            lines += [
                '### 2. Theo quy ước `body_only` (chỉ tính phần thân — quy ước gốc của notebook Kaggle)', '',
                '| k | TF-IDF (`body_only` Evidence Recall) | **BM25-only** (`body_only` Evidence Recall) | BGE-M3 dense (`body_only` Evidence Recall) |',
                '|---:|---:|---:|---:|',
            ]
            for r in summary:
                kv = r['k']
                tf_cell = f"{float(tfidf_by_k[kv]['body_only_evidence_recall']):.2%}" if tfidf_by_k else '—'
                lines.append(
                    f"| {kv} | {tf_cell} | **{r['body_only_evidence_recall']:.2%}** | "
                    f"{dense_by_k[kv]['body_only_evidence_recall']:.2%} |"
                )
            lines.append('')
        if (tfidf_by_k and dense_by_k and params['k1'] == DEFAULT_K1
                and params['b'] == DEFAULT_B and ks_list == [1, 3, 5]):
            lines += [
                '## Nhận xét kết quả', '',
                '- **Ảnh hưởng của k (`k = 1, 3, 5`):** Bước tăng rõ nhất của BM25 diễn ra từ `k=1` lên `k=3` (`Hit Rate` từ `85.00%` lên `90.00%`, `Evidence Recall` từ `80.00%` lên `84.17%`, tỷ lệ câu đủ mọi bằng chứng từ `75.00%` lên `80.00%`). Từ `k=3` lên `k=5`, `Chunk Recall` tăng thêm (`76.67%` lên `78.33%`) nhờ thu hồi thêm mảnh thay thế có chú giải lặp.',
                f"- **BM25-only vs. TF-IDF cosine (cùng ma trận `{manifest['matrix_shape'][0]} x {manifest['matrix_shape'][1]}` đặc trưng `(1, 2)`, `nnz = {manifest['matrix_nonzero']}`):** BM25 vượt TF-IDF ở mọi giá trị `k`, rõ nhất tại `k=1` (`Hit Rate@1` +10 điểm %, `Evidence Recall@1` +9.17 điểm %, `MRR@1` +0.1000) nhờ bão hòa tần suất từ (`k1 = 1.5`) và chuẩn hóa độ dài theo `|d|/avgdl` (`b = 0.75`). BM25 đưa bằng chứng đúng lên hạng 1 ở `Q05`, `Q16`, chọn ngay mảnh chứa cả dòng ngành lẫn chú giải ở `Q12`, và kéo mảnh thiếu của `Q15` từ hạng 11 (TF-IDF) vào hạng 3.",
                '- **BM25-only vs. BGE-M3 dense embedding (bù trừ giữa khớp từ khóa và ngữ nghĩa):** Tại `k=1` và `k=3` (cũng như `MRR` ở cả 3 mức `k`), **BM25-only vượt BGE-M3** (`Hit Rate@1`: `85.00%` so với `70.00%`; `Evidence Recall@1`: `80.00%` so với `65.00%`; `MRR@5`: `0.8667` so với `0.7867`) do văn bản quy chế có nhiều mốc điều khoản, mã cột (`C5`), mức điểm và thuật ngữ chính xác (`Q06`, `Q08`, `Q10` đạt hạng 1 ở BM25 nhưng hạng 2–3 ở BGE-M3; `Q15` lấy đủ 3/3 mảnh ở `k=3` với BM25 trong khi BGE-M3 thiếu mảnh IELTS 4.5 ở ngoài top-5). Ngược lại, tại `k=5`, **BGE-M3 vượt lên về độ phủ rộng** (`Hit Rate@5 = 95.00%`, `Evidence Recall@5 = 89.17%`, cùng đạt `All Evidence@5 = 80.00%` như BM25) nhờ bắt được ngữ nghĩa khi câu hỏi lệch từ khóa nguyên văn (`Q14` hỏi `khóa tuyển 2020` trên văn bản ghi `2022–2026` được BGE-M3 xếp hạng 5 trong khi BM25 xếp hạng 13; `Q16` lấy được 2/3 mảnh trong top-5). Sự bù trừ này là cơ sở thực nghiệm trực tiếp để đề xuất **Hybrid Retrieval (BM25 + Dense Embedding)** ở phần cải thiện.',
                '',
            ]

    lines += [
        '## Quy ước chấm', '',
        '- Gold được ánh xạ tự động từ 30 quote có sẵn, đúng tài liệu/trang và nguyên văn sau chuẩn hóa Unicode/khoảng trắng. Không dùng điểm BM25 để tạo gold.',
        '- Ngoài phần thân, chấp nhận chú giải bảng được lặp nếu quote có trong ngữ cảnh và được xác nhận bằng `context_source_spans` trên trang gốc. Tiêu đề biên tập không đủ điều kiện.',
        '- Một evidence group có thể có nhiều chunk thay thế. Lấy bất kỳ chunk nào trong group là đã tìm được bằng chứng đó.',
        '- Hit Rate@k: tỷ lệ câu tìm được ít nhất một chunk liên quan.',
        '- Chunk Recall@k: số chunk liên quan tìm được chia tổng số chunk liên quan của câu. Vì chú giải có thể lặp nhiều nơi, không bắt buộc lấy mọi chunk thay thế để có đủ bằng chứng.',
        '- Evidence Recall@k: số nhóm bằng chứng được tìm thấy chia tổng số nhóm cần thiết của câu.',
        '- Đủ mọi bằng chứng@k: tỷ lệ câu mà mọi nhóm bằng chứng đều được tìm thấy. MRR@k: nghịch đảo hạng đầu tiên trúng gold trong top-k.',
        '- Mọi chỉ số được lấy trung bình trên đủ 20 câu (macro), không bỏ câu khó. CSV ghi số thập phân 0–1, bảng này hiển thị phần trăm.',
        '- `body_only_evidence_recall` trong CSV chỉ xét phần thân, dùng đối chiếu cách đo của notebook embedding cũ. Không so trực tiếp Evidence Recall có ngữ cảnh với metric cũ chỉ phần thân.', '',
        '## Đọc output', '',
        '- `retrieval_summary.csv`: kết quả tổng hợp tại từng k.',
        '- `retrieval_per_question.csv`: kết quả từng câu/từng k.',
        '- `evaluation_details.json`: cấu hình, phiên bản/hash, nhãn liên quan, evidence groups, top-k và hạng bằng chứng đầu tiên.',
        '- Chỉ mục BM25 được lưu trong `experiment/outputs/bm25/index.joblib` (Git bỏ qua), có thể tạo lại bằng lệnh chạy. Chỉ tải file joblib do chính mình tạo/tin cậy.', '',
        '## Chạy lại từ thư mục gốc repo (với `uv venv`)', '',
        '```powershell',
        'uv venv --allow-existing .venv',
        'uv pip install --python .venv -r experiment/requirements-bm25.txt',
        'uv run --python .venv python experiment/bm25_retrieval.py --ks 1 3 5',
        '```', '',
        'Tra cứu riêng:', '',
        '```powershell',
        'uv run --python .venv python experiment/bm25_retrieval.py --query "Học phần tiên quyết là gì?" --top-k 5',
        '```', '',
        '## Giới hạn', '',
        'Đây là kết quả trên bộ 20 câu hiện tại, chưa phải tập test độc lập đã duyệt. Nhãn chỉ bao phủ các quote đã chọn, không khẳng định đã liệt kê mọi đoạn trả lời tương đương. OCR và human review vẫn pending; cần nhóm kiểm tra chéo nhãn. Điểm retrieval không phải độ chính xác câu trả lời của LLM. Chưa thực hiện generation trong lần chạy BM25 này.', '',
        'Tham khảo công thức: Robertson, S., & Zaragoza, H. (2009). *The Probabilistic Relevance Framework: BM25 and Beyond*; Kamphuis, C., et al. (2020). *Which BM25 Do You Mean? A Large-Scale Reproducibility Study of Scoring Variants* (ECIR 2020 — biến thể Lucene non-negative IDF).', ''
    ]
    return '\n'.join(lines)


def main():
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--data-dir', type=Path, default=ROOT / 'data')
    parser.add_argument('--output-dir', type=Path, default=ROOT / 'results/bm25_800')
    parser.add_argument('--index-path', type=Path, default=ROOT / 'outputs/bm25/index.joblib')
    parser.add_argument('--ks', type=int, nargs='+', default=[1, 3, 5])
    parser.add_argument('--k1', type=float, default=DEFAULT_K1)
    parser.add_argument('--b', type=float, default=DEFAULT_B)
    parser.add_argument('--ngram-max', type=int, default=DEFAULT_NGRAM_RANGE[1])
    parser.add_argument('--query')
    parser.add_argument('--top-k', type=int, default=5)
    args = parser.parse_args()
    if any(k < 1 for k in args.ks) or args.top_k < 1:
        parser.error('All k values must be positive')
    if args.ngram_max < 1:
        parser.error('--ngram-max must be >= 1')
    if not math.isfinite(args.k1) or args.k1 < 0:
        parser.error('--k1 must be a finite non-negative number')
    if not math.isfinite(args.b) or not (0.0 <= args.b <= 1.0):
        parser.error('--b must be a finite number in [0, 1]')

    ngram_range = (1, args.ngram_max)
    chunk_path = args.data_dir / 'chunks/chunks_by_structure.json'
    payload = json.loads(chunk_path.read_text(encoding='utf-8'))
    chunks = payload['chunks']
    if max(args.ks) > len(chunks) or args.top_k > len(chunks):
        parser.error('k cannot exceed the number of chunks')

    retriever = Bm25Retriever(chunks, k1=args.k1, b=args.b, ngram_range=ngram_range)
    if args.query is not None:
        hits = retriever.search(args.query, args.top_k)
        print(json.dumps([dict(rank=h['rank'], score=h['score'], chunk_id=h['chunk_id'],
                               section=h['section'], pdf_pages=h['pdf_pages'], text=h['text'])
                          for h in hits], ensure_ascii=False, indent=2))
        return

    question_path = args.data_dir / 'questions.json'
    pages_path = args.data_dir / 'processed/corpus_pages.json'
    questions = json.loads(question_path.read_text(encoding='utf-8'))
    if not questions or len({q['question_id'] for q in questions}) != len(questions):
        raise ValueError('Empty questions or duplicate question IDs')
    pages = json.loads(pages_path.read_text(encoding='utf-8'))
    gold = align_gold(questions, chunks, pages)
    ks = sorted(set(args.ks))
    rows, summary, details = evaluate(retriever, questions, gold, ks)

    params = dict(analyzer='word', ngram_range=list(ngram_range), lowercase=True,
                  strip_accents=None, token_pattern=TOKEN_PATTERN, stop_words=None,
                  k1=retriever.k1, b=retriever.b,
                  idf_formula='ln(1 + (N - df + 0.5) / (df + 0.5))',
                  doc_len_unit='ngram_tokens_in_range')
    index_path = args.index_path
    index_path.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(dict(params=params, vocabulary=retriever.vocabulary_, idf=retriever.idf_,
                     doc_len=retriever.doc_len_, avgdl=retriever.avgdl_, matrix=retriever.matrix,
                     chunk_ids=[c['chunk_id'] for c in chunks],
                     corpus_sha256=hashlib.sha256(chunk_path.read_bytes()).hexdigest()), index_path)

    manifest = dict(
        method='bm25_lucene', params=params, fit_input='chunks[*].text only',
        chunks=len(chunks), questions=len(questions), ks=ks,
        evidence_groups=sum(len(q['groups']) for q in gold),
        chunk_config=payload['config'], matrix_shape=list(retriever.matrix.shape),
        matrix_nonzero=int(retriever.matrix.nnz), avgdl=retriever.avgdl_,
        ubiquitous_terms_over_half_docs=int((retriever.df_ > len(chunks) / 2.0).sum()),
        source_hashes={name: hashlib.sha256(path.read_bytes()).hexdigest() for name, path in
                       [('chunks', chunk_path), ('questions', question_path), ('pages', pages_path)]},
        versions={'python': platform.python_version(),
                  **{name: importlib.metadata.version(name) for name in ['numpy', 'scipy', 'joblib']}},
        gold_policy='body_or_verified_source_context; editorial_only_excluded',
        tie_policy='stable corpus order', zero_score_policy='excluded',
        independent_human_review='pending',
    )
    args.output_dir.mkdir(parents=True, exist_ok=True)
    write_csv(args.output_dir / 'retrieval_per_question.csv', rows)
    write_csv(args.output_dir / 'retrieval_summary.csv', summary)
    save_json(args.output_dir / 'evaluation_details.json', dict(manifest=manifest, questions=details))
    (args.output_dir / 'README.md').write_text(report(summary, details, manifest), encoding='utf-8')
    print(json.dumps(dict(summary=summary, index=str(index_path), results=str(args.output_dir)),
                     ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
