import ast
import copy
import json
from pathlib import Path
import sys
import unittest

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from rag_embedding import (align_evidence, citation_audit, corpus_fingerprint, fit_context,
                           retrieval_metrics, search, unit_vectors, validate_chunks)


class RagTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.chunks = json.loads((ROOT / "data/chunks/chunks_by_structure.json").read_text(encoding="utf-8"))["chunks"]
        cls.questions = json.loads((ROOT / "data/questions.json").read_text(encoding="utf-8"))

    def test_full_corpus_and_all_evidence_align(self):
        validate_chunks(self.chunks)
        gold = align_evidence(self.questions, self.chunks)
        self.assertEqual(len(gold), 20)
        self.assertEqual(sum(len(g["groups"]) for g in gold), 30)
        for q in gold:
            all_ids = list(dict.fromkeys(cid for g in q["groups"] for cid in g["chunk_ids"]))
            self.assertEqual(retrieval_metrics(all_ids, q["groups"], len(all_ids))["all_evidence_hit"], 1)

    def test_alignment_rejects_wrong_page_and_editorial_only(self):
        q = copy.deepcopy(self.questions[:1])
        q[0]["evidence"][0]["pdf_page"] = 999
        with self.assertRaisesRegex(ValueError, "Unmapped"):
            align_evidence(q, self.chunks)
        q[0]["evidence"] = [{"doc_id": "X", "pdf_page": 1, "quote": "editorial"}]
        with self.assertRaises(ValueError):
            align_evidence(q, [{"chunk_id": "x", "doc_id": "X", "pdf_pages": [1],
                                "text": "editorial body", "body_char_start": 10}])

    def test_alternative_chunks_count_as_one_evidence(self):
        groups = [{"chunk_ids": ["a", "a2"]}, {"chunk_ids": ["b"]}]
        partial = retrieval_metrics(["a", "a2", "b"], groups, 2)
        self.assertEqual(partial["evidence_recall"], .5)
        self.assertEqual(partial["all_evidence_hit"], 0)
        self.assertEqual(retrieval_metrics(["z", "b"], groups, 2)["mrr"], .5)
        with self.assertRaises(ValueError):
            retrieval_metrics([], [{"chunk_ids": []}], 5)

    def test_cosine_scale_invariant_and_stable_ties(self):
        cs = [{"chunk_id": str(i)} for i in range(3)]
        hits = search(cs, [[2, 0], [1, 0], [0, 4]], [5, 0], 3)
        self.assertEqual([h["chunk_id"] for h in hits], ["0", "1", "2"])
        self.assertAlmostEqual(hits[0]["score"], 1)
        for values in [[[0, 0]], [[float("nan"), 1]]]:
            with self.assertRaises(ValueError): unit_vectors(values)

    def test_cache_changes_on_text_order_and_model_revision(self):
        fp = corpus_fingerprint(self.chunks, "model", "sha1")
        self.assertNotEqual(fp, corpus_fingerprint(self.chunks[::-1], "model", "sha1"))
        self.assertNotEqual(fp, corpus_fingerprint(self.chunks, "model", "sha2"))
        changed = copy.deepcopy(self.chunks)
        changed[0]["text"] += "new rule"
        self.assertNotEqual(fp, corpus_fingerprint(changed, "model", "sha1"))

    def test_prompt_budget_keeps_whole_ranked_chunks(self):
        class Tokenizer:
            def apply_chat_template(self, messages, **kwargs):
                return list("".join(m["content"] for m in messages))
        from rag_embedding import rag_messages
        hits = self.chunks[:3]
        budget = len(Tokenizer().apply_chat_template(rag_messages("q", hits[:1])))
        _, used, omitted = fit_context(Tokenizer(), "q", hits, budget)
        self.assertEqual(used, hits[:1])
        self.assertEqual(omitted, [h["chunk_id"] for h in hits[1:]])
        with self.assertRaises(ValueError): fit_context(Tokenizer(), "q", hits, 1)

    def test_citation_audit_rejects_unretrieved_id(self):
        result = citation_audit("Có [chunk1], nhưng [chunk2]", [{"chunk_id": "chunk1"}])
        self.assertEqual(result["unknown_ids"], ["chunk2"])

    def test_notebook_python_cells_and_embedded_snapshot(self):
        nb = json.loads((ROOT / "notebooks/S07_RAG_Embedding_Kaggle.ipynb").read_text(encoding="utf-8"))
        for cell in nb["cells"]:
            if cell["cell_type"] == "code" and not cell["source"].startswith("%"):
                ast.parse(cell["source"])
        embedded = next(c["source"] for c in nb["cells"] if "DATA = json.loads(" in c["source"])
        namespace = {"json": json, "validate_chunks": validate_chunks, "align_evidence": align_evidence,
                     "EVAL_LIMIT": None, "save_json": lambda *a: None, "OUTPUT": ROOT,
                     "display": lambda *a: None, "pd": __import__("pandas")}
        exec(compile(embedded, "embedded_data", "exec"), namespace)
        self.assertEqual(namespace["chunks"], self.chunks)
        self.assertEqual(namespace["questions"], self.questions)


if __name__ == "__main__":
    unittest.main()
