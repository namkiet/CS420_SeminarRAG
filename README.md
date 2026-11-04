# Seminar Topic: RAG (S07)

## Team Members
- **Trịnh Võ Nam Kiệt** — `24125013`
- **Tuấn Lĩnh** — `241250XX`
- **Trần Đăng Lê Huy** — `24125057`

## Research Question & Objective
> **Guiding Question:** *Does providing external documents eliminate hallucinations in language models?*

The goal of this seminar topic is to:
1. Demystify how a retriever is integrated with a generative language model.
2. Differentiate **parametric memory** (model weights) from **non-parametric memory** (external retrieval index), contrasting RAG with fine-tuning and long-context prompting.
3. Quantitatively evaluate retrieval performance (e.g., Recall@k, Top-$k$ Hit Rate).
4. Analyze whether generated answers are strictly grounded in retrieved evidence and examine failure modes.

## Key Requirements & Tasks
1. **Theoretical Foundation & Modeling:**
   - Define RAG architecture and explain the pipeline: Ingestion $\to$ Chunking $\to$ Indexing $\to$ Retrieval $\to$ Prompt Augmentation $\to$ Answer Generation.
   - Formulate and analyze the **RAG-Sequence** and **RAG-Token** equations (e.g., $p(y|x) \approx \sum_{z \in \text{top-}k} p_\eta(z|x) \cdot p_\theta(y|x, z)$) with a step-by-step worked example.
2. **Corpus & Benchmark Creation:**
   - Build a curated knowledge corpus of ~5–10 pages from verifiable sources.
   - Construct a benchmark set of 15–20 questions paired with ground-truth reference answers and citations.
3. **Retrieval Experiments:**
   - Implement a lightweight retrieval system (sparse TF-IDF/BM25 or dense embedding cosine similarity).
   - Evaluate Top-$k$ Hit Rate / Recall@$k$ comparing at least two chunk sizes or values of $k$.
4. **Answer Generation & Failure Analysis:**
   - Compare responses generated with vs. without retrieval (grounding vs. hallucination).
   - Categorize failure modes: missing retrieval, irrelevant chunk retrieval, unfaithful generation, and invalid citations (identifying at least 3 failure cases).
   - Propose verification and document-update mechanisms.

## Key Deliverables
- **Research Report:** 6–10 page research-style paper in Vietnamese (A4 format).
- **Presentation Slides:** 8–12 content slides for a 15-minute seminar presentation + 5-minute Q&A.
- **Worked Examples & Code:** Complete end-to-end question-answering workflow with retrieval evaluation and failure analysis.

## Experiment Data — G2 Tasks 1–2

See [`experiment/README.md`](experiment/README.md) for the prepared dataset.

- [Corpus](experiment/data/processed/corpus_pages.json): text and metadata for all 51 pages of four source documents.
- [Chunks](experiment/data/chunks/chunks_by_structure.json): 162 chunks from 80 parent articles/sections, capped at 800 `cl100k_base` tokens including context. See `experiment/README.md` for setup and regeneration commands.
- [Evaluation questions](experiment/data/questions.json): 20 questions with reference answers and 30 evidence spans; keep outside the retrieval index.
- [Sources](experiment/data/sources.json): source links, document versions, scope, and checksums. Original PDFs are in `experiment/data/raw/`.
- Data files are ready to load directly; no build script is required. OCR accuracy still needs independent review on 29 pages.

## References
- **Lewis, P. et al. (2020).** *Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks.* NeurIPS 2020. [Paper Link](https://papers.neurips.cc/paper/2020/hash/6b493230205f780e1bc26945df7481e5-Abstract.html)
- **Schneider, J. (2024).** *Explainable Generative AI (GenXAI): a survey, conceptualization, and research agenda.* Artificial Intelligence Review 57, 289. [DOI](https://doi.org/10.1007/s10462-024-10916-x)
