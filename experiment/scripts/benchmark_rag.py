"""Compare the repository's three retrievers with one fixed RAG generator."""

import argparse
import gc
import hashlib
import importlib.metadata
import io
import json
from pathlib import Path
import sys
from time import perf_counter
import zipfile


EXPERIMENT = Path(__file__).resolve().parents[1]
EMBEDDER = "BAAI/bge-m3"
EMBEDDER_SHA = "5617a9f61b028005a4858fdac845db406aefb181"
GENERATOR = "Qwen/Qwen2.5-1.5B-Instruct"
GENERATOR_SHA = "989aa7980e4cf806f80c7fef2b1adb7bc71aa306"
TOP_KS = (1, 3, 5)
MAX_INPUT = 8192
MAX_OUTPUT = 384
KERNEL_TITLE = "S07 RAG Retrieval Methods Benchmark"
KERNEL_ID = "tunlnh/s07-rag-retrieval-methods-benchmark"
DATASET = "tunlnh/s07-hcmus-rag-corpus"


def package_kaggle(output):
    modules = ("rag_embedding.py", "tfidf_retrieval.py", "bm25_retrieval.py")
    sources = {name: (EXPERIMENT / name).read_text(encoding="utf-8") for name in modules}
    sources["scripts/benchmark_rag.py"] = Path(__file__).read_text(encoding="utf-8")
    dependencies = " ".join(
        line for name in ("requirements-rag.txt", "requirements-tfidf.txt")
        for line in (EXPERIMENT / name).read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.startswith("#")
    )
    setup = (
        "from pathlib import Path\n"
        "import subprocess, sys\n"
        "src = Path('/tmp/s07_rag_benchmark_src')\n"
        "(src / 'scripts').mkdir(parents=True, exist_ok=True)\n"
        f"sources = {sources!r}\n"
        "for name, code in sources.items():\n"
        "    (src / name).write_text(code, encoding='utf-8')\n"
        "subprocess.run([sys.executable, '-u', str(src / 'scripts/benchmark_rag.py'),\n"
        "                '--output', '/kaggle/working'], check=True)\n"
    )
    notebook = {
        "nbformat": 4,
        "nbformat_minor": 5,
        "metadata": {"kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"}},
        "cells": [
            {"cell_type": "markdown", "id": "overview", "metadata": {},
             "source": "# S07 — Benchmark RAG\nTF-IDF, BM25 và BGE-M3 trên cùng corpus và 20 câu hỏi. "
                       "Cả ba dùng cùng Qwen, prompt, top-5 và giới hạn sinh."},
            {"cell_type": "code", "id": "install", "metadata": {}, "execution_count": None, "outputs": [],
             "source": f"%pip install -q {dependencies}"},
            {"cell_type": "code", "id": "benchmark", "metadata": {}, "execution_count": None, "outputs": [],
             "source": setup},
        ],
    }
    output.mkdir(parents=True, exist_ok=True)
    (output / "benchmark.ipynb").write_text(json.dumps(notebook, ensure_ascii=False, indent=2), encoding="utf-8")
    metadata = {"id": KERNEL_ID, "title": KERNEL_TITLE, "code_file": "benchmark.ipynb",
                "language": "python", "kernel_type": "notebook", "is_private": True,
                "enable_gpu": True, "enable_internet": True, "dataset_sources": [DATASET],
                "competition_sources": [], "kernel_sources": []}
    (output / "kernel-metadata.json").write_text(json.dumps(metadata, indent=2), encoding="utf-8")


def dense_vectors(chunks, questions, cache):
    import numpy as np
    from rag_embedding import corpus_fingerprint, unit_vectors

    texts = [q["question"] for q in questions]
    if cache:
        with zipfile.ZipFile(cache) as archive:
            index = json.loads(archive.read("index_manifest.json"))
            previous_queries = json.loads(archive.read("retrieval_hits.json"))
            if [row["question"] for row in previous_queries][:len(texts)] != texts:
                raise ValueError("Cached query order does not match the benchmark")
            vectors = archive.read("embeddings.npy")
            if (index["fingerprint"] != corpus_fingerprint(chunks, EMBEDDER, EMBEDDER_SHA)
                    or index["embeddings_sha256"] != hashlib.sha256(vectors).hexdigest()):
                raise ValueError("Cached embeddings do not match corpus and model revision")
            matrix = np.load(io.BytesIO(vectors), allow_pickle=False)
            queries = np.load(io.BytesIO(archive.read("query_embeddings.npy")), allow_pickle=False)[:len(texts)]
        return unit_vectors(matrix), unit_vectors(queries)

    import torch
    from sentence_transformers import SentenceTransformer

    encoder = SentenceTransformer(EMBEDDER, revision=EMBEDDER_SHA, device="cuda:0",
                                  model_kwargs={"torch_dtype": torch.float16})
    documents = [c["text"] for c in chunks]
    lengths = [len(encoder.tokenizer(text, truncation=False)["input_ids"]) for text in documents + texts]
    if max(lengths) > encoder.max_seq_length:
        raise ValueError("Embedding tokenizer would truncate an input")
    matrix = encoder.encode(documents, batch_size=4, normalize_embeddings=True, show_progress_bar=True)
    queries = encoder.encode(texts, batch_size=4, normalize_embeddings=True)
    del encoder
    gc.collect()
    torch.cuda.empty_cache()
    return unit_vectors(matrix), unit_vectors(queries)


