# Dàn ý Chi tiết & Timeline Bộ Slides Thuyết trình: RAG (S07)

> **Môn học:** CS420 — Nhập môn Trí tuệ Nhân tạo | Trường ĐH Khoa học Tự nhiên, ĐHQG-HCM  
> **Chủ đề Seminar:** [S07] Retrieval-Augmented Generation (RAG): Grounding LLM Responses in Documents  
> **Quy định thời gian:** Đúng **15 phút** thuyết trình (bắt buộc cả 3 thành viên đều nói) + **5 phút** Q&A  
> **Quy mô slides:** **20 slides tổng cộng** (1 Slide Bìa + 1 Slide Outline + 16 Slides Nội dung Trọng tâm + 1 References + 1 Thank You / Q&A)  
> **Phong cách thiết kế:** Tối giản theo chuẩn Beamer Madrid (GraphPlanner Style) — Mỗi slide chỉ chứa tối đa 1 bảng số liệu hoặc 1 sơ đồ luồng/công thức + 2–4 gạch đầu dòng ngắn gọn; có footnote nguồn ở góc dưới trái.  
> **Ngôn ngữ hiển thị:** Tiêu đề, bảng biểu, công thức và bullets trên mặt slide trình bày bằng **Tiếng Anh học thuật** (khớp 100% với file báo cáo `report/S07_Bao_Cao_RAG_HCMUS.tex`); kịch bản điều phối, ghi chú diễn giả và hướng dẫn luyện tập bằng **Tiếng Việt**.  
> **Phân công diễn giả:** Cân bằng hoàn hảo 3 thành viên (**mỗi người đúng 5:00 phút / 300 giây**):  
> - **Speaker 1 (00:00 – 05:00):** Trịnh Võ Nam Kiệt (`24125013`) — *Lý thuyết Nền tảng, Kiến trúc Pipeline & Mô hình Xác suất* (Slides 1–7)  
> - **Speaker 2 (05:00 – 10:00):** Trần Đăng Lê Huy (`24125057`) — *Corpus HCMUS, Thực nghiệm Retrieval & Worked Example Q01* (Slides 8–12)  
> - **Speaker 3 (10:00 – 15:00):** Bùi Trọng Tuấn Lĩnh (`24125066`) — *Chất lượng Sinh ngữ 4 Nhánh, 5 Ca lỗi, Thảo luận & Hậu kiểm* (Slides 13–20)  

---

## 1. Timeline Chi tiết theo Từng Giây (Minute-by-Minute Timeline)

```mermaid
gantt
    title TIMELINE THUYẾT TRÌNH SEMINAR S07 (TỔNG CỘNG ĐÚNG 15 PHÚT)
    dateFormat mm:ss
    axisFormat %M:%S
    
    section Speaker 1: Nam Kiệt (5:00)
    Slide 01: Title Page                 :00:00, 00:35
    Slide 02: Outline Roadmap            :00:35, 01:00
    Slide 03: Introduction & Question    :01:00, 01:50
    Slide 04: Grounding Paradigms        :01:50, 02:40
    Slide 05: Architecture & Failures    :02:40, 03:30
    Slide 06: Probabilistic Formulation  :03:30, 04:15
    Slide 07: Numerical Example (k=2)    :04:15, 05:00
    
    section Speaker 2: Lê Huy (5:00)
    Slide 08: HCMUS Regulatory Corpus    :05:00, 05:55
    Slide 09: Retrieval Setup & Protocol :05:55, 06:45
    Slide 10: Exp 1 - Retrieval Benchmark:06:45, 07:45
    Slide 11: Worked Example Q01 Retrieval:07:45, 08:50
    Slide 12: Worked Example Q01 Output  :08:50, 10:00
    
    section Speaker 3: Tuấn Lĩnh (5:00)
    Slide 13: Exp 2 - 4-Way Quality      :10:00, 11:00
    Slide 14: 5 Failure Archetypes       :11:00, 12:05
    Slide 15: RAG vs. Hallucination      :12:05, 12:55
    Slide 16: Limitations & Boundaries   :12:55, 13:45
    Slide 17: Verification & Maintenance :13:45, 14:30
    Slide 18: Conclusions & Takeaways    :14:30, 15:00
    Slide 19: References                 :15:00, 15:00
    Slide 20: Q&A Allocation             :15:00, 15:00

    section Phiên Q&A (5:00)
    Cả 3 thành viên phản biện hội đồng   :15:00, 20:00
```

---

## 2. Bảng Phân công, Điều phối Thời gian & Tín hiệu Chuyển giao (Handoff Cues)

