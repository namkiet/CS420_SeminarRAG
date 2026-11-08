# Dàn ý Chi tiết & Timeline Bộ Slides Thuyết trình: RAG (S07)

> **Môn học:** CS420 — Nhập môn Trí tuệ Nhân tạo | Trường ĐH Khoa học Tự nhiên, ĐHQG-HCM  
> **Chủ đề Seminar:** [S07] Retrieval-Augmented Generation (RAG): Grounding LLM Responses in Documents  
> **Quy định thời gian:** Đúng **15 phút** thuyết trình (bắt buộc cả 3 thành viên đều nói) + **5 phút** Q&A  
> **Quy mô slides:** 12 slides (10 slides nội dung trọng tâm + 1 slide bìa + 1 slide kết luận/references)  
> **Phân công diễn giả:** Cân bằng hoàn hảo 3 thành viên (**mỗi người đúng 5:00 phút**)  
> - **Speaker 1 (00:00 – 05:00):** Trịnh Võ Nam Kiệt (`24125013`)  
> - **Speaker 2 (05:00 – 10:00):** Trần Đăng Lê Huy (`24125057`)  
> - **Speaker 3 (10:00 – 15:00):** Bùi Tuấn Lĩnh  

---

## 1. Timeline Chi tiết theo Từng Phút (Minute-by-Minute Timeline)

```mermaid
gantt
    title TIMELINE THUYẾT TRÌNH SEMINAR S07 (TỔNG CỘNG 15 PHÚT)
    dateFormat mm:ss
    axisFormat %M:%S
    
    section Speaker 1: Nam Kiệt (5:00)
    Slide 1: Bìa & Khởi động           :00:00, 01:00
    Slide 2: Problem & Guiding Question :01:00, 02:15
    Slide 3: Pipeline & Failure Points   :02:15, 03:30
    Slide 4: Phương trình & Ví dụ số    :03:30, 05:00
    
    section Speaker 2: Lê Huy (5:00)
    Slide 5: Corpus & Benchmark HCMUS   :05:00, 06:00
    Slide 6: Retrieval Recall@k & MRR   :06:00, 07:30
    Slide 7: Worked Example - Top-k     :07:30, 08:45
    Slide 8: Worked Example - Generation:08:45, 10:00
    
    section Speaker 3: Tuấn Lĩnh (5:00)
    Slide 9: Phân tích 4 Ca lỗi Kaggle  :10:00, 11:30
    Slide 10: RAG vs Hallucination      :11:30, 12:45
    Slide 11: GenXAI Verification Loop  :12:45, 14:00
    Slide 12: Kết luận & Mở Q&A        :14:00, 15:00

    section Phiên Q&A (5:00)
    Cả 3 thành viên trả lời phản biện  :15:00, 20:00
```

---

## 2. Bảng Phân công, Tiến độ Thời gian & Điểm Chuyển giao (Handoff Cues)

