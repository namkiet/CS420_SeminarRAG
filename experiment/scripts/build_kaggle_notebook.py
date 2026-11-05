"""Build a Kaggle notebook from the tested helper; data is a separate Kaggle Dataset."""
import json
from pathlib import Path
import textwrap

ROOT = Path(__file__).resolve().parents[1]
cells = []


def md(text):
    cells.append({"cell_type": "markdown", "metadata": {}, "source": textwrap.dedent(text).strip() + "\n"})


def code(text):
    cells.append({"cell_type": "code", "execution_count": None, "metadata": {},
                  "outputs": [], "source": textwrap.dedent(text).strip() + "\n"})


md('''
    # S07 — RAG tiếng Việt bằng embedding trên Kaggle
    **Pipeline:** 162 chunks có sẵn → BGE-M3 dense embeddings → cosine top-k → Qwen2.5 → câu trả lời kèm nguồn.
    Không huấn luyện/fine-tune, không chia chunk lại. Chỉ index trường `text` của corpus.

    **Cách chạy:** Settings → Accelerator → GPU T4/P100; bật Internet; Run All.
    Add Input → Your Datasets → **S07 HCMUS RAG Corpus**; không cần API key.
    Mặc định chạy đủ 20 câu hỏi, so sánh cùng LLM có/không dùng RAG.
    Thay `CUSTOM_QUESTION` để hỏi câu khác. Output ở `/kaggle/working/s07_rag`.

    **Giới hạn:** OCR và đáp án còn chờ kiểm tra độc lập. Gold retrieval được ánh xạ tự động
    bằng trích đoạn nguyên văn + tài liệu + trang, là nhãn tạm để đánh giá.
    Citation audit chỉ kiểm tra ID; nhóm cần đọc câu trả lời và bằng chứng để chấm đúng/sai.
    Đây là baseline RAG dùng dense retrieval, không phải tái huấn luyện mô hình RAG của Lewis et al.
''')
code('%pip install -q sentence-transformers==5.1.2 transformers==4.57.1 accelerate==1.11.0 huggingface-hub==0.36.0')
md('''
    ## 1. Cấu hình và dữ liệu
    BGE-M3 hỗ trợ đa ngôn ngữ và đầu vào dài; vẫn kiểm tra token của từng chunk bằng tokenizer thật.
    162 vector nhỏ nên tìm kiếm cosine chính xác bằng NumPy, chưa cần cơ sở dữ liệu vector.
    Model revision được resolve thành SHA và ghi vào manifest để chạy lại.
''')
code('''
    from pathlib import Path
    import gc, hashlib, importlib.metadata, json, platform, random, time
    import numpy as np
    import pandas as pd
    import torch
    from IPython.display import display, Markdown
    from huggingface_hub import HfApi
    from sentence_transformers import SentenceTransformer
    from transformers import AutoTokenizer, AutoModelForCausalLM, LogitsProcessor

    EMBEDDING_MODEL = "BAAI/bge-m3"
    GENERATOR_MODEL = "Qwen/Qwen2.5-1.5B-Instruct"
    EMBEDDING_REVISION = None  # set SHA from run_manifest.json to reproduce a prior run
    GENERATOR_REVISION = None
    TOP_KS = [1, 3, 5]
    GENERATION_TOP_K = 5
    MAX_INPUT_TOKENS = 8192
    MAX_NEW_TOKENS = 384
    GENERATOR_DTYPE = torch.float32  # FP16 produced degenerate output on this Kaggle T4 runtime
    EVAL_LIMIT = None  # None = all 20; use 2 for a smoke run
    RUN_GENERATION = True
    CUSTOM_QUESTION = "Điều kiện đăng ký học phần tiên quyết là gì?"
    DATA_ROOT = None  # auto-detect attached Kaggle dataset; or set a specific directory
    OUTPUT = Path("/kaggle/working/s07_rag")
    OUTPUT.mkdir(parents=True, exist_ok=True)
    SEED = 42
    random.seed(SEED); np.random.seed(SEED); torch.manual_seed(SEED)
    DEVICE = "cuda:0" if torch.cuda.is_available() else "cpu"
    print("Device:", DEVICE)
    if DEVICE == "cpu":
        print("CPU sẽ chậm. Nên bật GPU trước khi Run All.")
''')
code((ROOT / "rag_embedding.py").read_text(encoding="utf-8"))
code('''
    # Only corpus chunks enter the index; questions/answers are evaluation data.
    DATA_ROOT, DATA = load_dataset(DATA_ROOT)
    chunks = DATA["corpus"]["value"]["chunks"]
    all_questions = DATA["questions"]["value"]
    questions = all_questions if EVAL_LIMIT is None else all_questions[:EVAL_LIMIT]
    sources = DATA["sources"]["value"]
    validate_chunks(chunks)
    if not questions: raise ValueError("No evaluation questions")
    gold = align_evidence(questions, chunks)
    save_json(OUTPUT / "gold_alignment.json", gold)
    print("Dataset directory:", DATA_ROOT)
    print({"chunks": len(chunks), "questions": len(questions), "evidence": sum(len(g["groups"]) for g in gold)})
    display(pd.DataFrame(chunks)[["doc_id", "chunk_id", "section", "pdf_pages"]].head())
''')
md('''
    ## 2. Embedding và index
    Chuẩn hóa L2 để dot product = cosine. Không dùng ngưỡng cosine tùy ý làm xác suất đúng.
    Cache chỉ tái sử dụng nếu corpus, thứ tự chunk, model và model revision giống nhau.
    Không cắt ngầm chunk nếu vượt giới hạn token của embedding model.
''')
code('''
    api = HfApi()
    embedding_sha = api.model_info(EMBEDDING_MODEL, revision=EMBEDDING_REVISION).sha
    encoder = SentenceTransformer(EMBEDDING_MODEL, revision=embedding_sha, device=DEVICE,
                                model_kwargs={"torch_dtype": torch.float16 if DEVICE.startswith("cuda") else torch.float32})
    texts = [c["text"] for c in chunks]
    lengths = [len(encoder.tokenizer(t, truncation=False)["input_ids"]) for t in texts]
    too_long = [chunks[i]["chunk_id"] for i, n in enumerate(lengths) if n > encoder.max_seq_length]
    if too_long:
        raise ValueError(f"Embedding would truncate chunks: {too_long}")
    fingerprint = corpus_fingerprint(chunks, EMBEDDING_MODEL, embedding_sha)
    cache_file, meta_file = OUTPUT / "embeddings.npy", OUTPUT / "index_manifest.json"
    started = time.perf_counter()
    meta = json.loads(meta_file.read_text()) if meta_file.exists() else {}
    if cache_file.exists() and meta.get("fingerprint") == fingerprint:
        matrix = unit_vectors(np.load(cache_file, allow_pickle=False))
        if matrix.shape != (len(chunks), encoder.get_sentence_embedding_dimension()):
            raise ValueError("Cached matrix shape mismatch")
        if hashlib.sha256(cache_file.read_bytes()).hexdigest() != meta["embeddings_sha256"]:
            raise ValueError("Cached embedding checksum mismatch")
        print("Loaded matching embedding cache")
    else:
        matrix = unit_vectors(encoder.encode(texts, batch_size=4, show_progress_bar=True,
                                            normalize_embeddings=True, convert_to_numpy=True))
        np.save(cache_file, matrix)
    save_json(meta_file, {"fingerprint": fingerprint, "model": EMBEDDING_MODEL,
                         "revision": embedding_sha, "shape": list(matrix.shape),
                         "chunk_ids": [c["chunk_id"] for c in chunks],
                         "embeddings_sha256": hashlib.sha256(cache_file.read_bytes()).hexdigest(),
                         "max_actual_tokens": max(lengths), "max_model_tokens": encoder.max_seq_length})
    query_texts = [q["question"] for q in questions] + [CUSTOM_QUESTION]
    query_lengths = [len(encoder.tokenizer(t, truncation=False)["input_ids"]) for t in query_texts]
    if max(query_lengths) > encoder.max_seq_length:
        raise ValueError("Question exceeds embedding token limit")
    query_vectors = unit_vectors(encoder.encode(query_texts, batch_size=4,
                                               normalize_embeddings=True, convert_to_numpy=True))
    np.save(OUTPUT / "query_embeddings.npy", query_vectors)
    embedding_seconds = time.perf_counter() - started
    ranked = [search(chunks, matrix, v, max(TOP_KS + [GENERATION_TOP_K])) for v in query_vectors]
    save_json(OUTPUT / "retrieval_hits.json", [
        {"question": question, "hits": hits} for question, hits in zip(query_texts, ranked)])
    print("Embedding shape:", matrix.shape, "max token:", max(lengths), "seconds:", round(embedding_seconds, 2))
''')
md('''
    ## 3. Đánh giá retrieval (nhãn tạm)
    - **Hit@k:** tìm được ít nhất một bằng chứng.
    - **Evidence Recall@k:** tỷ lệ đoạn bằng chứng yêu cầu được tìm thấy. Hai chunk chứa cùng bằng chứng là lựa chọn thay thế.
    - **All Evidence Hit@k:** tìm đủ tất cả bằng chứng của câu hỏi.
    - **Chunk Recall@k:** phần chunk liên quan đã tìm; **MRR@k:** nghịch đảo hạng relevant đầu tiên.
    Không bỏ câu khó/không ánh xạ được khỏi mẫu số: lỗi ánh xạ sẽ dừng notebook.
''')
code('''
    metric_rows = []
    for q, g, hits in zip(questions, gold, ranked):
        for k in TOP_KS:
            metric_rows.append({"question_id": q["question_id"], "k": k,
                                **retrieval_metrics([h["chunk_id"] for h in hits], g["groups"], k)})
    metrics = pd.DataFrame(metric_rows)
    summary = metrics.groupby("k").mean(numeric_only=True).reset_index()
    metrics.to_csv(OUTPUT / "retrieval_per_question.csv", index=False)
    summary.to_csv(OUTPUT / "retrieval_summary.csv", index=False)
    display(summary)
    display(pd.DataFrame(ranked[-1])[["rank", "chunk_id", "score", "pdf_pages", "section"]])
    # Free encoder GPU memory before loading the generator.
    del encoder
    gc.collect()
    if torch.cuda.is_available(): torch.cuda.empty_cache()
''')
md('''
    ## 4. Sinh câu trả lời: RAG và baseline không retrieval
    Cùng model, greedy decoding và số token tối đa. RAG được cung cấp tối đa 5 chunks;
    giữ nguyên chunk và thứ tự xếp hạng, dừng thêm khi hết ngân sách prompt.
    Mọi chunk bị loại khỏi prompt được ghi lại riêng: retrieval thành công chưa chắc generation đã nhận đủ bằng chứng.
    `ask()` cho phép hỏi tiếp sau khi chạy notebook, encoder chỉ nạp lại khi cần câu hỏi mới.
''')
code('''
    generator_sha = None
    answer_rows = []
    if RUN_GENERATION:
        if "llm" in globals():
            del llm
            gc.collect()
            if torch.cuda.is_available(): torch.cuda.empty_cache()
        generator_sha = api.model_info(GENERATOR_MODEL, revision=GENERATOR_REVISION).sha
        tokenizer = AutoTokenizer.from_pretrained(GENERATOR_MODEL, revision=generator_sha)
        llm = AutoModelForCausalLM.from_pretrained(
            GENERATOR_MODEL, revision=generator_sha,
            torch_dtype=GENERATOR_DTYPE,
            device_map=DEVICE, attn_implementation="sdpa")
        llm.eval()
        context_limit = getattr(llm.config, "max_position_embeddings", 32768)
        if MAX_INPUT_TOKENS + MAX_NEW_TOKENS > context_limit:
            raise ValueError("Prompt + output budget exceeds generator context")

        class FiniteLogitsProcessor(LogitsProcessor):
            def __call__(self, input_ids, scores):
                if not torch.isfinite(scores).all():
                    raise FloatingPointError("Non-finite generation logits; stop instead of saving invalid answers")
                return scores

        def generate(messages):
            ids = tokenizer.apply_chat_template(messages, tokenize=True, add_generation_prompt=True)
            if len(ids) > MAX_INPUT_TOKENS:
                raise ValueError("Generation prompt exceeds budget; no silent truncation")
            inputs = {"input_ids": torch.tensor([ids], device=DEVICE),
                      "attention_mask": torch.ones((1, len(ids)), dtype=torch.long, device=DEVICE)}
            start = time.perf_counter()
            with torch.inference_mode():
                outputs = llm.generate(**inputs, max_new_tokens=MAX_NEW_TOKENS, do_sample=False,
                                       pad_token_id=tokenizer.eos_token_id, use_cache=True,
                                       logits_processor=[FiniteLogitsProcessor()])
            new_ids = outputs[0, len(ids):]
            answer = tokenizer.decode(new_ids, skip_special_tokens=True).strip()
            validate_answer_text(answer)
            return {"answer": answer,
                    "input_tokens": len(ids), "output_tokens": len(new_ids),
                    "reached_token_limit": len(new_ids) == MAX_NEW_TOKENS,
                    "seconds": time.perf_counter() - start}

        def answer_from_hits(question, hits):
            messages, used, omitted = fit_context(tokenizer, question, hits, MAX_INPUT_TOKENS)
            result = generate(messages)
            return {**result, "context_ids": [h["chunk_id"] for h in used],
                    "omitted_context_ids": omitted, "prompt": messages,
                    "citations": citation_audit(result["answer"], used),
                    "sources": [{key: h.get(key) for key in
                                 ["chunk_id", "document_title", "pdf_pages", "section", "source_pdf_url"]}
                                for h in used]}

        for i, (q, hits) in enumerate(zip(questions, ranked), 1):
            baseline_messages = [
                {"role": "system", "content": "Trả lời ngắn gọn bằng tiếng Việt. Nếu không biết quy định HCMUS, nói rõ không đủ thông tin. Không bịa nguồn."},
                {"role": "user", "content": q["question"]}]
            baseline = generate(baseline_messages)
            rag = answer_from_hits(q["question"], hits[:GENERATION_TOP_K])
            answer_rows.append({"question_id": q["question_id"], "question": q["question"],
                                "reference_answer": q["reference_answer"],
                                "expected_key_points": q.get("expected_key_points", []),
                                "evidence": q["evidence"], "baseline": {**baseline, "prompt": baseline_messages}, "rag": rag})
            save_json(OUTPUT / "answers_comparison.json", answer_rows)
            print(i, "/", len(questions), q["question_id"], "saved")

        custom_answer = answer_from_hits(CUSTOM_QUESTION, ranked[-1][:GENERATION_TOP_K])
        save_json(OUTPUT / "custom_answer.json", {"question": CUSTOM_QUESTION, **custom_answer})
        display(Markdown(custom_answer["answer"]))

        def ask(question, k=5):
            if question in query_texts:
                v = query_vectors[query_texts.index(question)]
            else:
                # Use CPU for ad-hoc query embedding while LLM stays on GPU.
                query_encoder = SentenceTransformer(EMBEDDING_MODEL, revision=embedding_sha, device="cpu")
                if len(query_encoder.tokenizer(question, truncation=False)["input_ids"]) > query_encoder.max_seq_length:
                    raise ValueError("Question exceeds embedding limit")
                v = query_encoder.encode(question, normalize_embeddings=True, convert_to_numpy=True)
                del query_encoder
            return answer_from_hits(question, search(chunks, matrix, v, k))
    else:
        print("RUN_GENERATION=False: only retrieval was evaluated.")
''')
md('''
    ## 5. Lưu kết quả và mẫu chấm thủ công
    Chấm mỗi câu có/không RAG về đúng nội dung, đủ ý, trích dẫn hỗ trợ kết luận và biết từ chối khi thiếu nguồn.
    Để trống điểm; không dùng cosine similarity thay cho độ đúng câu trả lời.
    Xem lại PDF gốc trước khi kết luận, đặc biệt văn bản sửa đổi, bảng học phí và OCR.
''')
code('''
    manual_rows = []
    for row in answer_rows:
        for mode in ["baseline", "rag"]:
            manual_rows.append({"question_id": row["question_id"], "question": row["question"], "mode": mode,
                                "answer": row[mode]["answer"], "reference_answer": row["reference_answer"],
                                "correctness_1_5": "", "completeness_1_5": "", "citation_support_1_5": "",
                                "reviewer": "", "notes": ""})
    pd.DataFrame(manual_rows, columns=["question_id", "question", "mode", "answer", "reference_answer",
        "correctness_1_5", "completeness_1_5", "citation_support_1_5", "reviewer", "notes"]).to_csv(
            OUTPUT / "manual_review.csv", index=False)
    save_json(OUTPUT / "run_manifest.json", {
        "data_commit": "8bba55c1c62a286928955ecfcd63b549759285d1",
        "dataset_directory": str(DATA_ROOT), "dataset_ref": "tunlnh/s07-hcmus-rag-corpus",
        "data_sha256": {k: v["sha256"] for k, v in DATA.items()},
        "embedding_model": EMBEDDING_MODEL, "embedding_revision": embedding_sha,
        "generator_model": GENERATOR_MODEL, "generator_revision": generator_sha,
        "generator_dtype": str(GENERATOR_DTYPE), "generator_attention": "sdpa",
        "top_ks": TOP_KS, "generation_top_k": GENERATION_TOP_K, "seed": SEED,
        "max_input_tokens": MAX_INPUT_TOKENS, "max_new_tokens": MAX_NEW_TOKENS,
        "do_sample": False, "question_ids": [q["question_id"] for q in questions],
        "index_fingerprint": fingerprint, "device": DEVICE,
        "gpu": torch.cuda.get_device_name(0) if torch.cuda.is_available() else None,
        "python": platform.python_version(), "embedding_seconds": embedding_seconds,
        "packages": {p: importlib.metadata.version(p) for p in
                     ["torch", "numpy", "sentence-transformers", "transformers", "huggingface-hub", "accelerate"]},
        "human_review_status": "pending", "generation_completed": len(answer_rows)})
    print("Outputs:", OUTPUT)
    display(pd.DataFrame({"file": [p.name for p in sorted(OUTPUT.iterdir())],
                          "bytes": [p.stat().st_size for p in sorted(OUTPUT.iterdir())]}))
''')
md('''
    ## Nguồn và cách thay dữ liệu
    - [BGE-M3 model card](https://huggingface.co/BAAI/bge-m3): dùng dense vector qua Sentence Transformers.
    - [Qwen2.5-1.5B-Instruct](https://huggingface.co/Qwen/Qwen2.5-1.5B-Instruct): generator nhỏ để chạy GPU Kaggle.
    - [Sentence Transformers](https://sbert.net/docs/package_reference/sentence_transformer/SentenceTransformer.html).
    - [Transformers generation](https://huggingface.co/docs/transformers/main_classes/text_generation).

    [Kaggle Dataset](https://www.kaggle.com/datasets/tunlnh/s07-hcmus-rag-corpus), snapshot dữ liệu từ commit `8bba55c`.
    Khi cập nhật corpus/questions, tạo version mới cho Dataset bằng ZIP từ
    `python experiment/scripts/package_kaggle_dataset.py`. Gắn đúng version trong Input.
    Manifest cache đảm bảo tạo lại vector khi thay corpus; SHA256SUMS kiểm tra dữ liệu tải lên.
    Nội dung nguồn và model được tải/chạy trong môi trường Kaggle; không gọi API trả phí.
''')
code('''
    import shutil
    from IPython.display import FileLink
    if RUN_GENERATION:
        print("Nguồn đã cung cấp cho câu hỏi demo (cần đối chiếu với kết luận của model):")
        display(pd.DataFrame(custom_answer["sources"]))
        if not custom_answer["citations"]["has_citation"]:
            print("Model chưa chèn citation trong đáp án; chưa được xem là trích dẫn đạt yêu cầu.")
    archive = shutil.make_archive("/kaggle/working/s07_rag_results", "zip", OUTPUT)
    display(FileLink(archive))
''')

notebook = {"nbformat": 4, "nbformat_minor": 5, "metadata": {
    "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
    "language_info": {"name": "python", "version": "3.11"},
    "kaggle": {"accelerator": "gpu", "isInternetEnabled": True, "language": "python", "sourceType": "notebook"}},
    "cells": cells}
for i, cell in enumerate(cells):
    cell["id"] = f"s07-{i:03d}"
target = ROOT / "notebooks" / "S07_RAG_Embedding_Kaggle.ipynb"
target.parent.mkdir(exist_ok=True)
target.write_text(json.dumps(notebook, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print(target, target.stat().st_size)