| Slide | File nguồn (`slides/content/`) | Mốc thời gian | Thời lượng | Tiêu đề trên Mặt Slide (English) | Diễn giả | Mục tiêu & Tín hiệu Chuyển giao (Handoff Cue) |
| :---: | :--- | :---: | :---: | :--- | :---: | :--- |
| **01** | `01_title.tex` | **00:00 – 00:35** | 35s | **[S07] Retrieval-Augmented Generation (RAG)** | **Nam Kiệt** | Chào hội đồng, giới thiệu nhóm 3 thành viên và tôn chỉ kết hợp lý thuyết với thực nghiệm độc lập. |
| **02** | `02_outline.tex` | **00:35 – 01:00** | 25s | **Outline** | **Nam Kiệt** | Trình bày lộ trình 3 phần rõ ràng tương ứng với thời lượng 5 phút của từng diễn giả. |
| **03** | `03_intro_question.tex` | **01:00 – 01:50** | 50s | **Introduction \& Guiding Question** | **Nam Kiệt** | Nêu hạn chế Parametric memory; Đặt câu hỏi nghiên cứu: *"Does external documents eliminate hallucinations?"* |
| **04** | `04_paradigms.tex` | **01:50 – 02:40** | 50s | **Knowledge Grounding Paradigms** | **Nam Kiệt** | So sánh Fine-tuning vs Long-context vs RAG qua bảng 3 hàng; Dẫn chứng kết quả Lewis et al. trên NQ. |
| **05** | `05_pipeline.tex` | **02:40 – 03:30** | 50s | **RAG Architecture \& Theoretical Failure Points** | **Nam Kiệt** | Sơ đồ luồng TikZ 6 bước; Phân tích 3 nhóm rủi ro lỗi: Pre-retrieval, Retrieval, và Post-retrieval. |
| **06** | `06_formulation.tex` | **03:30 – 04:15** | 45s | **Probabilistic Modeling: Sequence vs. Token** | **Nam Kiệt** | Trình bày 2 công thức Lewis et al. (2020), giải thích biến ẩn $z$ và sự khác biệt giữa Sequence và Token. |
| **07** | `07_numerical_example.tex` | **04:15 – 04:55** | 40s | **Worked Numerical Example ($k=2, T=2$)** | **Nam Kiệt** | Bảng $z_1, z_2$; tính ra $0.5280$ (Sequence) vs $0.4692$ (Token); giải thích sự không giao hoán giữa $\sum$ và $\prod$. |
| -- | -- | **04:55 – 05:00** | 05s | *[Chuyển giao 1]* | Nam Kiệt $\to$ Lê Huy | *"Để kiểm chứng lý thuyết trên văn bản thực tế, bạn Lê Huy sẽ trình bày phần thực nghiệm quy chế HCMUS."* |
| **08** | `08_corpus.tex` | **05:00 – 05:55** | 55s | **Experimental Corpus: HCMUS Regulations** | **Lê Huy** | Bảng 4 văn bản quy chế D01–D04 (51 trang, 162 chunks, trần 800 tokens); Benchmark 20 câu / 30 gold evidence. |
| **09** | `09_retrieval_setup.tex` | **05:55 – 06:45** | 50s | **Retrieval Configurations \& Evaluation Protocol** | **Lê Huy** | So sánh TF-IDF, BM25, Dense BGE-M3; Định nghĩa Evidence Recall@k, Hit Rate@k, All Evidence@k, MRR@k. |
| **10** | `10_retrieval_results.tex` | **06:45 – 07:45** | 60s | **Experiment 1: Retrieval Performance** | **Lê Huy** | Bảng Table 4: BM25 dẫn đầu top-1 (80.00\%), BGE-M3 dẫn đầu top-5 (89.17\%, Hit 95.00\%); Cảnh báo Hit $\neq$ Accuracy. |
| **11** | `11_worked_example_retrieval.tex` | **07:45 – 08:50** | 65s | **Worked Example (Q01): Top-5 Candidate Chunks** | **Lê Huy** | Case Q01: Tiên quyết vs Học trước; Bảng Top-5 chunks (Rank 1 Cosine = 0.6271, trang 4 chứa gold evidence Điều 3). |
| **12** | `12_worked_example_generation.tex` | **08:50 – 09:55** | 65s | **Worked Example (Q01): Grounded vs. Baseline Output** | **Lê Huy** | So sánh Baseline 0/2 (ảo giác) vs Grounded RAG 2/2 (đúng bản chất); Ghi rõ citation tag do nhóm đối chiếu bổ sung. |
| -- | -- | **09:55 – 10:00** | 05s | *[Chuyển giao 2]* | Lê Huy $\to$ Tuấn Lĩnh | *"Dù Q01 thành công, hệ thống vẫn tồn tại nhiều lỗi tinh vi. Xin mời bạn Tuấn Lĩnh phân tích các failure cases."* |
| **13** | `13_generation_quality.tex` | **10:00 – 11:00** | 60s | **Experiment 2: 4-Way Answer Quality** | **Tuấn Lĩnh** | Bảng Table 5: Baseline 0/20, RAG đạt 45–50\% (+45–50 pp); Điểm nghẽn: 0/60 đáp án RAG tự sinh được citation-ID. |
| **14** | `14_failure_archetypes.tex` | **11:00 – 12:05** | 65s | **Empirical Failure Modes: 5 Representative Cases** | **Tuấn Lĩnh** | Bảng 5 ca lỗi: Q07 (Missing retrieval), Q01 (Distractor), Q05 (Omission), Q13 (Table column C1/C5), Q19 (Citation). |
| **15** | `15_discussion_hallucination.tex` | **12:05 – 12:55** | 50s | **Discussion: Does RAG Eliminate Hallucinations?** | **Tuấn Lĩnh** | Khẳng định: KHÔNG. RAG giải quyết knowledge gap nhưng dịch chuyển lỗi sang pipeline; đối chiếu Schneider/RAGTruth. |
| **16** | `16_limitations.tex` | **12:55 – 13:45** | 50s | **Limitations \& Applicability Boundaries** | **Tuấn Lĩnh** | 5 giới hạn: mẫu 20 câu, 51 trang/29 trang OCR, chấm GPT non-blind, mô hình 1.5B, chi phí context 2.7k–3.2k tokens. |
| **17** | `17_verification_maintenance.tex` | **13:45 – 14:30** | 45s | **Proposed Improvements: Verification \& Maintenance** | **Tuấn Lĩnh** | Đề xuất GenXAI Verification Loop (tuple Claim-Condition-Chunk-Quote) & Chuẩn hóa bảng biểu, version registry. |
| **18** | `18_conclusions.tex` | **14:30 – 14:55** | 25s | **Conclusions \& Core Takeaways** | **Tuấn Lĩnh** | 4 đúc kết: 50\% lift, BM25 vs BGE-M3, Hit 95\% không đủ, thông điệp cốt lõi: Cần Verification Loop. |
| **19** | `19_references.tex` | **14:55 – 14:58** | 03s | **Key References** | **Tuấn Lĩnh** | Trích dẫn Lewis (2020), Schneider (2024), BGE-M3, Qwen2.5, Quy chế HCMUS, Link mã nguồn GitHub. |
| **20** | `20_qa.tex` | **14:58 – 15:00** | 02s | **Thank You \& Q\&A** | **Tuấn Lĩnh** | Cảm ơn và mở đầu phiên Q&A 5 phút, nêu phân công lĩnh vực trả lời của 3 thành viên. |
| -- | -- | **15:00 – 20:00** | 5:00 | **Phiên Hỏi \& Đáp (Q\&A)** | **Cả 3 thành viên** | Trả lời bảo vệ kỹ thuật trước Giảng viên và Hội đồng (Q01–Q15 theo phân công). |

---

## 3. Chiến lược Quản lý Tốc độ & Pacing Checkpoints

- **Nguyên tắc "Đèn vàng" (Pacing Checkpoints):**
  - **Mốc 04:15:** Nếu Nam Kiệt chưa vào slide 7 (Ví dụ số), phải bỏ qua các phân tích phụ của slide 6, nêu ngay kết quả Sequence $0.5280$ vs Token $0.4692$ và bàn giao đúng 04:55.
  - **Mốc 08:50:** Nếu Lê Huy chưa qua slide 12 (Worked example output), tập trung ngay vào độ tương phản cốt lõi giữa Baseline (ảo giác) vs RAG (phân biệt thi đạt vs học tập) và bàn giao đúng 09:55.
  - **Mốc 14:30:** Tuấn Lĩnh bắt đầu slide 18 (Conclusions), chốt câu thông điệp cốt lõi và kết thúc lời thuyết trình ở 14:55, không để bị chuông báo hết giờ ngắt ngang.
- **Phân bổ Trách nhiệm Q&A (15:00 – 20:00):**
  - **Trịnh Võ Nam Kiệt:** Nền tảng lý thuyết, phương trình RAG-Sequence/Token, giải thích các thuật toán Retrieval (`Q02–Q04, Q07`).
  - **Trần Đăng Lê Huy:** Corpus HCMUS, kỹ thuật chunking, thiết kế benchmark, định nghĩa và phân tích chỉ số retrieval (`Q05–Q06, Q08–Q11, Q14`).
  - **Bùi Trọng Tuấn Lĩnh:** Đánh giá chất lượng sinh ngữ, cơ chế citation, 5 ca lỗi thực tế, hiện tượng hallucination, giải pháp hậu kiểm GenXAI (`Q01, Q12–Q13, Q15`).

---

## 4. Chi tiết Từng Slide: Nội dung Hiển thị & Kịch bản Diễn giả

### Phần 1: Lý thuyết Nền tảng & Mô hình Xác suất (00:00 – 05:00)
**Diễn giả:** Trịnh Võ Nam Kiệt (`24125013`)