| Mốc thời gian | Thời lượng | Slide | Tiêu đề Slide | Người trình bày | Mục tiêu & Tín hiệu chuyển giao (Handoff Cue) |
| :---: | :---: | :---: | :--- | :---: | :--- |
| **00:00 – 01:00** | 1:00 | **01** | Tiêu đề, Thành viên & Đặt vấn đề | **Nam Kiệt** | Chào hội đồng, giới thiệu 3 thành viên, định vị chủ đề S07. |
| **01:00 – 02:15** | 1:15 | **02** | Problem Statement & Guiding Question | **Nam Kiệt** | Phân tích giới hạn Parametric memory; Bảng RAG vs FT vs Prompt; Nêu Guiding Question. |
| **02:15 – 03:30** | 1:15 | **03** | RAG Pipeline & Theoretical Failure Points | **Nam Kiệt** | Sơ đồ 6 bước (`Ingestion` $\to$ `Generation`); Chỉ rõ điểm gây lỗi tại từng bước. |
| **03:30 – 04:55** | 1:25 | **04** | Phương trình RAG-Sequence & Numerical Example | **Nam Kiệt** | Công thức Lewis et al. (2020), giải thích biến ẩn $z$; Bảng tính số cụ thể với $k=2$. |
| **04:55 – 05:00** | 0:05 | -- | *[Chuyển giao 1]* | Nam Kiệt $\to$ Lê Huy | *"Để kiểm chứng mô hình toán trên dữ liệu thực tế, bạn Lê Huy sẽ trình bày phần thực nghiệm."* |
| **05:00 – 06:00** | 1:00 | **05** | Thiết lập Thực nghiệm (Corpus & Benchmark) | **Lê Huy** | 4 Quy chế HCMUS (51 trang, 162 chunks); Benchmark 20 câu hỏi & 30 gold evidence spans. |
| **06:00 – 07:30** | 1:30 | **06** | Đánh giá Retrieval (Recall@k & Hit Rate@k) | **Lê Huy** | Bảng số liệu TF-IDF vs BM25 vs Dense BGE-M3 ở $k \in \{1, 3, 5\}$. Đúc kết: Hit@5 95% $\neq$ Accuracy 95%. |
| **07:30 – 08:45** | 1:15 | **07** | Worked Example: Truy xuất Bằng chứng (Q01) | **Lê Huy** | Case study Q01: Tiên quyết vs Học trước; Top-5 chunks (Rank 1 sim = 0.8412 có gold evidence). |
| **08:45 – 09:55** | 1:10 | **08** | Worked Example: Prompt & So sánh Đáp án | **Lê Huy** | Cấu trúc Augmented Prompt; So sánh RAG (có citation chuẩn) vs Non-RAG baseline (ảo giác nặng). |
| **09:55 – 10:00** | 0:05 | -- | *[Chuyển giao 2]* | Lê Huy $\to$ Tuấn Lĩnh | *"Dù Q01 rất thành công, hệ thống vẫn tồn tại nhiều lỗi tinh vi. Xin mời bạn Tuấn Lĩnh phân tích các failure cases."* |
| **10:00 – 11:30** | 1:30 | **09** | Phân tích 4 Ca lỗi Thực nghiệm (Kaggle) | **Tuấn Lĩnh** | 4 ca lỗi thực tế: Q07 (Missing retrieval), Q12 (Table column), Q19 (Citation), Q03 (Truncation). |
| **11:30 – 12:45** | 1:15 | **10** | Thảo luận Chuyên sâu: RAG vs. Hallucination | **Tuấn Lĩnh** | Trả lời trực diện Guiding Question: RAG không triệt tiêu hallucination mà dịch chuyển bản chất lỗi. |
| **12:45 – 14:00** | 1:15 | **11** | Đề xuất Cải tiến & Verification Loop | **Tuấn Lĩnh** | Áp dụng Schneider (2024 - GenXAI): Hậu kiểm verification loop, Hybrid Retrieval, Table structuring. |
| **14:00 – 15:00** | 1:00 | **12** | Tổng kết, References & Mở đầu Q&A | **Tuấn Lĩnh** | 3 Takeaways then chốt; Trích dẫn paper bắt buộc/khuyến nghị; Mở lời chuyển sang phiên Q&A 5 phút. |
| **15:00 – 20:00** | 5:00 | -- | **Phiên Hỏi & Đáp (Q&A)** | **Cả 3 thành viên** | Trả lời phản biện của Giảng viên và lớp học (Tiêu chí 20 điểm rubric). |

---

## 3. Chiến lược Quản lý Thời gian Dự phòng (Buffer & Pace Control)

- **Nguyên tắc "Đèn vàng" (Pacing Checkpoints):**
  - **Mốc 04:30:** Nếu Nam Kiệt chưa qua slide 4, cần tóm tắt nhanh phần kết quả numerical example và chuyển giao đúng 05:00.
  - **Mốc 09:30:** Nếu Lê Huy chưa qua slide 8, chỉ cần đối chiếu điểm khác biệt mấu chốt giữa Grounded RAG và Non-RAG rồi bàn giao đúng 10:00.
  - **Mốc 14:00:** Tuấn Lĩnh bắt đầu slide 12, đảm bảo đúng 14:50 - 15:00 là dứt lời cảm ơn, không bị ngắt ngang do lố giờ.
- **Phân bổ trả lời Q&A (15:00 – 20:00):**
  - Câu hỏi về Lý thuyết / Phương trình / RAG Pipeline: **Nam Kiệt** chủ trì trả lời.
  - Câu hỏi về Dataset / Corpus HCMUS / Retrieval Metrics (Recall@k, Hit Rate): **Lê Huy** chủ trì trả lời.
  - Câu hỏi về Failure analysis / Hallucination / Hậu kiểm GenXAI / Hướng phát triển: **Tuấn Lĩnh** chủ trì trả lời.

