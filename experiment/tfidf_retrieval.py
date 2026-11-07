"""G2 Tasks 3-4: TF-IDF cosine retrieval and evidence-based evaluation.

Run from repository root:
  .venv/Scripts/python.exe experiment/tfidf_retrieval.py --ks 1 3 5
"""
import argparse
import csv
import hashlib
import importlib.metadata
import json
from pathlib import Path
import platform

import joblib
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer

from rag_embedding import (align_evidence, normalized_text, retrieval_metrics,
                           validate_chunks)

ROOT = Path(__file__).resolve().parent
PARAMS = dict(analyzer='word', ngram_range=(1, 2), lowercase=True,
              strip_accents=None, token_pattern=r'(?u)\b\w+\b', stop_words=None,
              min_df=1, max_df=1.0, norm='l2', smooth_idf=True, sublinear_tf=True)


class TfidfRetriever:
    def __init__(self, chunks):
        validate_chunks(chunks)
        self.chunks = chunks
        self.vectorizer = TfidfVectorizer(**PARAMS)
        # Fit vocabulary and IDF on corpus ONLY, never questions/answers/gold.
        self.matrix = self.vectorizer.fit_transform(normalized_text(c['text']) for c in chunks)

    def search(self, question, k=5):
        if not isinstance(k, int) or k < 1:
            raise ValueError('k must be a positive integer')
        question = normalized_text(question)
        if not question:
            raise ValueError('Question is empty')
        query = self.vectorizer.transform([question])
        if query.nnz == 0:
            return []
        # Dot product of L2-normalized TF-IDF rows equals cosine similarity.
        scores = (self.matrix @ query.T).toarray().ravel()
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
                               chunk_ids=list(dict.fromkeys(group['chunk_ids']+context_ids))))
        result.append(dict(question_id=row['question_id'], groups=groups,
                           human_review_status=row['human_review_status']))
    return result