#### Slide 1: Title Page (`01_title.tex` | 00:00 – 00:35 | 35 giây)
- **On-Slide Content (English):**
  - Box Title: `[S07] Retrieval-Augmented Generation (RAG)`
  - Subtitle: `Grounding LLM Responses in Documents: An Empirical Study on HCMUS Regulatory Data`
  - Presenters: `Trịnh Võ Nam Kiệt (24125013) · Trần Đặng Lê Huy (24125057) · Bùi Trọng Tuấn Lĩnh (24125066)`
  - Institution: `Faculty of Information Technology, University of Science, VNU-HCM | CS420 — Intro to AI`
- **Kịch bản Diễn giả (Tiếng Việt):**
  > "Kính thưa Thầy và các bạn, nhóm em xin phép trình bày đề tài seminar S07: Retrieval-Augmented Generation — RAG. Nghiên cứu của nhóm em kết hợp giữa lý thuyết mô hình hóa xác suất nền tảng của Lewis và cộng sự tại NeurIPS 2020 với việc đo lường thực nghiệm độc lập trên toàn bộ 4 văn bản quy chế đào tạo thực tế của Trường Đại học Khoa học Tự nhiên. Bài thuyết trình được chia đều 5 phút cho 3 thành viên: em là Nam Kiệt, tiếp theo là bạn Lê Huy và bạn Tuấn Lĩnh."

#### Slide 2: Outline Roadmap (`02_outline.tex` | 00:35 – 01:00 | 25 giây)
- **On-Slide Content (English):**
  1. `Theoretical Foundation & Modeling (Speaker 1: Nam Kiet, 00:00 - 05:00)`
  2. `HCMUS Corpus & Retrieval Evaluation (Speaker 2: Le Huy, 05:00 - 10:00)`
  3. `Answer Quality, Failure Analysis & Verification (Speaker 3: Tuan Linh, 10:00 - 15:00)`
  - Footnote: `CS420 Seminar S07: 15-minute presentation balanced across 3 team members + 5-minute Q&A.`
- **Kịch bản Diễn giả (Tiếng Việt):**
  > "Nội dung bài báo cáo gồm 3 phần trọng tâm: Phần 1, em sẽ trình bày bản chất bộ nhớ, kiến trúc pipeline và phương trình toán học RAG-Sequence, RAG-Token. Phần 2, bạn Lê Huy sẽ công bố kết quả thực nghiệm đối soát 3 mô hình retrieval và worked example thực tế. Phần 3, bạn Tuấn Lĩnh sẽ mổ xẻ chất lượng sinh ngữ qua 80 câu trả lời, phân tích 5 ca lỗi thực tế và đề xuất cơ chế hậu kiểm GenXAI."

#### Slide 3: Introduction & Guiding Question (`03_intro_question.tex` | 01:00 – 01:50 | 50 giây)
- **On-Slide Content (English):**
  - Heading: `Does providing external documents eliminate hallucinations?`
  - Bullets:
    - `▪ Parametric Memory Limits: LLM weights encode knowledge statically, leading to factual hallucinations, cut-off staleness, and unverified assertions.`
    - `▪ Non-Parametric Grounding: An external document index provides modular, updatable, and inspectable evidence for factual verification.`
    - `▪ The Core Research Question: Does conditioning generation on retrieved passages eliminate hallucinations, or does it shift error points to the retrieval pipeline?`
    - `▪ Seminar Objective: Combine probabilistic modeling (Lewis et al., 2020) with an empirical audit on 4 official HCMUS academic regulations.`
  - Footnote: `Lewis et al. (NeurIPS 2020), §1; Schneider (2024), GenXAI, §1.`
- **Kịch bản Diễn giả (Tiếng Việt):**
  > "Điểm yếu lớn nhất của các mô hình ngôn ngữ lớn hiện nay là Parametric Memory — toàn bộ tri thức được nén tĩnh trong ma trận trọng số. Điều này gây ra ảo giác (hallucination), lỗi thời theo thời gian và hoàn toàn không thể truy vết bằng chứng. RAG ra đời nhằm bổ sung Non-parametric Memory — một kho tài liệu bên ngoài có thể cập nhật nóng mà không cần huấn luyện lại. Tuy nhiên, câu hỏi nghiên cứu cốt lõi mà nhóm em đặt ra là: Liệu việc cung cấp tài liệu bên ngoài có thực sự triệt tiêu được ảo giác, hay nó chỉ dịch chuyển sai số sang các khâu trong pipeline? Nhóm em sẽ trả lời trực diện câu hỏi này thông qua dữ liệu thực nghiệm."

#### Slide 4: Knowledge Grounding Paradigms (`04_paradigms.tex` | 01:50 – 02:40 | 50 giây)
- **On-Slide Content (English):**
  - Table:
    | Paradigm | Operating Mechanism | Latency / Compute | Knowledge Update |
    | :--- | :--- | :--- | :--- |
    | Fine-Tuning | Updates parametric neural weights | High training cost | Requires retraining |
    | Long-Context | Appends all source text into prompt | Quadratic token cost | Dynamic per query |
    | RAG (Hybrid) | Pairs top-k retrieval with LLM generation | Bounded context cost | Hot-swappable index |
  - Bullets:
    - `▪ Decoupled Architecture: Parametric model acts as a language synthesizer; non-parametric index acts as the verifiable knowledge store.`
    - `▪ Efficiency & Precision: Mitigates "Lost-in-the-Middle" phenomena and context dilution by filtering large corpora into top-k evidence.`
    - `▪ Lewis et al. Finding: RAG-Sequence achieved 44.5 Exact Match on Natural Questions, outperforming a 50x larger parametric T5-11B model (36.6).`
  - Footnote: `Lewis et al. (NeurIPS 2020), Table 1; Liu et al. (2024), TACL.`
- **Kịch bản Diễn giả (Tiếng Việt):**
  > "Để neo kiến thức cho mô hình, có 3 phương pháp tiếp cận chính. Fine-tuning can thiệp trực tiếp vào trọng số nhưng tốn kém GPU và có nguy cơ quên thảm họa (catastrophic forgetting). Long-context đưa toàn bộ tài liệu vào prompt nhưng chi phí token tăng theo cấp số nhân và dễ mắc hiện tượng 'Lost-in-the-Middle'. RAG là giải pháp dung hòa tối ưu: tách biệt nhiệm vụ sinh ngữ cho LLM và lưu trữ tri thức cho Retriever. Trong bài báo gốc của Lewis (2020), RAG đạt 44.5 điểm Exact Match trên tập Natural Questions, vượt trội hoàn toàn so với mô hình thuần tham số T5-11B có kích thước lớn gấp 50 lần."

#### Slide 5: RAG Pipeline & Failure Points (`05_pipeline.tex` | 02:40 – 03:30 | 50 giây)
- **On-Slide Content (English):**
  - Flow: `1. Ingestion` $\to$ `2. Chunking` $\to$ `3. Indexing` $\to$ `4. Retrieval` $\to$ `5. Augment` $\to$ `6. Generation`
  - Bullets:
    - `▪ Pre-Retrieval Failure Points: OCR noise on scanned documents; premature text splits detaching qualifying exceptions from primary articles.`
    - `▪ Retrieval Failure Points: False negative omissions (gold threshold clauses rank outside top-k); lexical distractor confusion.`
    - `▪ Post-Retrieval Failure Points: Context distraction; condition omission; table column misreading; failure to produce verifiable citation IDs.`
  - Footnote: `Adapted from Lewis et al. (2020), Figure 1; CS420 S07 Report §4.2, Figure 1.`
