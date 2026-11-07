import copy
import json
import math
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

import joblib

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from bm25_retrieval import Bm25Retriever, align_gold, evaluate
from rag_embedding import retrieval_metrics


def chunk(cid, text):
    return dict(chunk_id=cid, text=text, pdf_pages=[1], doc_id='X',
                body_char_start=0, context_source_spans=[])


class Bm25Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.chunks = json.loads((ROOT / 'data/chunks/chunks_by_structure.json').read_text(encoding='utf-8'))['chunks']
        cls.questions = json.loads((ROOT / 'data/questions.json').read_text(encoding='utf-8'))
        cls.pages = json.loads((ROOT / 'data/processed/corpus_pages.json').read_text(encoding='utf-8'))

    def test_bm25_score_matches_hand_calculation(self):
        # Doc a: unigrams [alpha, alpha, beta] (3) + bigrams [alpha alpha, alpha beta] (2) -> dl_a = 5
        # Doc b: unigrams [beta, gamma] (2) + bigrams [beta gamma] (1) -> dl_b = 3
        # avgdl = (5 + 3) / 2 = 4.0
        k1, b = 1.5, 0.75
        retriever = Bm25Retriever([chunk('a', 'alpha alpha beta'), chunk('b', 'beta gamma')],
                                  k1=k1, b=b, ngram_range=(1, 2))
        self.assertAlmostEqual(retriever.avgdl_, 4.0)

        # Query "alpha beta" -> unigrams: alpha(1), beta(1); bigram: "alpha beta"(1)
        idf_rare = math.log(1.0 + (2.0 - 1.0 + 0.5) / (1.0 + 0.5))   # df = 1 -> ln(2)
        idf_common = math.log(1.0 + (2.0 - 2.0 + 0.5) / (2.0 + 0.5)) # df = 2 -> ln(1.2)
        norm_a = 1.0 - b + b * (5.0 / 4.0)
        norm_b = 1.0 - b + b * (3.0 / 4.0)

        w_a_alpha = idf_rare * (2.0 * (k1 + 1.0)) / (2.0 + k1 * norm_a)
        w_a_beta = idf_common * (1.0 * (k1 + 1.0)) / (1.0 + k1 * norm_a)
        w_a_bigram = idf_rare * (1.0 * (k1 + 1.0)) / (1.0 + k1 * norm_a)
        expected_a = w_a_alpha + w_a_beta + w_a_bigram
        expected_b = idf_common * (1.0 * (k1 + 1.0)) / (1.0 + k1 * norm_b)

        hits = retriever.search('alpha beta', 2)
        self.assertEqual([h['chunk_id'] for h in hits], ['a', 'b'])
        self.assertAlmostEqual(hits[0]['score'], expected_a)
        self.assertAlmostEqual(hits[1]['score'], expected_b)

        # Duplicate query token multiplies by qtf
        hits_dup = retriever.search('gamma gamma', 2)
        expected_gamma = 2.0 * idf_rare * (1.0 * (k1 + 1.0)) / (1.0 + k1 * norm_b)
        self.assertEqual([h['chunk_id'] for h in hits_dup], ['b'])
        self.assertAlmostEqual(hits_dup[0]['score'], expected_gamma)

    def test_idf_is_strictly_positive_and_length_normalized(self):
        # Term "học" appears in 100% of docs (df = 2 = N); IDF must still be > 0,
        # and the shorter chunk must outrank the padded chunk when tf is equal.
        short = chunk('short', 'học phí')
        long_doc = chunk('long', 'học tập rèn luyện ngoại ngữ quy chế tín chỉ')
        retriever = Bm25Retriever([long_doc, short], k1=1.5, b=0.75, ngram_range=(1, 2))
        self.assertTrue((retriever.idf_ > 0).all())
        hits = retriever.search('học', 2)
        self.assertEqual([h['chunk_id'] for h in hits], ['short', 'long'])
        self.assertGreater(hits[0]['score'], hits[1]['score'])
        self.assertGreater(hits[1]['score'], 0.0)

    def test_ties_are_stable_and_invalid_inputs_rejected(self):
        retriever = Bm25Retriever([chunk('first', 'alpha beta'), chunk('second', 'alpha beta')])
        hits = retriever.search('alpha beta', 2)
        self.assertEqual([h['chunk_id'] for h in hits], ['first', 'second'])
        self.assertAlmostEqual(hits[0]['score'], hits[1]['score'])
        self.assertEqual(retriever.search('zzzzunseenvocabulary'), [])
        for bad_q in ['', '   ', '!!!']:
            if not bad_q.strip():
                with self.assertRaises(ValueError):
                    retriever.search(bad_q)
            else:
                self.assertEqual(retriever.search(bad_q), [])
        for bad_k in [0, -1, True, 1.5]:
            with self.assertRaises(ValueError):
                retriever.search('alpha', bad_k)
        with self.assertRaises(ValueError):
            Bm25Retriever([chunk('a', 'alpha')], k1=-0.1)
        with self.assertRaises(ValueError):
            Bm25Retriever([chunk('a', 'alpha')], b=1.5)
        with self.assertRaises(ValueError):
            Bm25Retriever([chunk('a', 'alpha')], ngram_range=(2, 1))

    def test_query_never_changes_vocabulary_idf_or_lengths(self):
        retriever = Bm25Retriever([chunk('a', 'học phí 1 tín chỉ')])
        vocabulary = dict(retriever.vocabulary_)
        idf = retriever.idf_.copy()
        doc_len = retriever.doc_len_.copy()
        avgdl = retriever.avgdl_
        retriever.search('reference_answer_secret học phí')
        self.assertEqual(vocabulary, retriever.vocabulary_)
        self.assertTrue((idf == retriever.idf_).all())
        self.assertTrue((doc_len == retriever.doc_len_).all())
        self.assertEqual(avgdl, retriever.avgdl_)
        self.assertIn('1', vocabulary)
        self.assertIn('phí', vocabulary)
        self.assertIn('học phí', vocabulary)
        self.assertNotIn('reference_answer_secret', vocabulary)

    def test_source_context_counts_but_editorial_context_does_not(self):
        body = chunk('body', 'Giá 100 đồng.')
        prefix = 'Giá 100 đồng.\n'
        repeated = chunk('repeated', prefix + 'Nội dung khác')
        repeated['body_char_start'] = len(prefix)
        repeated['context_source_spans'] = [dict(pdf_page=1, char_start=0, char_end=13)]
        fake = copy.deepcopy(repeated)
        fake['chunk_id'] = 'editorial'
        fake['context_source_spans'] = []
        questions = [dict(question_id='Q', evidence=[dict(doc_id='X', pdf_page=1, quote='Giá 100 đồng.')])]
        pages = [dict(doc_id='X', pdf_page=1, text='Giá 100 đồng.')]
        gold = align_gold(questions, [body, repeated, fake], pages)
        self.assertEqual(gold[0]['groups'][0]['body_chunk_ids'], ['body'])
        self.assertEqual(gold[0]['groups'][0]['chunk_ids'], ['body', 'repeated'])
        pages[0]['text'] = 'Không có bằng chứng này'
        with self.assertRaisesRegex(ValueError, 'source page'):
            align_gold(questions, [body], pages)

    def test_vocabulary_and_gold_match_tfidf_baseline_identically(self):
        bm25 = Bm25Retriever(self.chunks)
        tfidf_details_path = ROOT / 'results/tfidf_800/evaluation_details.json'
        if tfidf_details_path.exists():
            tfidf_eval = json.loads(tfidf_details_path.read_text(encoding='utf-8'))
            self.assertEqual(list(bm25.matrix.shape), tfidf_eval['manifest']['matrix_shape'])
            self.assertEqual(int(bm25.matrix.nnz), tfidf_eval['manifest']['matrix_nonzero'])
            gold = align_gold(self.questions, self.chunks, self.pages)
            for aligned, expected_q in zip(gold, tfidf_eval['questions'], strict=True):
                self.assertEqual(aligned['question_id'], expected_q['question_id'])
                self.assertEqual(aligned['groups'], expected_q['evidence_groups'])

    def test_full_corpus_alignment_and_macro_metrics(self):
        gold = align_gold(self.questions, self.chunks, self.pages)
        self.assertEqual(len(gold), 20)
        self.assertEqual(sum(len(q['groups']) for q in gold), 30)
        retriever = Bm25Retriever(self.chunks)
        rows, summary, details = evaluate(retriever, self.questions, gold, [1, 3, 5])
        self.assertEqual(len(rows), 60)
        self.assertEqual(len(details), 20)
        for metric in summary:
            selected = [r for r in rows if r['k'] == metric['k']]
            self.assertEqual(len(selected), 20)
            for name in list(metric)[1:]:
                self.assertAlmostEqual(metric[name], sum(r[name] for r in selected) / 20)
        for q in self.questions:
            selected = [r for r in rows if r['question_id'] == q['question_id']]
            for name in ['hit_rate', 'chunk_recall', 'evidence_recall', 'all_evidence_hit']:
                self.assertEqual([r[name] for r in selected], sorted(r[name] for r in selected))

    def test_saved_index_reconstructs_same_rankings(self):
        retriever = Bm25Retriever(self.chunks)
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'index.joblib'
            joblib.dump(dict(
                params=dict(k1=retriever.k1, b=retriever.b, ngram_range=list(retriever.ngram_range)),
                vocabulary=retriever.vocabulary_, idf=retriever.idf_,
                doc_len=retriever.doc_len_, avgdl=retriever.avgdl_, matrix=retriever.matrix,
                chunk_ids=[c['chunk_id'] for c in self.chunks],
            ), path)
            loaded = joblib.load(path)
            restored = Bm25Retriever.from_saved(self.chunks, loaded)
            question = self.questions[0]['question']
            self.assertEqual(retriever.search(question), restored.search(question))
            with self.assertRaises(ValueError):
                Bm25Retriever.from_saved(self.chunks[:-1], loaded)

    def test_cli_runs_without_sklearn_and_writes_all_outputs(self):
        with tempfile.TemporaryDirectory() as directory:
            out_dir = Path(directory) / 'results'
            idx_path = Path(directory) / 'index.joblib'
            code = (
                "import sys; sys.modules['sklearn'] = None; "
                f"sys.argv = ['bm25_retrieval.py', '--output-dir', {str(out_dir)!r}, "
                f"'--index-path', {str(idx_path)!r}, '--ks', '1', '3', '5']; "
                f"sys.path.insert(0, {str(ROOT)!r}); "
                "import bm25_retrieval; bm25_retrieval.main()"
            )
            proc = subprocess.run([sys.executable, '-B', '-c', code],
                                  capture_output=True, text=True, encoding='utf-8', check=True)
            payload = json.loads(proc.stdout)
            self.assertEqual([r['k'] for r in payload['summary']], [1, 3, 5])
            for filename in ['retrieval_summary.csv', 'retrieval_per_question.csv',
                             'evaluation_details.json', 'README.md']:
                self.assertTrue((out_dir / filename).is_file(), filename)
            self.assertTrue(idx_path.is_file())

            q_proc = subprocess.run(
                [sys.executable, '-B', str(ROOT / 'bm25_retrieval.py'),
                 '--query', self.questions[0]['question'], '--top-k', '3'],
                capture_output=True, text=True, encoding='utf-8', check=True,
            )
            hits = json.loads(q_proc.stdout)
            self.assertEqual(len(hits), 3)
            gold_q1 = align_gold(self.questions[:1], self.chunks, self.pages)[0]
            self.assertIn(hits[0]['chunk_id'], gold_q1['groups'][0]['chunk_ids'])


if __name__ == '__main__':
    unittest.main()