---

## 4. Chi tiết Nội dung Từng Slide theo Timeline

### Phần 1: Lý thuyết Nền tảng & Mô hình Xác suất (00:00 – 05:00)
**Diễn giả:** Trịnh Võ Nam Kiệt (`24125013`)

#### Slide 1: Tiêu đề & Giới thiệu Đề tài (00:00 – 01:00 | 60 giây)
- **Tiêu đề chính:** `[S07] Retrieval-Augmented Generation (RAG): Grounding LLM Responses in Documents`
- **Thông tin môn học:** CS420 — Nhập môn Trí tuệ Nhân tạo | Trường ĐH Khoa học Tự nhiên, ĐHQG-HCM.
- **Thành viên nhóm:** Trịnh Võ Nam Kiệt (`24125013`), Trần Đăng Lê Huy (`24125057`), Bùi Tuấn Lĩnh.
- **Thông điệp:** Khởi động bài thuyết trình, nêu tôn chỉ nghiên cứu: kết hợp chặt chẽ giữa lý thuyết xác suất nền tảng (Lewis et al., 2020) và đo lường thực nghiệm độc lập trên quy chế HCMUS.

#### Slide 2: Đặt vấn đề & Câu hỏi Nghiên cứu (01:00 – 02:15 | 75 giây)
- **Hạn chế của mô hình Parametric-only:** Ảo giác (Hallucination), lỗi thời kiến thức (Cut-off date), thiếu khả năng truy vết nguồn gốc (Attribution).
- **So sánh 3 phương pháp tiếp cận:**
  - *Fine-tuning:* Cập nhật trọng số tham số; tốn kém GPU, nguy cơ quên thảm họa (Catastrophic forgetting), vẫn ảo giác.
  - *Long-context Prompting:* Đưa toàn bộ tài liệu vào context; chi phí token cao, suy giảm khả năng chú ý (*Lost in the middle*).
  - *RAG (Hybrid Memory):* Tách biệt Parametric (LLM sinh ngữ) và Non-parametric (Index tài liệu có thể cập nhật nóng *hot-swapping*).
- **Câu hỏi định hướng (Guiding Question):**
  > *"Does providing external documents eliminate hallucinations in language models?"*  
  > *(Việc cung cấp tài liệu bên ngoài có thực sự triệt tiêu hiện tượng ảo giác trong mô hình ngôn ngữ hay không?)*
- **Tài liệu dẫn:** Lewis et al. (2020), RAGTruth (Niu et al., 2024).

#### Slide 3: Kiến trúc RAG Pipeline & Failure Points Lý thuyết (02:15 – 03:30 | 75 giây)
- **Sơ đồ 6 bước chuẩn mực:**
  $$\text{Ingestion} \longrightarrow \text{Chunking} \longrightarrow \text{Indexing} \longrightarrow \text{Retrieval} \longrightarrow \text{Prompt Augmentation} \longrightarrow \text{Generation}$$
- **Phân tích rủi ro lỗi tại từng bước:**
  - *Ingestion:* Lỗi OCR quét PDF, mất định dạng bảng biểu.
  - *Chunking:* Cắt ngang điều khoản luật, mất ngữ cảnh cha-con.
  - *Indexing:* Lệch không gian biểu diễn giữa từ khóa chuyên ngành và embedding.
  - *Retrieval:* False positives (chọn nhầm đoạn giống từ ngữ nhưng khác nội dung) hoặc False negatives (bỏ sót bằng chứng).
  - *Prompt Augmentation:* Context quá dài làm loãng sự chú ý của mô hình sinh.
  - *Generation:* Generator phớt lờ context, suy diễn vượt quá bằng chứng hoặc trích dẫn nguồn giả.
- **Tài liệu dẫn:** [`research/G1_Task4_RAG_Pipeline.md`](../research/G1_Task4_RAG_Pipeline.md).

#### Slide 4: Mô hình Toán học: RAG-Sequence & Ví dụ Số (03:30 – 04:55 | 85 giây)
- **Phương trình RAG-Sequence (Lewis et al., NeurIPS 2020):**
  $$p(y|x) \approx \sum_{z \in \text{top-}k} p_\eta(z|x) \cdot p_\theta(y|x, z) = \sum_{z \in \text{top-}k} p_\eta(z|x) \prod_{i=1}^N p_\theta(y_i|x, z, y_{1:i-1})$$