- **Kịch bản Diễn giả (Tiếng Việt):**
  > "Hệ thống RAG chuẩn mực vận hành qua 6 công đoạn tuần tự. Điều quan trọng là lỗi có thể phát sinh ở từng mắt xích: Ở khâu Ingestion và Chunking, việc quét OCR lỗi hoặc cắt ngang văn bản pháp lý sẽ làm đứt rời điều kiện ngoại lệ khỏi điều khoản chính. Ở khâu Retrieval, mô hình có thể bỏ sót bằng chứng hoặc bị đánh lừa bởi các đoạn văn trùng từ khóa bề mặt. Ở khâu Generation, dù có bằng chứng trong prompt, LLM vẫn có thể đọc lệch cột bảng biểu, bỏ qua điều kiện phụ hoặc trích dẫn nguồn giả. Đây chính là nguồn gốc của các ca ảo giác dạng mới."

#### Slide 6: Probabilistic Modeling: Sequence vs. Token (`06_formulation.tex` | 03:30 – 04:15 | 45 giây)
- **On-Slide Content (English):**
  - `1. RAG-Sequence (Sequence-Level Marginalization):`
    $$p_{\mathrm{Seq}}(y \mid x) \approx \sum_{z \in \mathrm{top-}k} p_\eta(z \mid x) \prod_{i=1}^{T} p_\theta(y_i \mid x, z, y_{<i})$$
  - `2. RAG-Token (Token-Level Step Marginalization):`
    $$p_{\mathrm{Tok}}(y \mid x) \approx \prod_{i=1}^{T} \left[ \sum_{z \in \mathrm{top-}k} p_\eta(z \mid x) p_\theta(y_i \mid x, z, y_{<i}) \right]$$
  - Bullets:
    - `▪ Latent Passage (z): Retrieved documents act as latent variables marginalized across top-k candidates.`
    - `▪ Sequence Formulation: Generates entire response y from a single document z; preserves topic coherence.`
    - `▪ Token Formulation: Dynamically switches documents across tokens; ideal for synthesizing multi-source facts.`
    - `▪ Variables: x: query; y_{<i}: generated prefix; η, θ: retriever/generator parameters; p in [0, 1].`
  - Footnote: `Lewis et al. (NeurIPS 2020), §2.1, Equations (1)–(2).`
- **Kịch bản Diễn giả (Tiếng Việt):**
  > "Về mặt toán học, Lewis và cộng sự mô hình hóa tài liệu truy xuất z như một biến ẩn (latent variable) được lấy cận biên trên Top-k đoạn văn. Sự khác biệt cốt lõi nằm ở vị trí của phép lấy tích và tổng: RAG-Sequence điều kiện hóa toàn bộ chuỗi đáp án y trên cùng một tài liệu z rồi mới lấy tổng xác suất, giúp câu trả lời thống nhất một văn phong. Ngược lại, RAG-Token cho phép hoán đổi tài liệu tham chiếu tại từng token sinh ra, rất phù hợp khi cần tổng hợp nhiều dữ kiện từ các tài liệu khác nhau."

#### Slide 7: Worked Numerical Example ($k=2, T=2$) (`07_numerical_example.tex` | 04:15 – 05:00 | 45 giây)
- **On-Slide Content (English):**
  - Table:
    | Passage (z) | Retriever Weight $p_\eta(z \mid x)$ | $p_\theta(a \mid x, z)$ | $p_\theta(b \mid x, z, a)$ |
    | :--- | :---: | :---: | :---: |
    | $z_1$ | 0.70 | 0.80 | 0.90 |
    | $z_2$ | 0.30 | 0.40 | 0.20 |
  - Calculations:
    - `▪ RAG-Sequence Calculation:` $p_{\mathrm{Seq}} = 0.70 \times (0.80 \times 0.90) + 0.30 \times (0.40 \times 0.20) = 0.5040 + 0.0240 = \mathbf{0.5280}$
    - `▪ RAG-Token Calculation:` $p_{\mathrm{Tok}} = (0.70 \times 0.80 + 0.30 \times 0.40) \times (0.70 \times 0.90 + 0.30 \times 0.20) = 0.6800 \times 0.6900 = \mathbf{0.4692}$
    - `▪ Operator Inversion: The discrepancy (0.5280 vs. 0.4692) reflects the non-commutativity of \sum and \prod.`
    - `▪ Implementation Distinction: Modern instruction-tuned QA (e.g., Qwen) performs prompt conditioning rather than explicit marginalization.`
  - Footnote: `CS420 S07 Report §3.2, Table 1. Probabilities parameterized to demonstrate mathematical formulation.`
- **Kịch bản Diễn giả (Tiếng Việt):**
  > "Để minh họa trực quan, nhóm giả định truy xuất được k=2 đoạn văn với trọng số 0.70 và 0.30 để sinh 2 token a và b. Dưới mô hình RAG-Sequence, xác suất chuỗi đạt 0.5280. Nhưng dưới mô hình RAG-Token, giá trị này chỉ là 0.4692. Độ lệch này sinh ra do tính không giao hoán giữa phép cộng và phép nhân. Cần lưu ý rằng các hệ thống QA hiện đại như Qwen thực hiện ghép prompt thay vì tính cận biên chính xác. Để kiểm chứng lý thuyết trên văn bản thực tế, bạn Lê Huy sẽ trình bày phần thực nghiệm quy chế HCMUS."

---

### Phần 2: Thiết lập Thực nghiệm & Worked Example Thực tế (05:00 – 10:00)
**Diễn giả:** Trần Đăng Lê Huy (`24125057`)

#### Slide 8: Experimental Corpus: HCMUS Regulations (`08_corpus.tex` | 05:00 – 05:55 | 55 giây)
- **On-Slide Content (English):**
  - Table:
    | ID | Regulatory Document Title and Reference | Scope | Pages |
    | :--- | :--- | :--- | :---: |
    | D01 | Undergraduate Academic Regulations 2026 (Dec. 3087/QĐ-KHTN) | Academic Rules | 21 |
    | D02 | Student Conduct Assessment 2020 & Amendment 2023 | Conduct Scoring | 16 |
    | D03 | Tuition Fee Rates AY 2026–2027 (Dec. 3317/QĐ-KHTN) | Fees (K2022+) | 5 |
    | D04 | Foreign Language Graduation Standards (Dec. 2464/QĐ-KHTN) | Exit Standards | 9 |
    | **Total** | **Authoritative four-document regulatory snapshot** | **PDF Corpus** | **51** |
  - Bullets:
    - `▪ Corpus Scale: 51 pages segmented into 80 parent sections and 162 chunks under an 800-token ceiling (cl100k_base).`
    - `▪ Evaluation Benchmark: 20 administrative queries mapped to 30 gold evidence groups (held out from indexing).`
    - `▪ Metadata Preservation: Articles, PDF page numbers, cohort scopes, and table footnotes injected into chunk headers.`
    - `▪ Scope Distinction: Exceeds standard 5–10 page guideline to test real-world administrative cross-referencing.`
  - Footnote: `CS420 S07 Report §4.1, Table 2. Verified against official HCMUS portals (commit 3bb5f3a).`