def save_json(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')


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
    summary = [dict(k=k, **{name:float(np.mean([r[name] for r in rows if r['k']==k]))
                           for name in metric_names}) for k in ks]
    return rows, summary, details


def report(summary, details, manifest):
    lines = [
        '# G2 Task 3–4: TF-IDF retrieval', '',
        f"Đã chạy {manifest['questions']} câu hỏi trên {manifest['chunks']} chunks, trần chunk 800 token.", '',
        '## Cấu hình', '',
        '- TF-IDF unigram + bigram, lowercase, giữ dấu tiếng Việt và token một ký tự/chữ số; không dùng stopword tiếng Anh.',
        '- Token hóa theo regex/khoảng trắng, không phải bộ tách từ tiếng Việt. Chuẩn hóa Unicode NFC và khoảng trắng.',
        '- `tf = 1 + ln(count)`, `idf = ln((1 + N)/(1 + df)) + 1`; chuẩn hóa L2 rồi tích vô hướng để tính cosine.',
        '- Chỉ fit vocabulary/IDF trên `chunks[*].text`. Không fit câu hỏi, đáp án hoặc nhãn liên quan.',
        '- Không lọc tài liệu theo gold, không sửa câu hỏi, không mở rộng truy vấn hoặc điều chỉnh tham số sau khi xem điểm.',
        '- Hòa điểm giữ thứ tự corpus; query không có từ vựng chung trả danh sách rỗng, không lấy chunk điểm 0.', '',
        '## Kết quả', '',
        '| k | Hit Rate@k | Chunk Recall@k | Evidence Recall@k | Đủ mọi bằng chứng@k | MRR@k |',
        '|---|---:|---:|---:|---:|---:|']
    for r in summary:
        lines.append(f"| {r['k']} | {r['hit_rate']:.2%} | {r['chunk_recall']:.2%} | {r['evidence_recall']:.2%} | {r['all_evidence_hit']:.2%} | {r['mrr']:.4f} |")
    largest = summary[-1]
    k = largest['k']
    misses = [q for q in details if q['first_relevant_rank'] is None or q['first_relevant_rank'] > k]
    incomplete = [q for q in details if any(r is None or r > k for r in q['evidence_first_ranks'])]
    lines += ['', f"Tại k={k}: tìm được ít nhất một bằng chứng cho {round(largest['hit_rate']*len(details))}/{len(details)} câu; "
              f"đủ mọi bằng chứng cho {round(largest['all_evidence_hit']*len(details))}/{len(details)} câu.",
              f"Không trúng bằng chứng trong top-{k}: "+(', '.join(q['question_id'] for q in misses) or 'không có')+'.',
              f"Chưa đủ mọi bằng chứng trong top-{k}: "+(', '.join(q['question_id'] for q in incomplete) or 'không có')+'.', '',
              '## Quy ước chấm', '',
              '- Gold được ánh xạ tự động từ 30 quote có sẵn, đúng tài liệu/trang và nguyên văn sau chuẩn hóa Unicode/khoảng trắng. Không dùng điểm TF-IDF để tạo gold.',
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
              '- Chỉ mục TF-IDF được lưu trong `experiment/outputs/tfidf/index.joblib` (Git bỏ qua), có thể tạo lại bằng lệnh chạy. Chỉ tải file joblib do chính mình tạo/tin cậy.', '',
              '## Chạy lại từ thư mục gốc repo', '', '```powershell',
              '.\\.venv\\Scripts\\python.exe -m pip install -r experiment/requirements-tfidf.txt',
              '.\\.venv\\Scripts\\python.exe experiment/tfidf_retrieval.py --ks 1 3 5',
              '```', '', 'Tra cứu riêng:', '', '```powershell',
              '.\\.venv\\Scripts\\python.exe experiment/tfidf_retrieval.py --query "Học phần tiên quyết là gì?" --top-k 5',
              '```', '', '## Giới hạn', '',
              'Đây là kết quả trên bộ 20 câu hiện tại, chưa phải tập test độc lập đã duyệt. Nhãn chỉ bao phủ các quote đã chọn, không khẳng định đã liệt kê mọi đoạn trả lời tương đương. OCR và human review vẫn pending; cần nhóm kiểm tra chéo nhãn. Điểm retrieval không phải độ chính xác câu trả lời của LLM. Chưa thực hiện generation trong lần chạy TF-IDF này.', '',
              '[Tài liệu TfidfVectorizer của scikit-learn](https://scikit-learn.org/1.7/modules/generated/sklearn.feature_extraction.text.TfidfVectorizer.html)', '']
    return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--data-dir', type=Path, default=ROOT/'data')
    parser.add_argument('--output-dir', type=Path, default=ROOT/'results/tfidf_800')
    parser.add_argument('--ks', type=int, nargs='+', default=[1, 3, 5])
    parser.add_argument('--query')
    parser.add_argument('--top-k', type=int, default=5)
    args = parser.parse_args()
    if any(k < 1 for k in args.ks) or args.top_k < 1:
        parser.error('All k values must be positive')
    chunk_path = args.data_dir/'chunks/chunks_by_structure.json'
    payload = json.loads(chunk_path.read_text(encoding='utf-8'))
    chunks = payload['chunks']
    if max(args.ks) > len(chunks) or args.top_k > len(chunks):
        parser.error('k cannot exceed the number of chunks')
    retriever = TfidfRetriever(chunks)
    if args.query is not None:
        hits = retriever.search(args.query, args.top_k)
        print(json.dumps([dict(rank=h['rank'], score=h['score'], chunk_id=h['chunk_id'],
                               section=h['section'], pdf_pages=h['pdf_pages'], text=h['text'])
                          for h in hits], ensure_ascii=False, indent=2))
        return
    question_path = args.data_dir/'questions.json'
    pages_path = args.data_dir/'processed/corpus_pages.json'
    questions = json.loads(question_path.read_text(encoding='utf-8'))
    if not questions or len({q['question_id'] for q in questions}) != len(questions):
        raise ValueError('Empty questions or duplicate question IDs')
    pages = json.loads(pages_path.read_text(encoding='utf-8'))
    gold = align_gold(questions, chunks, pages)
    ks = sorted(set(args.ks))
    rows, summary, details = evaluate(retriever, questions, gold, ks)
    index_path = ROOT/'outputs/tfidf/index.joblib'
    index_path.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(dict(vectorizer=retriever.vectorizer, matrix=retriever.matrix,
                     chunk_ids=[c['chunk_id'] for c in chunks],
                     corpus_sha256=hashlib.sha256(chunk_path.read_bytes()).hexdigest()), index_path)
    manifest = dict(method='tfidf_cosine', params=PARAMS, fit_input='chunks[*].text only',
                    chunks=len(chunks), questions=len(questions), ks=ks,
                    evidence_groups=sum(len(q['groups']) for q in gold),
                    chunk_config=payload['config'], matrix_shape=list(retriever.matrix.shape),
                    matrix_nonzero=int(retriever.matrix.nnz),
                    source_hashes={name:hashlib.sha256(path.read_bytes()).hexdigest() for name,path in
                                   [('chunks',chunk_path),('questions',question_path),('pages',pages_path)]},
                    versions={'python':platform.python_version(), **{name:importlib.metadata.version(name)
                              for name in ['scikit-learn','numpy','scipy','joblib','threadpoolctl']}},
                    gold_policy='body_or_verified_source_context; editorial_only_excluded',
                    tie_policy='stable corpus order', zero_score_policy='excluded',
                    independent_human_review='pending')
    args.output_dir.mkdir(parents=True, exist_ok=True)
    write_csv(args.output_dir/'retrieval_per_question.csv', rows)
    write_csv(args.output_dir/'retrieval_summary.csv', summary)
    save_json(args.output_dir/'evaluation_details.json', dict(manifest=manifest, questions=details))
    (args.output_dir/'README.md').write_text(report(summary, details, manifest), encoding='utf-8')
    print(json.dumps(dict(summary=summary, index=str(index_path), results=str(args.output_dir)),
                     ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