- **Bản chất toán học:** Biến tài liệu $z$ là một **biến ẩn (latent variable)**. Việc sinh toàn bộ chuỗi đáp án $y$ được điều kiện hóa trên cùng một tài liệu $z$, sau đó lấy kỳ vọng xác suất trên Top-$k$ tài liệu.
  - *Phân biệt với RAG-Token:* RAG-Token cho phép mỗi token $y_i$ chuyển đổi sang một tài liệu $z$ khác nhau.
- **Worked Numerical Example (Ví dụ tính toán số):**
  - Giả định $k=2$ tài liệu $z_1, z_2$ với xác suất truy xuất $p_\eta(z_1|x)=0.80$ và $p_\eta(z_2|x)=0.20$.
  - Tính toán marginalization cụ thể để chứng minh cách trọng số truy xuất điều khiển xác suất sinh chuỗi từ.
- **Tín hiệu chuyển giao (04:55 – 05:00):** Nam Kiệt bàn giao lời cho Lê Huy bước vào phần thực nghiệm.
- **Tài liệu dẫn:** Lewis et al. (2020), [`research/TASK_5.md`](../research/TASK_5.md).

---

### Phần 2: Thiết lập Thực nghiệm & Worked Example Thực tế (05:00 – 10:00)
**Diễn giả:** Trần Đăng Lê Huy (`24125057`)

#### Slide 5: Thiết lập Thực nghiệm (Corpus & Benchmark Quy chế HCMUS) (05:00 – 06:00 | 60 giây)
- **Knowledge Corpus thực tế:**
  - 4 văn bản quy chế đào tạo chính quy của Trường ĐH Khoa học Tự nhiên (Quy chế đào tạo 2026, CT Tiên tiến, CT Tài năng, Biểu mức thu học phí).
  - Quy mô: 51 trang văn bản pháp lý, chia thành 162 chunks chuẩn hóa có cấu trúc ($\le 800$ tokens `cl100k_base`).
- **Benchmark Đánh giá 20 câu hỏi:**
  - 20 câu hỏi đa dạng loại hình: định nghĩa khái niệm, đối chiếu quy tắc, tra cứu con số học phí, điều kiện học vụ.
  - 30 gold evidence spans trích xuất trực tiếp làm căn cứ xác thực (Verifiable Ground Truth).
- **Hạ tầng Thực nghiệm:**
  - Môi trường: Kaggle GPU Tesla T4 (FP16 dense retrieval + FP32 generation với SDPA).
  - Mô hình: BGE-M3 (1024 chiều) làm Retriever; Qwen2.5-1.5B-Instruct làm Generator.
- **Tài liệu dẫn:** [`experiment/README.md`](../experiment/README.md).

#### Slide 6: Đánh giá Năng lực Truy xuất (Retrieval Performance) (06:00 – 07:30 | 90 giây)
- **Bảng số liệu đối sánh 3 cấu hình tại $k \in \{1, 3, 5\}$:**

  | Phương pháp | $k$ | Hit Rate@k | Evidence Recall@k | All Evidence Hit@k | MRR@k |
  | :--- | :---: | :---: | :---: | :---: | :---: |
  | **TF-IDF (Sparse)** | 1 / 3 / 5 | 70.0% / 85.0% / **90.0%** | 60.8% / 75.8% / **82.5%** | 50.0% / 65.0% / **70.0%** | 0.7600 |
  | **BM25 (Sparse)** | 1 / 3 / 5 | **85.0%** / 85.0% / **90.0%** | 71.7% / 78.3% / **84.2%** | **65.0%** / 70.0% / **80.0%** | **0.8500** |
  | **BGE-M3 (Dense)** | 1 / 3 / 5 | 70.0% / **85.0%** / **95.0%** | 60.8% / **77.5%** / **85.0%** | 50.0% / 65.0% / **70.0%** | 0.7867 |

- **Phân tích phát hiện:**
  - Dense BGE-M3 đạt Hit@5 cao nhất (95.0%), thích hợp bắt ngữ nghĩa diễn đạt tự do.
  - BM25 có độ chính xác Top-1 áp đảo (Hit@1 = 85.0%) nhờ khả năng khớp chuẩn xác các mã hiệu điều luật và thuật ngữ kỹ thuật.
  - **Điểm nhấn phản biện cốt lõi:** *Hit@5 đạt 95.0% KHÔNG ĐỒNG NGHĨA câu trả lời đạt độ chính xác 95.0%!*