- **Kịch bản Diễn giả (Tiếng Việt):**
  > "Kính thưa Thầy, bước sang phần thực nghiệm, nhóm em xây dựng bộ ngữ liệu gồm 4 văn bản quy chế chính thức của Trường ĐH Khoa học Tự nhiên: Quy chế đào tạo 2026, Quy chế điểm rèn luyện, Định mức học phí và Chuẩn ngoại ngữ tốt nghiệp. Tổng quy mô là 51 trang văn bản pháp lý — mở rộng hơn so với gợi ý 5–10 trang của đề bài để thử thách khả năng định vị điều khoản chéo. Tài liệu được cấu trúc thành 80 điều mục và chia thành 162 chunks với trần 800 token. Bộ benchmark gồm 20 câu hỏi đi kèm 30 nhóm bằng chứng vàng được tách biệt hoàn toàn khỏi chỉ mục tìm kiếm."

#### Slide 9: Retrieval Setup & Protocol (`09_retrieval_setup.tex` | 05:55 – 06:45 | 50 giây)
- **On-Slide Content (English):**
  - Table:
    | Retriever | Type | Representation | Hyperparameters |
    | :--- | :--- | :--- | :--- |
    | TF-IDF | Sparse Lexical | Unigram + bigram frequencies | Sublinear TF, cosine distance |
    | BM25 | Sparse Lexical | Term frequency saturation & length penalty | Vietnamese tokens, $k_1=1.5, b=0.75$ |
    | BGE-M3 | Dense Neural | 1024-dim multilingual dense embeddings | Normalized vectors, cosine similarity |
  - Bullets:
    - `▪ Evaluation Metrics (Macro-averaged across 20 queries, 30 gold evidence groups):`
      - `Evidence Recall@k: Fraction of necessary gold evidence groups retrieved (r/m).`
      - `Hit Rate@k: Binary indicator if at least one gold evidence group is found (r >= 1).`
      - `All Evidence Hit@k: Binary indicator if all gold evidence groups are retrieved (r = m).`
      - `MRR@k: Reciprocal rank of the first relevant evidence chunk (0 if not in top-k).`
    - `▪ Benchmark Cut-offs: Evaluated at k in {1, 3, 5} to compare early precision vs. multi-hop recall.`
  - Footnote: `CS420 S07 Report §4.1; Retrieval evaluation scripts at commit 5771d80.`
- **Kịch bản Diễn giả (Tiếng Việt):**
  > "Nhóm triển khai thực nghiệm so sánh độc lập 3 mô hình retrieval: TF-IDF (từ khóa thưa), BM25 (có bão hòa tần suất từ và chuẩn hóa độ dài văn bản với k1=1.5, b=0.75), và Dense BGE-M3 (nhúng vector ngữ nghĩa 1024 chiều). Về chỉ số đánh giá, nhóm phân biệt rạch ròi giữa: Hit Rate@k (tìm thấy ít nhất 1 bằng chứng), Evidence Recall@k (tỷ lệ bằng chứng tìm được trên tổng số bằng chứng bắt buộc), All Evidence Hit@k (tìm đủ 100% bằng chứng của câu hỏi) và MRR@k (thứ hạng nghịch đảo). Cả 3 phương pháp được đo lường đồng bộ tại k = 1, 3 và 5."

#### Slide 10: Experiment 1: Retrieval Performance (`10_retrieval_results.tex` | 06:45 – 07:45 | 60 giây)
- **On-Slide Content (English):**
  - Table:
    | Retriever | Recall@1 | Recall@3 | Recall@5 | Hit@5 | All Evidence@5 | MRR@5 |
    | :--- | :---: | :---: | :---: | :---: | :---: | :---: |
    | TF-IDF | 70.83% | 82.50% | 82.50% | 90.00% | 15/20 | 0.8250 |
    | BM25 | **80.00%** | **84.17%** | 84.17% | 90.00% | **16/20** | **0.8667** |
    | BGE-M3 | 65.00% | 81.67% | **89.17%** | **95.00%** | **16/20** | 0.7867 |
  - Bullets:
    - `▪ Early Precision (BM25): BM25 dominates top-1 ranking (Recall@1 = 80.00%) via exact lexical matching of regulatory terms.`
    - `▪ High-Cutoff Coverage (BGE-M3): Dense embeddings lead at k=5 (Recall@5 = 89.17%, Hit@5 = 95.00%) by capturing semantic paraphrases.`
    - `▪ Plateau Effect: Lexical methods saturate at k=3, whereas BGE-M3 gains +7.50 percentage points expanding from k=3 to k=5.`
    - `▪ Crucial Takeaway: Hit@5 = 95.00% does NOT imply 95% answer accuracy! Downstream generation bottlenecks persist.`
  - Footnote: `CS420 S07 Report §5, Table 4. Evaluated on 20 queries, 30 gold evidence groups (commit 5771d80).`
- **Kịch bản Diễn giả (Tiếng Việt):**
  > "Nhìn vào bảng kết quả Table 4, ta thấy sự phân hóa rất rõ giữa hai trường phái: BM25 thống trị về độ chính xác ở Top-1 với Recall@1 đạt 80.00% và MRR@5 đạt 0.8667 nhờ khớp chuẩn xác các mã hiệu điều luật và thuật ngữ hành chính. Ngược lại, Dense BGE-M3 thể hiện ưu thế bao phủ ngữ nghĩa vượt trội ở ngưỡng k=5 với Recall@5 đạt 89.17% và Hit@5 đạt 95.00%. Đáng chú ý, các phương pháp từ khóa bị bão hòa hoàn toàn khi tăng từ k=3 lên k=5, trong khi BGE-M3 tăng thêm 7.5%. Tuy nhiên, kết luận phản biện then chốt ở đây là: Hit@5 đạt 95% KHÔNG ĐỒNG NGHĨA câu trả lời sinh ra đạt độ chính xác 95%!"

#### Slide 11: Worked Example (Q01): Top-5 Candidate Chunks (`11_worked_example_retrieval.tex` | 07:45 – 08:50 | 65 giây)
- **On-Slide Content (English):**
  - Prompt: `Benchmark Query (Q01): According to the 2026 Academic Regulations, how does a prerequisite course differ from a pre-learning course?`
  - Table:
    | Rank | Chunk Identifier | Cosine | Page | Content Summary and Regulatory Scope |
    | :---: | :--- | :---: | :---: | :--- |
    | **1** | `D01_regulation_article_3_03` | **0.6271** | 4 | **Gold Evidence:** Article 3, Clause 3(c) (Both definitions) |
    | 2 | `D01_regulation_article_27_01` | 0.5813 | 21 | Article 27: Transitional clauses for earlier cohorts |
    | 3 | `D01_regulation_article_3_02` | 0.5704 | 3 | Article 3, Clause 2: Elective and general course definitions |
    | 4 | `D01_regulation_article_6_02` | 0.5643 | 7 | Article 6: Semester scheduling and course limits |
    | 5 | `D01_regulation_article_18_02` | 0.5540 | 16 | Article 18: Credit exemptions and transfer guidelines |
  - Bullets:
    - `▪ Successful Top-1 Alignment: Rank-1 passage provides 100% of required gold evidence for both course concepts.`
    - `▪ Crucial Regulatory Distinction: Prerequisite requires "passing" the exam; pre-learning only requires "completing the coursework".`
    - `▪ Distractor Risk: Ranks 2–5 introduce adjacent credit/scheduling rules that risk inducing model confusion.`
  - Footnote: `CS420 S07 Report §4.2, Table 3. Dense ranking log from retrieval_hits.json.`