def answer_all(questions, rankings, gold_by_id, output):
    import torch
    from transformers import AutoModelForCausalLM, AutoTokenizer, LogitsProcessor
    from rag_embedding import citation_audit, fit_context, retrieval_metrics, save_json, validate_answer_text

    class FiniteLogits(LogitsProcessor):
        def __call__(self, input_ids, scores):
            if not torch.isfinite(scores).all():
                raise FloatingPointError("Non-finite generation logits")
            return scores

    torch.manual_seed(42)
    tokenizer = AutoTokenizer.from_pretrained(GENERATOR, revision=GENERATOR_SHA)
    model = AutoModelForCausalLM.from_pretrained(
        GENERATOR, revision=GENERATOR_SHA, torch_dtype=torch.float32,
        device_map="cuda:0", attn_implementation="sdpa",
    ).eval()
    answers = []
    for question in questions:
        qid = question["question_id"]
        for method, hits in rankings[qid].items():
            row = {"question_id": qid, "method": method, "question": question["question"],
                   "reference_answer": question["reference_answer"]}
            if not hits:
                answers.append(dict(row, status="no_context", answer="", context_ids=[]))
                continue
            messages, used, omitted = fit_context(tokenizer, question["question"], hits, MAX_INPUT)
            ids = [hit["chunk_id"] for hit in used]
            coverage = retrieval_metrics(ids, gold_by_id[qid]["groups"], len(ids))
            tokens = tokenizer.apply_chat_template(messages, tokenize=True, add_generation_prompt=True)
            input_ids = torch.tensor([tokens], device="cuda:0")
            start = perf_counter()
            with torch.inference_mode():
                result = model.generate(
                    input_ids=input_ids, attention_mask=torch.ones_like(input_ids),
                    max_new_tokens=MAX_OUTPUT, do_sample=False, use_cache=True,
                    pad_token_id=tokenizer.eos_token_id, logits_processor=[FiniteLogits()],
                )
            torch.cuda.synchronize()
            seconds = perf_counter() - start
            new_tokens = result[0, input_ids.shape[1]:]
            answer = tokenizer.decode(new_tokens, skip_special_tokens=True).strip()
            try:
                validate_answer_text(answer)
                status = "generated"
            except ValueError:
                status = "degenerate_text"
            audit = citation_audit(answer, used)
            valid_ids = sorted(set(audit["cited_ids"]) & set(ids))
            answers.append(dict(
                row, status=status, answer=answer, prompt=messages, context_ids=ids,
                omitted_context_ids=omitted, context_evidence_recall=coverage["evidence_recall"],
                context_all_evidence=bool(coverage["all_evidence_hit"]), input_tokens=len(tokens),
                output_tokens=len(new_tokens), reached_token_limit=len(new_tokens) == MAX_OUTPUT,
                seconds=seconds, citations=audit, valid_inline_ids=valid_ids,
            ))
            save_json(output / "answers.json", answers)
            print(f"{len(answers)}/{len(questions)*len(rankings[qid])} {qid} {method} {seconds:.1f}s", flush=True)
    save_json(output / "answers.json", answers)
    return len(answers)