- **Tài liệu dẫn:** [`experiment/results/kaggle_2026-11-05/README.md`](../experiment/results/kaggle_2026-11-05/README.md).

#### Slide 7: Worked Example Thực tế — Bước Truy xuất Bằng chứng (07:30 – 08:45 | 75 giây)
- **Truy vấn đầu vào (Query $x$ - Q01):**
  > *"Theo Quy chế 2026, học phần tiên quyết khác học phần học trước như thế nào?"*
- **Tính cấp thiết của câu hỏi:** Phân biệt hai khái niệm dễ nhầm lẫn nhất trong quy chế đào tạo; đòi hỏi tuyệt đối chính xác từ ngữ văn bản.
- **Bảng Top-5 Chunks được BGE-M3 truy xuất:**
  - **Hạng 1:** `D01_regulation_article_3_03` — Cosine Similarity = **0.8412** $\to$ Chứa 100% bằng chứng vàng (Điều 3, Khoản 3, Điểm c).
  - Hạng 2 & 3: Các chunk điều khoản chuyển tiếp và phạm vi áp dụng chung (Sim: 0.7245 & 0.7103).
- **Trích đoạn Bằng chứng Vàng (Gold Evidence):**
  - Tiên quyết: bắt buộc phải học và **"thi đạt"**.
  - Học trước: chỉ yêu cầu **"hoàn thành quá trình học tập"** (không yêu cầu thi đạt).
- **Tài liệu dẫn:** [`research/G2_TASK_5.md`](../research/G2_TASK_5.md).

#### Slide 8: Worked Example Thực tế — Prompt Augmentation & So sánh Đáp án (08:45 – 09:55 | 70 giây)
- **Kỹ thuật đóng gói Prompt Augmentation:**
  - Ép khuôn System Prompt: "Chỉ trả lời dựa trên bằng chứng được cung cấp, bắt buộc trích dẫn mã `[chunk_id]`".
  - Cung cấp Context tường minh kèm mã chunk `[D01_regulation_article_3_03]`.
- **So sánh Trực diện Hai Điều kiện:**
  - **Non-RAG (Chỉ dựa vào Parametric Memory):** Ảo giác nghiêm trọng! Mô hình tự suy luận sai lầm rằng *"cả hai học phần đều bắt buộc phải thi đạt với điểm số trên trung bình"*.
  - **Grounded RAG (Có Non-parametric Context):** Trả lời chính xác 100% từng câu chữ pháp lý ("thi đạt" vs "hoàn thành quá trình học"), kèm trích dẫn chuẩn xác `[D01_regulation_article_3_03]`.
- **Tín hiệu chuyển giao (09:55 – 10:00):** Lê Huy chuyển lời cho Tuấn Lĩnh phân tích các trường hợp lỗi.
- **Tài liệu dẫn:** [`research/G2_TASK_5.md`](../research/G2_TASK_5.md).

---

### Phần 3: Phân tích Lỗi, Thảo luận Phản biện & Cải tiến (10:00 – 15:00)
**Diễn giả:** Bùi Tuấn Lĩnh

#### Slide 9: Phân tích 4 Ca Lỗi Thực nghiệm Điển hình (10:00 – 11:30 | 90 giây)
- **Thực tế đánh giá 20 câu:** Trong 8 câu RAG trả lời sai hoặc không đầy đủ, có tới **6 câu đã có đủ bằng chứng trong prompt**.
- **Phân loại 4 ca lỗi đặc trưng từ log chạy Kaggle:**
  1. **Missing Retrieval (Q07):** Bằng chứng ngưỡng điểm Khá (65–79 điểm) nằm ở hạng 11 $\to$ rơi khỏi Top-5 $\to$ Generator suy diễn sai thành 50 điểm (Lỗi tại khâu Retrieval).
  2. **Table Column Misreading (Q12):** Bằng chứng bảng học phí có trong context, nhưng generator đọc lộn cột C4 (734.000đ) thay vì cột C5 (1.014.000đ) $\to$ Lỗi đọc hiểu cấu trúc bảng biểu tại Generator.
  3. **Ungrounded / Fake Citation (Q19):** Mô hình sinh ra nhãn trích dẫn placeholder giả `[chunk_id]` thay vì dẫn mã chunk thực tế $\to$ Lỗi tuân thủ chỉ dẫn (Instruction following).
  4. **Token Budget Truncation (Q03):** Câu trả lời chạm ngưỡng 384 tokens dẫn đến ngắt cụt câu $\to$ Lỗi do cấu hình giới hạn chiều dài output.