- **Kịch bản Diễn giả (Tiếng Việt):**
  > "Nhóm lấy câu hỏi Q01 làm ví dụ phân tích chi tiết: 'Theo Quy chế 2026, học phần tiên quyết khác học phần học trước như thế nào?'. BGE-M3 đã truy xuất xuất sắc khi đưa đúng đoạn chunk Điều 3 Khoản 3(c) lên Hạng 1 với Cosine Similarity là 0.6271 tại trang PDF số 4. Đoạn văn này chứa đầy đủ định nghĩa vàng: Tiên quyết bắt buộc sinh viên phải 'thi đạt', trong khi Học trước chỉ yêu cầu 'hoàn thành quá trình học tập'. Tuy nhiên, các vị trí từ Hạng 2 đến Hạng 5 lại chứa các điều khoản chuyển tiếp và miễn trừ tín chỉ, tạo thành các đoạn gây nhiễu ngữ cảnh (distractors)."

#### Slide 12: Worked Example (Q01): Grounded vs. Baseline Output (`12_worked_example_generation.tex` | 08:50 – 10:00 | 70 giây)
- **On-Slide Content (English):**
  - Table:
    | Configuration | Score | Generated Response Content & Attribution |
    | :--- | :---: | :--- |
    | Baseline (No RAG) | 0 / 2 | Hallucinates generic academic progression; falsely claims both course types require passing grades; lacks any regulatory citation. |
    | Grounded RAG (BGE-M3) | **2 / 2** | Correctly states prerequisite requires **"passing"** (thi đạt), while pre-learning only requires **"completing the study process"**. [D01_regulation_article_3_03]* |
  - Bullets:
    - `▪ Prompt Augmentation: Context injected under structured SOURCES block with chunk IDs, article titles, and page numbers.`
    - `▪ Factual Grounding Contrast: Parametric memory guesses incorrectly; RAG context enables precise legal differentiation.`
    - `▪ *Human Attribution Caveat: Qwen generated the correct text but failed to emit the citation ID; the reference tag was verified and added post-hoc by human auditors.`
  - Footnote: `CS420 S07 Report §4.2; Task 6 answer comparison logs. *Citation verified and appended during human audit.`
- **Kịch bản Diễn giả (Tiếng Việt):**
  > "Khi đưa vào mô hình ngôn ngữ Qwen2.5-1.5B, sự tương phản là tuyệt đối. Nhánh Baseline không có tài liệu đạt 0/2 điểm: mô hình suy diễn cảm tính và khẳng định sai lệch rằng cả hai môn đều phải thi đạt trên trung bình. Trong khi đó, nhánh Grounded RAG đạt trọn vẹn 2/2 điểm khi nêu chính xác sự khác biệt pháp lý giữa 'thi đạt' và 'hoàn thành quá trình học tập'. Tuy nhiên, một lưu ý học thuật quan trọng: mô hình Qwen sinh đúng nội dung nhưng không tự xuất được mã trích dẫn; mã [D01_regulation_article_3_03] trên slide là do nhóm đối chiếu và bổ sung thủ công. Dù Q01 thành công, hệ thống vẫn tồn tại nhiều lỗi tinh vi. Xin mời bạn Tuấn Lĩnh phân tích các failure cases thực tế."

---

### Phần 3: Phân tích Lỗi, Thảo luận Phản biện & Cải tiến (10:00 – 15:00)
**Diễn giả:** Bùi Trọng Tuấn Lĩnh (`24125066`)

#### Slide 13: Experiment 2: 4-Way Answer Quality (`13_generation_quality.tex` | 10:00 – 11:00 | 60 giây)
- **On-Slide Content (English):**
  - Table:
    | Configuration | Fully Correct | Partial | Incorrect | Unsupported | Valid Citations |
    | :--- | :---: | :---: | :---: | :---: | :---: |
    | Baseline (No RAG) | 0/20 (0.0%) | 3/20 (15.0%) | 17/20 (85.0%) | 15/20 (75.0%) | 0/20 (0.0%) |
    | RAG (TF-IDF) | **10/20 (50.0%)** | 5/20 (25.0%) | 5/20 (25.0%) | 8/20 (40.0%) | 0/20 (0.0%) |
    | RAG (BM25) | 9/20 (45.0%) | 6/20 (30.0%) | 5/20 (25.0%) | 7/20 (35.0%) | 0/20 (0.0%) |
    | RAG (BGE-M3) | **10/20 (50.0%)** | 6/20 (30.0%) | 4/20 (20.0%) | **6/20 (30.0%)** | 0/20 (0.0%) |
  - Highlight: `+45.0 to +50.0 pp accuracy gain over unaugmented baseline (0% -> 50%)`
  - Bullets:
    - `▪ Recall != Accuracy Bottleneck: Despite higher Evidence Recall@5 (89.17%), BGE-M3 ties with TF-IDF at 50% accuracy.`
    - `▪ Significant Hallucination Drop: Unsupported claims decrease from 75% in baseline to 30% in BGE-M3 and 35% in BM25.`
    - `▪ Universal Citation Blindness: All 60 RAG answers omitted formal citation tags despite explicit prompt constraints.`
  - Footnote: `CS420 S07 Report §5, Table 5. Evaluated on Qwen2.5-1.5B-Instruct across 80 completions (commit 3bb5f3a).`
- **Kịch bản Diễn giả (Tiếng Việt):**
  > "Kính thưa Thầy, bước sang phần đánh giá chất lượng sinh ngữ trên 80 câu trả lời của Task 6. Kết quả cho thấy RAG tạo ra bước nhảy vọt: nâng tỷ lệ đúng nội dung chính từ 0% ở Baseline lên mức 45% đến 50%, đồng thời kéo giảm tỷ lệ phát biểu sai từ 75% xuống còn 30%. Tuy nhiên, có hai phát hiện thực nghiệm then chốt: Thứ nhất, dù BGE-M3 có Recall@5 đạt tới 89.17%, độ chính xác cuối cùng của nó vẫn chỉ dừng ở 50% (ngang bằng TF-IDF). Thứ hai, toàn bộ 60 câu trả lời RAG của mô hình Qwen đều thất bại trong việc tự sinh mã citation-ID hợp lệ, dù hệ thống đã ép khuôn chỉ dẫn rất chặt chẽ."