def run(args):
    sys.path.insert(0, str(EXPERIMENT))
    import numpy as np
    from bm25_retrieval import Bm25Retriever
    from rag_embedding import load_dataset, retrieval_metrics, save_json, search
    from tfidf_retrieval import TfidfRetriever, align_gold, write_csv

    if not args.retrieval_only or not args.dense_cache:
        import torch
        if not torch.cuda.is_available():
            raise RuntimeError("CUDA is required for uncached BGE-M3 or generation")
    root, data = load_dataset(args.data_dir)
    chunks, questions = data["corpus"]["value"]["chunks"], data["questions"]["value"]
    page_path = root / "processed/corpus_pages.json"
    pages = json.loads(page_path.read_text(encoding="utf-8"))
    gold = align_gold(questions, chunks, pages)
    gold_by_id = {item["question_id"]: item for item in gold}
    tfidf, bm25 = TfidfRetriever(chunks), Bm25Retriever(chunks)
    matrix, queries = dense_vectors(chunks, questions, args.dense_cache)
    rankings, metrics = {}, []
    for q, query in zip(questions, queries, strict=True):
        qid, text = q["question_id"], q["question"]
        rankings[qid] = {"tfidf": tfidf.search(text, max(TOP_KS)),
                         "bm25": bm25.search(text, max(TOP_KS)),
                         "bge_m3": search(chunks, matrix, query, max(TOP_KS))}
        for method, hits in rankings[qid].items():
            ids = [hit["chunk_id"] for hit in hits]
            groups = gold_by_id[qid]["groups"]
            body = [{"chunk_ids": group["body_chunk_ids"]} for group in groups]
            for k in TOP_KS:
                metrics.append(dict(
                    method=method, question_id=qid, k=k, **retrieval_metrics(ids, groups, k),
                    body_evidence_recall=retrieval_metrics(ids, body, k)["evidence_recall"],
                ))
    summary = []
    metric_names = list(metrics[0])[3:]
    for method in ("tfidf", "bm25", "bge_m3"):
        for k in TOP_KS:
            selected = [row for row in metrics if row["method"] == method and row["k"] == k]
            summary.append(dict(method=method, k=k, **{
                name: float(np.mean([row[name] for row in selected])) for name in metric_names
            }))
    args.output.mkdir(parents=True, exist_ok=True)
    write_csv(args.output / "retrieval_summary.csv", summary)
    write_csv(args.output / "retrieval_per_question.csv", metrics)
    save_json(args.output / "retrieval_hits.json", {
        qid: {method: [{key: hit[key] for key in ("chunk_id", "rank", "score", "doc_id", "pdf_pages")}
                       for hit in hits] for method, hits in methods.items()}
        for qid, methods in rankings.items()
    })
    print(json.dumps(summary, ensure_ascii=False), flush=True)
    packages = ["numpy", "scipy", "scikit-learn", "joblib"]
    if not args.retrieval_only:
        packages.extend(["torch", "sentence-transformers", "transformers", "accelerate"])
    manifest = dict(
        chunk_count=len(chunks), question_ids=[q["question_id"] for q in questions],
        evidence_count=sum(len(g["groups"]) for g in gold), retrieval_ks=TOP_KS,
        generation_top_k=max(TOP_KS), data_sha256={key: value["sha256"] for key, value in data.items()},
        pages_sha256=hashlib.sha256(page_path.read_bytes()).hexdigest(),
        gold="source body + provenance-checked repeated context", human_review_status="pending",
        embedder=EMBEDDER, embedder_revision=EMBEDDER_SHA, dense_cache=bool(args.dense_cache),
        generator=GENERATOR, generator_revision=GENERATOR_SHA, generator_dtype="float32",
        attention="sdpa", max_input_tokens=MAX_INPUT, max_output_tokens=MAX_OUTPUT,
        do_sample=False, seed=42, packages={name: importlib.metadata.version(name) for name in packages},
        code_sha256={path.name: hashlib.sha256(path.read_bytes()).hexdigest()
                     for path in [Path(__file__), *(EXPERIMENT / name for name in
                                                   ("rag_embedding.py", "tfidf_retrieval.py", "bm25_retrieval.py"))]},
    )
    save_json(args.output / "manifest.json", manifest)
    if not args.retrieval_only:
        manifest["gpu"] = torch.cuda.get_device_name(0)
        manifest["completed_answers"] = answer_all(questions, rankings, gold_by_id, args.output)
        save_json(args.output / "manifest.json", manifest)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data-dir", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--retrieval-only", action="store_true")
    parser.add_argument("--dense-cache", type=Path, help="Verified ZIP from the original Kaggle run")
    parser.add_argument("--package-kaggle", action="store_true")
    args = parser.parse_args()
    if args.package_kaggle:
        package_kaggle(args.output)
    else:
        run(args)


if __name__ == "__main__":
    main()
