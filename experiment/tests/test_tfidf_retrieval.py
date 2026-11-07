import copy
import json
import math
from pathlib import Path
import sys
import unittest

import joblib

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from tfidf_retrieval import TfidfRetriever, align_gold, evaluate
from rag_embedding import retrieval_metrics


def chunk(cid, text):
    return dict(chunk_id=cid, text=text, pdf_pages=[1], doc_id='X',
                body_char_start=0, context_source_spans=[])


class TfidfTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.chunks = json.loads((ROOT/'data/chunks/chunks_by_structure.json').read_text(encoding='utf-8'))['chunks']
        cls.questions = json.loads((ROOT/'data/questions.json').read_text(encoding='utf-8'))
        cls.pages = json.loads((ROOT/'data/processed/corpus_pages.json').read_text(encoding='utf-8'))

    def test_tfidf_cosine_matches_hand_calculation(self):
        retriever = TfidfRetriever([chunk('a', 'alpha alpha beta'), chunk('b', 'beta gamma')])
        # Include bigrams in the independent calculation for document a.
        idf_rare = 1+math.log(3/2)
        weights = [(1+math.log(2))*idf_rare, 1, idf_rare, idf_rare]
        expected = weights[0]/math.sqrt(sum(w*w for w in weights))
        hits = retriever.search('alpha', 2)
        self.assertEqual([h['chunk_id'] for h in hits], ['a'])
        self.assertAlmostEqual(hits[0]['score'], expected)

    def test_ties_are_stable_and_unseen_query_has_no_results(self):
        retriever = TfidfRetriever([chunk('first', 'alpha beta'), chunk('second', 'alpha beta')])
        self.assertEqual([h['chunk_id'] for h in retriever.search('alpha beta', 2)], ['first', 'second'])
        self.assertAlmostEqual(retriever.search('alpha beta')[0]['score'], 1)
        self.assertEqual(retriever.search('zzzzunseenvocabulary'), [])
        with self.assertRaises(ValueError):
            retriever.search('   ')
        with self.assertRaises(ValueError):
            retriever.search('alpha', 0)

    def test_query_never_changes_vocabulary_or_idf(self):
        retriever = TfidfRetriever([chunk('a', 'học phí 1 tín chỉ')])
        vocabulary = dict(retriever.vectorizer.vocabulary_)
        idf = retriever.vectorizer.idf_.copy()
        retriever.search('reference_answer_secret học phí')
        self.assertEqual(vocabulary, retriever.vectorizer.vocabulary_)
        self.assertTrue((idf == retriever.vectorizer.idf_).all())
        self.assertIn('1', vocabulary)
        self.assertIn('phí', vocabulary)
        self.assertNotIn('reference_answer_secret', vocabulary)

    def test_source_context_counts_but_editorial_context_does_not(self):
        body = chunk('body', 'Giá 100 đồng.')
        prefix = 'Giá 100 đồng.\n'
        repeated = chunk('repeated', prefix+'Nội dung khác')
        repeated['body_char_start'] = len(prefix)
        repeated['context_source_spans'] = [dict(pdf_page=1, char_start=0, char_end=13)]
        fake = copy.deepcopy(repeated)
        fake['chunk_id'] = 'editorial'
        fake['context_source_spans'] = []
        questions = [dict(question_id='Q', evidence=[dict(doc_id='X',pdf_page=1,quote='Giá 100 đồng.')])]
        pages = [dict(doc_id='X',pdf_page=1,text='Giá 100 đồng.')]
        gold = align_gold(questions, [body,repeated,fake], pages)
        self.assertEqual(gold[0]['groups'][0]['body_chunk_ids'], ['body'])
        self.assertEqual(gold[0]['groups'][0]['chunk_ids'], ['body','repeated'])
        pages[0]['text'] = 'Không có bằng chứng này'
        with self.assertRaisesRegex(ValueError, 'source page'):
            align_gold(questions,[body],pages)

    def test_metrics_for_partial_complete_and_no_hits(self):
        groups = [dict(chunk_ids=['a','alternative']),dict(chunk_ids=['b'])]
        partial = retrieval_metrics(['wrong','a','b'], groups, 2)
        self.assertEqual(partial['hit'], 1)
        self.assertEqual(partial['evidence_recall'], .5)
        self.assertEqual(partial['chunk_recall'], 1/3)
        self.assertEqual(partial['all_evidence_hit'], 0)
        self.assertEqual(partial['mrr'], .5)
        self.assertEqual(retrieval_metrics(['a','b'],groups,2)['all_evidence_hit'], 1)
        self.assertTrue(all(v == 0 for v in retrieval_metrics([],groups,5).values()))

    def test_full_corpus_alignment_and_macro_metrics(self):
        gold = align_gold(self.questions,self.chunks,self.pages)
        self.assertEqual(len(gold), 20)
        self.assertEqual(sum(len(q['groups']) for q in gold), 30)
        retriever = TfidfRetriever(self.chunks)
        rows, summary, details = evaluate(retriever,self.questions,gold,[1,3,5])
        self.assertEqual(len(rows), 60)
        self.assertEqual(len(details), 20)
        for metric in summary:
            selected = [r for r in rows if r['k']==metric['k']]
            self.assertEqual(len(selected),20)
            for name in list(metric)[1:]:
                self.assertAlmostEqual(metric[name],sum(r[name] for r in selected)/20)
        for q in self.questions:
            selected = [r for r in rows if r['question_id']==q['question_id']]
            for name in ['hit_rate','chunk_recall','evidence_recall','all_evidence_hit']:
                self.assertEqual([r[name] for r in selected],sorted(r[name] for r in selected))

    def test_saved_index_reconstructs_same_rankings(self):
        import tempfile
        retriever = TfidfRetriever(self.chunks)
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory)/'index.joblib'
            joblib.dump(dict(vectorizer=retriever.vectorizer,matrix=retriever.matrix),path)
            loaded = joblib.load(path)
            restored = TfidfRetriever.__new__(TfidfRetriever)
            restored.chunks = retriever.chunks
            restored.vectorizer = loaded['vectorizer']
            restored.matrix = loaded['matrix']
            question = self.questions[0]['question']
            self.assertEqual(retriever.search(question),restored.search(question))


if __name__ == '__main__':
    unittest.main()