#### Slide 14: Empirical Failure Modes: 5 Representative Cases (`14_failure_archetypes.tex` | 11:00 – 12:05 | 65 giây)
- **On-Slide Content (English):**
  - Table:
    | Query | Observed Prompt and Generation Behavior | Root Cause and Remediation Stage |
    | :---: | :--- | :--- |
    | **Q07** | Top-5 misses the 65–79 score band chunk. BGE-M3 fabricates "Average 50 points" for a 68-point score. | **Retrieval Omission:** Gold threshold missing; model guesses parametrically. |
    | **Q01** | Correct definition ranks 1. TF-IDF/BM25 rank English prerequisite at rank 2, derailing output focus. | **Distractor Interference:** Lexical match confuses cross-attention context. |
    | **Q05** | Model receives Article 19 but asserts credit completion alone suffices for graduation. | **Condition Pruning:** Generator overlooks secondary administrative rules. |
    | **Q13** | All retrievers capture tuition table. Model reads column C1 (488k) instead of C5 (1,014k vs. 974k). | **Tabular Misalignment:** 1.5B LLM struggles with row-column intersections. |
    | **Q19** | Model captures valid deadlines but fabricates a non-existent decision suffix identifier. | **Metadata Hallucination:** Generates plausible-sounding official numbers. |
  - Bullets:
    - `▪ Comprehensive Distribution: Failures occur across retrieval (Q07, Q01), reasoning (Q05), tables (Q13), and citations (Q19).`
    - `▪ High Risk of Structured Data: Multi-column tables and multi-condition checklists require specialized extraction pipelines.`
  - Footnote: `CS420 S07 Report §6, Table 6. Case analysis from 80-answer generation logs (commit 3bb5f3a).`
- **Kịch bản Diễn giả (Tiếng Việt):**
  > "Nhóm đã mổ xẻ log và phân loại 5 ca lỗi điển hình đại diện cho các mắt xích pipeline: Tại Q07, bằng chứng khung điểm rèn luyện Khá nằm ngoài Top-5 khiến mô hình tự suy diễn thành 50 điểm (Lỗi Retrieval). Tại Q01, đoạn văn về chuẩn tiếng Anh làm lệch hướng sinh ngữ của TF-IDF/BM25 (Lỗi Distractor). Tại Q05, mô hình nhận đủ Điều 19 nhưng tự ý cắt gọt, chỉ nêu số tín chỉ mà bỏ sót điều kiện kỷ luật và chuẩn ngoại ngữ (Lỗi Generator). Tại Q13, mô hình đọc lệch cột bảng học phí: lấy cột C1 thay vì C5 dẫn đến kết luận chênh lệch 0 đồng (Lỗi Bảng biểu). Và tại Q19, mô hình tự bịa ra số hiệu quyết định không có thật (Lỗi Trích dẫn)."

#### Slide 15: Discussion: Does RAG Eliminate Hallucinations? (`15_discussion_hallucination.tex` | 12:05 – 12:55 | 50 giây)
- **Hiệu ứng Trình chiếu (Click Overlays):** Chia làm 3 phần xuất hiện dần dần qua 3 lần click:
  - *Click 1 (Part 1):* Câu hỏi nghiên cứu định hướng & Kết luận trực diện in đậm:
    - Question: `Does providing external documents eliminate hallucinations?`
    - Verdict: `NO. RAG transforms the nature and origin of hallucinations.`
  - *Click 2 (Part 2):* Bản chất chuyển dịch lỗi & Ngụy biện về ngữ cảnh:
    - `▪ Paradigm Shift in Errors: RAG resolves the parametric knowledge deficit (jumping from 0% to 50% accuracy), but introduces pipeline-dependent vulnerabilities.`
    - `▪ The Grounding Fallacy: Supplying relevant documents is a necessary condition, but not a sufficient condition to guarantee factual truthfulness.`
  - *Click 3 (Part 3):* Các sai số tích lũy & Đối chiếu y văn:
    - `▪ Cascading Pipeline Errors: Hallucinations now emerge from retrieval omissions, adjacent distractors, condition pruning, and tabular distortion.`
    - `▪ Literature Corroboration: Aligns with Schneider (2024, GenXAI) and Niu et al. (ACL 2024, RAGTruth): LLMs frequently assert ungrounded claims despite prompt grounding.`
  - Footnote: `Schneider (2024), GenXAI, §1–§2; Niu et al. (ACL 2024), RAGTruth; CS420 S07 Report §1, §6.`
- **Kịch bản Diễn giả (Tiếng Việt):**
  > "Quay trở lại câu hỏi nghiên cứu định hướng: Cung cấp tài liệu bên ngoài có triệt tiêu hoàn toàn ảo giác không? Câu trả lời dứt khoát là: KHÔNG. RAG giải quyết triệt để sự thiếu hụt kiến thức tĩnh, nhưng nó làm dịch chuyển bản chất của ảo giác sang các sai số tích lũy trong pipeline. Việc cung cấp ngữ cảnh chỉ là điều kiện cần, hoàn toàn không phải điều kiện đủ để đảm bảo tính trung thực. Phát hiện thực nghiệm của nhóm hoàn toàn trùng khớp với khung lý thuyết GenXAI của Schneider (2024) và tập ngữ liệu RAGTruth (ACL 2024): mô hình vẫn thường xuyên sinh ra các khẳng định không được bảo chứng bởi tài liệu."

#### Slide 16: Limitations & Applicability Boundaries (`16_limitations.tex` | 12:55 – 13:45 | 50 giây)
- **On-Slide Content (English):**
  - Bullets:
    - `▪ Benchmark Sample Size: 20 curated administrative queries; a single outcome change shifts performance by 5.0 percentage points (requires cautious statistical interpretation).`
    - `▪ Corpus Scope: 51 pages across 4 documents from a single university; 29 pages OCR-processed without complete token-level human audit.`
    - `▪ Evaluation Methodology: Correctness scores were assigned via automated GPT-based qualitative review; double-blind human cross-annotation remains pending.`
    - `▪ Generator Scale: Evaluated on a frozen 1.5B instruction-tuned model (Qwen2.5-1.5B-Instruct); larger models (7B/72B) may better interpret complex tables.`
    - `▪ Inference Context Overhead: Top-5 RAG increases prompt tokens from 236 to 2,749–3,205 tokens (approx 12x latency and API cost increase).`
  - Footnote: `CS420 S07 Report §7. Limitations documented in accordance with seminar evaluation standards.`
- **Kịch bản Diễn giả (Tiếng Việt):**
  > "Nhóm cũng nghiêm túc nhìn nhận các giới hạn của nghiên cứu: Thứ nhất, bộ benchmark gồm 20 câu hỏi nên mỗi câu tương ứng với 5% điểm số, cần thận trọng khi khái quát hóa. Thứ hai, 29 trang tài liệu OCR chưa được kiểm tra chéo từng ký tự. Thứ ba, bảng điểm Task 6 sử dụng hỗ trợ từ GPT nên mang tính chất sơ bộ (provisional). Thứ tư, thực nghiệm thực hiện trên mô hình nhỏ 1.5B; các mô hình lớn hơn có thể xử lý bảng biểu tốt hơn. Và cuối cùng là chi phí context: RAG làm tăng dung lượng prompt từ 236 lên hơn 3.000 tokens, tức tăng chi phí và độ trễ gấp 12 lần."

#### Slide 17: Proposed Improvements: Verification & Maintenance (`17_verification_maintenance.tex` | 13:45 – 14:30 | 45 giây)
- **On-Slide Content (English):**
  - Block 1: `1. Post-Generation Verification Loop (Schneider, 2024 — GenXAI)`
    - `Atomic Claim Decomposition: Deconstruct generated answers into verifiable tuples:`
      $$\langle\text{Claim},\ \text{Applicable Cohort},\ \text{Chunk ID},\ \text{Verbatim Quote}\rangle$$
    - `Natural Language Inference (NLI) Gate: Automatically audit entailment between claim and quote; trigger safe abstention ("Insufficient information") if ungrounded.`
  - Block 2: `2. Tabular Structuring & Regulatory Maintenance`
    - `Structured Table Parsing: Convert dense multi-column tuition matrices into explicit key-value schemas to eliminate column misalignment (as observed in Q13).`
    - `Versioned Corpus Registry: Track circulars by decision number, effective date, and SHA-256 hash; execute automated diffs to retire obsolete regulatory chunks.`
  - Footnote: `Schneider (2024), GenXAI, §3.3; CS420 S07 Report §6. Proposed architectural improvements.`