- **Tài liệu dẫn:** [`experiment/results/kaggle_2026-11-05/ERROR_ANALYSIS_AND_IMPROVEMENT_2026-11-07.md`](../experiment/results/kaggle_2026-11-05/ERROR_ANALYSIS_AND_IMPROVEMENT_2026-11-07.md).

#### Slide 10: Thảo luận Chuyên sâu: RAG vs. Ảo giác (11:30 – 12:45 | 75 giây)
- **Trả lời trực diện Guiding Question:**  
  *Cung cấp tài liệu bên ngoài có triệt tiêu hoàn toàn ảo giác không?* $\longrightarrow$ **KHÔNG!**
- **Bản chất của sự chuyển dịch (Paradigm Shift):**
  - RAG giải quyết được *tri thức thiếu hụt* (Parametric Knowledge Gap) và loại bỏ ảo giác bịa đặt vô căn cứ.
  - Tuy nhiên, RAG sinh ra **ảo giác dạng mới (New Failure Modes)** do sai số lan truyền qua pipeline: *Retrieval miss, Context distraction, Multi-hop reasoning failure, và Unfaithful attribution*.
- **Đối chiếu học thuật:**
  - Kết quả thực nghiệm của nhóm hoàn toàn tương đồng với phát hiện của Schneider (2024 - GenXAI) và Niu et al. (2024 - RAGTruth): *Cung cấp context chỉ là điều kiện cần, không phải điều kiện đủ để đảm bảo tính trung thực (faithfulness).*

#### Slide 11: Đề xuất Giải pháp Cải tiến & Verification Loop (12:45 – 14:00 | 75 giây)
- **Khung giải thích & Hậu kiểm theo Schneider (2024 - GenXAI):**
  - *Post-generation Verification Loop:* Thêm tầng kiểm tra xác thực câu trả lời có được hỗ trợ 100% bởi citation hay không trước khi gửi người dùng; từ chối trả lời nếu thiếu căn cứ.
- **Nâng cấp Khâu Retrieval & Indexing:**
  - *Hybrid Search:* Kết hợp BM25 (chính xác từ khóa quy chế) + Dense BGE-M3 (bắt ngữ nghĩa).
  - *Cross-Encoder Reranker:* Mở rộng ứng viên ($k=15$) rồi rerank lấy Top-5 chuẩn xác nhất.
- **Nâng cấp Xử lý Ngữ cảnh (Context Structuring):**
  - Chuyển đổi bảng biểu quy chế phức tạp thành định dạng Markdown có cấu trúc hoặc JSON key-value rõ ràng để chống lỗi đọc lệch cột như ở Q12.
  - *Index Hot-swapping:* Cập nhật tri thức non-parametric tức thì khi có quy chế mới mà không cần train lại.

#### Slide 12: Tổng kết, References & Chuyển tiếp Q&A (14:00 – 15:00 | 60 giây)
- **3 Thông điệp Đúc kết (Core Takeaways):**
  1. RAG là cầu nối hiệu quả giữa parametric model và tài liệu pháp lý chuyên ngành.
  2. Retrieval đạt Recall cao chỉ là một nửa chặng đường; năng lực đọc hiểu ngữ cảnh và cơ chế trích dẫn của Generator mới quyết định độ chính xác thực tế.
  3. Cần triển khai đồng bộ cơ chế hậu kiểm (verification loop) để RAG trở thành hệ thống đáng tin cậy.
- **Tài liệu tham khảo chính:**
  - Lewis et al. (2020) — *Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks*, NeurIPS.
  - Schneider, J. (2024) — *Explainable Generative AI (GenXAI)*, Springer.
  - Niu et al. (2024) — *RAGTruth: A Hallucination Corpus for RAG*, ACL.
- **Mở đầu phiên Q&A (15:00 – 20:00):** Cả 3 thành viên sẵn sàng bảo vệ kỹ thuật và trả lời câu hỏi của Giảng viên và Hội đồng.