- **Kịch bản Diễn giả (Tiếng Việt):**
  > "Để khắc phục, nhóm đề xuất hai giải pháp kiến trúc: Thứ nhất là áp dụng Verification Loop theo Schneider (2024): bóc tách câu trả lời thành các tuple nguyên tử gồm luận điểm, phạm vi áp dụng, mã chunk và trích dẫn nguyên văn, sau đó dùng mô hình NLI để kiểm tra quan hệ kéo theo (entailment), chủ động từ chối nếu thiếu bằng chứng. Thứ hai là tiền xử lý bảng biểu phức tạp thành cấu trúc JSON key-value có gắn chặt tiêu đề cột, đồng thời xây dựng sổ đăng ký phiên bản với mã băm SHA-256 để tự động cập nhật vector index khi có quy chế mới ban hành."

#### Slide 18: Conclusions & Core Takeaways (`18_conclusions.tex` | 14:30 – 14:55 | 25 giây)
- **On-Slide Content (English):**
  - Bullets:
    - `▪ Substantial Accuracy Lift: RAG elevates core factual correctness from 0% in an unaugmented baseline to 45–50% on complex administrative regulations.`
    - `▪ Complementary Retrieval Roles: BM25 delivers highest top-1 precision (Recall@1 = 80.00%); BGE-M3 provides greatest aggregate coverage (Recall@5 = 89.17%).`
    - `▪ The Verification Imperative: High recall (Hit@5 = 95%) is insufficient. Generators omit conditions, confuse tables, and fail at citation IDs.`
    - `▪ Core Takeaway: Curing hallucinations requires treating retrieval, structured parsing, and post-generation claim verification as an integrated pipeline.`
  - Central Message: `External documents ground LLMs, but only rigorous verification ensures reliability.`
  - Footnote: `CS420 S07 Seminar Report, Faculty of Information Technology, HCMUS (2026).`
- **Kịch bản Diễn giả (Tiếng Việt):**
  > "Tóm lại, nghiên cứu của nhóm rút ra 3 kết luận cốt lõi: RAG nâng độ chính xác từ 0% lên 50%; BM25 mạnh về độ chính xác Top-1 còn BGE-M3 mạnh về độ phủ Top-5; và quan trọng nhất: Cung cấp tài liệu chỉ mới là một nửa chặng đường — tài liệu ngoài neo kiến thức cho mô hình, nhưng chỉ có cơ chế hậu kiểm khắt khe mới đảm bảo được sự tin cậy."

#### Slide 19 & 20: References & Q&A (`19_references.tex`, `20_qa.tex` | 14:55 – 15:00 | 5 giây)
- **On-Slide Content (English):**
  - Slide 19: Full papers (Lewis 2020, Schneider 2024, BGE-M3, Qwen2.5, HCMUS Decisions, GitHub repo).
  - Slide 20: Tối giản, tập trung (đã xóa phần phân công trách nhiệm để giao diện sạch sẽ):
    - Title: `Thank you for listening!`
    - Subtitle: `Any questions?`
- **Kịch bản Diễn giả (Tiếng Việt):**
  > "Nhóm xin chân thành cảm ơn Thầy và các bạn đã chú ý lắng nghe. Nhóm em đã sẵn sàng bước vào phiên hỏi đáp 5 phút!"

---

## 5. Bảng Phân bổ Trả lời Câu hỏi Q&A (Rubric 20 Điểm)

| STT | Câu hỏi Thường gặp & Trọng tâm Kỹ thuật | Người trả lời chính | Người dự phòng | Tài liệu căn cứ |
| :---: | :--- | :---: | :---: | :--- |
| **Q01** | Cung cấp tài liệu bên ngoài có loại bỏ hoàn toàn hallucination không? | **Tuấn Lĩnh** | Lê Huy | Bảng Table 5, Task 6 answers |
| **Q02** | Phân biệt Parametric vs Non-parametric memory? RAG khác Fine-tuning và Long-context thế nào? | **Nam Kiệt** | Tuấn Lĩnh | Lewis et al. (2020), Slide 4 |
| **Q03** | Bản chất phương trình RAG-Sequence và RAG-Token? Ví dụ số tính toán ra sao? | **Nam Kiệt** | Lê Huy | Lewis §2.1, Slide 6–7 |
| **Q04** | Nhóm có huấn luyện lại end-to-end mô hình Lewis không? Triển khai thực tế khác gì? | **Nam Kiệt** | Tuấn Lĩnh | Qwen prompt conditioning, Report §3 |
| **Q05** | Bộ dữ liệu corpus gồm những gì? Vì sao dùng 51 trang thay vì 5–10 trang theo đề? | **Lê Huy** | Tuấn Lĩnh | Table 2 Report, sources.json |
| **Q06** | Vì sao chia chunk theo cấu trúc điều khoản và đặt trần 800 token? | **Lê Huy** | Nam Kiệt | chunks_by_structure.json |
| **Q07** | Bản chất khác biệt kỹ thuật giữa TF-IDF, BM25 và BGE-M3? | **Nam Kiệt** | Lê Huy | Code retrieval, Report §4.1 |
| **Q08** | Vì sao nhóm chọn đánh giá ở k = 1, 3, 5? Đã đáp ứng yêu cầu 2 cấu hình chưa? | **Lê Huy** | Nam Kiệt | Table 4 Report, TASKS.md |
| **Q09** | Phân biệt Evidence Recall@k, Hit Rate@k, All Evidence Hit@k và MRR@k? | **Lê Huy** | Nam Kiệt | Report §4.1, retrieval_summary.csv |
| **Q10** | Giữa BM25 và BGE-M3, mô hình nào tốt hơn trên quy chế HCMUS? | **Lê Huy** | Tuấn Lĩnh | Slide 10, Table 4 & Table 5 |
| **Q11** | So sánh giữa Baseline không RAG và có RAG có đảm bảo tính công bằng không? | **Lê Huy** | Nam Kiệt | Run manifest, cùng seed/decoding |
| **Q12** | Câu trả lời đúng nội dung có đồng nghĩa với việc mô hình sinh citation đúng không? | **Tuấn Lĩnh** | Lê Huy | Table 5, 0/60 citations, Slide 12 |
| **Q13** | Nêu 3 ca lỗi thực tế điển hình và phân tích nguyên nhân gốc rễ? | **Tuấn Lĩnh** | Lê Huy | Table 6 Report, Q07, Q13, Q05, Q19 |
| **Q14** | Phương pháp đánh giá chất lượng câu trả lời của nhóm là gì? Hạn chế là gì? | **Lê Huy** | Tuấn Lĩnh | GPT qualitative review, Report §4.3 |
| **Q15** | Nếu phát triển tiếp, nhóm đề xuất giải pháp hậu kiểm và cập nhật tài liệu ra sao? | **Tuấn Lĩnh** | Nam Kiệt | GenXAI Verification Loop, Slide 17 |
