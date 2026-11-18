# Kịch bản Thuyết trình Trực tuyến — Speaker 2

> **Hình thức:** Trực tuyến (Google Meet / Zoom / MS Teams)  
> **Diễn giả:** Trần Đăng Lê Huy (`24125057`)  
> **Nhiệm vụ:** Phần 2 — *Corpus HCMUS, Thực nghiệm Retrieval & Ví dụ Q01*  
> **Thời lượng:** **05:00 phút** (`05:00 – 10:00`) | **Slides:** 08–12  
> **Thiết lập:** Bật mic ngay khi Nam Kiệt xong, dùng chuột chỉ dẫn bảng số liệu.

---

## Bảng Thời gian & Checkpoints (Speaker 2)

| Slide | Tiêu đề | Mốc thời gian | Thời lượng | Thao tác |
| :---: | :--- | :---: | :---: | :--- |
| **08** | HCMUS Corpus | `05:00 – 05:55` | 55s | Bật mic, bấm `Space`, rê chuột 4 văn bản. |
| **09** | Retrieval Setup | `05:55 – 06:45` | 50s | Bấm `Space`, chỉ 4 chỉ số đánh giá. |
| **10** | Retrieval Benchmark | `06:45 – 07:45` | 60s | Bấm `Space`, khoanh BM25 80% vs BGE-M3 89.17%. |
| **11** | Example Q01 Retrieval | `07:45 – 08:50` | 65s | Bấm `Space`, chỉ Hạng 1 Cosine 0.6271. |
| **12** | Example Q01 Output | `08:50 – 09:55` | 65s | Bấm `Space`, so Baseline 0/2 vs RAG 2/2. |
| **--** | **Handoff** | `09:55 – 10:00` | 05s | Nhường lời cho Tuấn Lĩnh. |

> [!TIP]
> **Checkpoint `08:50`:** Phải đang ở Slide 12. Nhấn mạnh Baseline (đoán sai) vs RAG (đúng *thi đạt* vs *hoàn thành học tập*), rồi nhường lời cho Lĩnh đúng `09:55`.

---

## Chi tiết Từng Slide

### Slide 08: HCMUS Regulatory Documents (`08_corpus.tex`)
- **Thời lượng:** `05:00 – 05:55` (55s)
- **Trên màn hình:** Bảng 4 văn bản D01–D04 (51 trang, 162 chunks, trần 800 tokens); 20 câu hỏi / 30 gold evidence.
- **Thao tác:** `[ACTION]:` Bật mic, bấm `Space` sang Slide 08. `[MOUSE]:` Lướt qua D01–D04.

#### Tiếng Việt:
> "Cảm ơn Kiệt. Em là **Lê Huy**, em xin trình bày phần thực nghiệm.  
> Nhóm thu thập **4 văn bản quy chế chính thức của HCMUS**: `[MOUSE: Bảng]`  
> 1. **D01:** Quy chế đào tạo 2026 (21 trang).  
> 2. **D02:** Quy chế điểm rèn luyện 2020 & sửa đổi 2023 (16 trang).  
> 3. **D03:** Học phí 2026–2027 cho khóa 2022 trở về sau (5 trang).  
> 4. **D04:** Chuẩn ngoại ngữ tốt nghiệp (9 trang).  
> Tổng cộng **51 trang** — lớn hơn mức gợi ý 5–10 trang để thử thách tìm kiếm chéo nhiều điều luật.  
> Dữ liệu được chia thành 80 mục và **162 chunks** (tối đa 800 token `cl100k_base`).  
> Bộ test gồm **20 câu hỏi** và **30 nhóm bằng chứng vàng**, tách riêng khỏi kho tìm kiếm."

#### English:
> "Thank you, Kiet. I am **Le Huy**, and I will present our experiments.  
> We collected **four official HCMUS regulation documents**: `[MOUSE: Table]`  
> 1. **D01:** Academic Regulations 2026 (21 pages).  
> 2. **D02:** Conduct Assessment 2020 & 2023 Amendment (16 pages).  
> 3. **D03:** Tuition Fees 2026–2027 for Cohort 2022+ (5 pages).  
> 4. **D04:** Foreign Language Exit Standards (9 pages).  
> In total, **51 pages**—larger than the 5–10 page guideline to test cross-article lookup.  
> We split them into 80 sections and **162 chunks** (800-token cap, `cl100k_base`).  
> Our benchmark has **20 questions** and **30 gold evidence groups**, kept separate from the index."

- **Chuyển slide:** `"Tiếp theo là 3 bộ tìm kiếm và cách đánh giá."` $\to$ Bấm `Space`.

---

### Slide 09: Retrieval Configurations & Protocol (`09_retrieval_setup.tex`)
- **Thời lượng:** `05:55 – 06:45` (50s)
- **Trên màn hình:** Bảng TF-IDF, BM25, BGE-M3 và 4 chỉ số tại $k \in \{1, 3, 5\}$.
- **Thao tác:** `[MOUSE]:` Chỉ BM25 ($k_1=1.5, b=0.75$) và BGE-M3 (1024 chiều).

#### Tiếng Việt:
> "Nhóm so sánh 3 bộ tìm kiếm: `[MOUSE: Bảng]`  
> - **TF-IDF:** Đếm từ khóa cơ bản (unigram, bigram).  
> - **BM25:** Tìm từ khóa nâng cao, giới hạn lặp từ ($k_1=1.5$) và phạt độ dài ($b=0.75$).  
> - **BGE-M3:** Nhúng ngữ nghĩa đa ngôn ngữ thành vector 1024 chiều.  
> Nhóm đo 4 chỉ số trên 20 câu hỏi tại $k = 1, 3, 5$:  
> - **Evidence Recall@$k$:** Tỷ lệ bằng chứng vàng tìm được ($r/m$).  
> - **Hit Rate@$k$:** Tỷ lệ câu tìm được ít nhất 1 bằng chứng.  
> - **All Evidence Hit@$k$:** Tỷ lệ câu tìm đủ 100% bằng chứng.  
> - **MRR@$k$:** Thứ hạng nghịch đảo của đoạn đúng đầu tiên."

#### English:
> "We compare three retrievers: `[MOUSE: Table]`  
> - **TF-IDF:** Basic keyword frequency (unigram and bigram).  
> - **BM25:** Keyword matching with term saturation ($k_1=1.5$) and length penalty ($b=0.75$).  
> - **BGE-M3:** Multilingual dense embeddings using 1024-dimensional vectors.  
> We measure four metrics at $k \in \{1, 3, 5\}$:  
> - **Evidence Recall@$k$:** Share of required gold evidence found ($r/m$).  
> - **Hit Rate@$k$:** Share of queries with at least one gold chunk.  
> - **All Evidence Hit@$k$:** Share of queries with 100% of gold chunks.  
> - **MRR@$k$:** Reciprocal rank of the first relevant chunk."

- **Chuyển slide:** `"Đây là kết quả thực nghiệm 1."` $\to$ Bấm `Space`.

---

### Slide 10: Experiment 1: Retrieval Performance (`10_retrieval_results.tex`)
- **Thời lượng:** `06:45 – 07:45` (60s)
- **Trên màn hình:** Bảng Table 4 và 4 nhận xét.
- **Thao tác:** `[MOUSE]:` Khoanh **80.00%** của BM25 (Recall@1), rồi **89.17%** và **95.00%** của BGE-M3 ($k=5$).

#### Tiếng Việt:
> "Bảng Table 4 cho thấy sự khác biệt rất rõ:  
> - **BM25 mạnh nhất ở Top-1:** `[MOUSE: Recall@1]` Đạt **80.00% Recall@1** và **0.8667 MRR@5** vì khớp chính xác mã điều luật như 'Điều 3'.  
> - **BGE-M3 mạnh nhất ở Top-5:** `[MOUSE: Recall@5]` Đạt **89.17% Recall@5** và **95.00% Hit@5** nhờ hiểu được ngữ nghĩa khi hỏi tự do.  
> - **Điểm bão hòa:** Các mô hình từ khóa chững lại sau $k=3$, còn BGE-M3 tăng thêm 7.5%.  
> `[nhấn mạnh]` **Lưu ý quan trọng:** Hit@5 đạt 95% KHÔNG có nghĩa câu trả lời đúng 95%! Bước sinh câu trả lời vẫn còn nhiều lỗi."

#### English:
> "Table 4 shows a clear trade-off:  
> - **BM25 wins at Top-1:** `[MOUSE: Recall@1]` It reaches **80.00% Recall@1** and **0.8667 MRR@5** because exact keywords match article numbers well.  
> - **BGE-M3 wins at Top-5:** `[MOUSE: Recall@5]` It leads with **89.17% Recall@5** and **95.00% Hit@5** by capturing meaning.  
> - **Plateau:** Keyword methods stop improving after $k=3$, while BGE-M3 gains +7.50 percentage points.  
> `[emphasize]` **Key warning:** A 95.00% Hit@5 does NOT mean 95% answer accuracy! Generation errors still happen."

- **Chuyển slide:** `"Hãy xem ví dụ thực tế ở câu hỏi Q01."` $\to$ Bấm `Space`.

---

### Slide 11: Worked Example (Q01): Retrieval (`11_worked_example_retrieval.tex`)
- **Thời lượng:** `07:45 – 08:50` (65s)
- **Trên màn hình:** Câu hỏi Q01 và bảng Top-5 của BGE-M3.
- **Thao tác:** `[MOUSE]:` Chỉ câu Q01, rồi chỉ Hạng 1 (`D01_regulation_article_3_03`, Cosine 0.6271).

#### Tiếng Việt:
> "Xét câu hỏi **Q01**: `[MOUSE: Câu hỏi]` *'Học phần tiên quyết khác học phần học trước thế nào?'*  
> Bảng trên là kết quả xếp hạng của BGE-M3: `[MOUSE: Hàng 1]`  
> - **Hạng 1:** Đưa đúng đoạn `D01_regulation_article_3_03` lên đầu với Cosine **0.6271** (trang 4).  
> Đoạn này chứa đủ **100% bằng chứng** (Điều 3, Khoản 3c):  
>   + Môn tiên quyết: phải học và **'thi đạt'**.  
>   + Môn học trước: chỉ cần **'hoàn thành quá trình học tập'**.  
> - **Đoạn gây nhiễu:** `[MOUSE: Hàng 2--5]` Các hạng 2–5 là quy định miễn tín chỉ và lịch học, dễ làm mô hình sinh bị rối."

#### English:
> "Let us look at query **Q01**: `[MOUSE: Question]` *'How does a prerequisite course differ from a pre-learning course?'*  
> This table shows BGE-M3's top-5 results: `[MOUSE: Rank 1]`  
> - **Rank 1:** `D01_regulation_article_3_03` ranks first with **0.6271** cosine similarity (page 4).  
> It holds **100% of the gold evidence** (Article 3, Clause 3c):  
>   + Prerequisite: students must enroll and **'pass'** the exam.  
>   + Pre-learning: students only need to **'complete the study process'**.  
> - **Distractors:** `[MOUSE: Ranks 2--5]` Ranks 2–5 cover credit transfers and scheduling, which can confuse the generator."

- **Chuyển slide:** `"Vậy mô hình trả lời thế nào khi có và không có 5 đoạn này?"` $\to$ Bấm `Space`.

---

### Slide 12: Worked Example (Q01): Output (`12_worked_example_generation.tex`)
- **Thời lượng:** `08:50 – 09:55` (65s)
- **Trên màn hình:** Bảng so sánh Baseline (0/2) vs Grounded RAG (2/2).
- **Thao tác:** `[MOUSE]:` Chỉ Baseline, rồi Grounded RAG, gạch dưới *"thi đạt"* và *"hoàn thành quá trình học tập"*.

#### Tiếng Việt:
> "Đây là câu trả lời của **Qwen2.5-1.5B-Instruct**: `[MOUSE: Bảng]`  
> - **Baseline (Không RAG):** Được **0/2 điểm**. Do không có tài liệu, mô hình đoán mò sai rằng cả hai môn đều phải thi đạt.  
> - **Grounded RAG (BGE-M3):** Được **2/2 điểm**. Nhờ đoạn Điều 3, mô hình phân biệt đúng: tiên quyết phải **'thi đạt'**, còn học trước chỉ cần **'hoàn thành quá trình học tập'**.  
> - **Lưu ý:** Cả 60 câu RAG của Qwen đều **không tự xuất được mã trích dẫn**; mã `[D01_regulation_article_3_03]` trên slide là do nhóm tự kiểm tra và gắn thêm."

#### English:
> "Here is how **Qwen2.5-1.5B-Instruct** answers: `[MOUSE: Table]`  
> - **Baseline (No RAG):** Scores **0 / 2**. Without documents, it guesses wrong that both courses require passing grades.  
> - **Grounded RAG (BGE-M3):** Scores **2 / 2**. Using Article 3, it correctly states prerequisite requires **'passing'**, while pre-learning only requires **'completing the study process'**.  
> - **Note:** All 60 RAG answers from Qwen **failed to output valid citation IDs**; our team verified and added `[D01_regulation_article_3_03]` manually."

- **Online Handoff (`09:55 – 10:00`):**  
  `[ACTION]:` Nhìn webcam, nói rõ:  
  - **Tiếng Việt:** *"Dù Q01 thành công, hệ thống vẫn còn nhiều lỗi ở các câu khác. Em xin nhường mic cho bạn Tuấn Lĩnh phân tích các ca lỗi thực tế ạ."*  
  - **English:** *"While Q01 worked well, errors still happen on other queries. I will hand over to Tuan Linh to analyze the failure cases."*  
  `[ACTION]:` Tắt mic (Mute).

---

## Q&A Trực tuyến (Speaker 2: Lê Huy)

1. **Q05: Corpus gồm gì? Sao lại 51 trang thay vì 5–10 trang?**  
   - Gồm 4 quy chế (Đào tạo 21p, Rèn luyện 16p, Học phí 5p, Ngoại ngữ 9p). Nhóm dùng toàn văn 51 trang để test khả năng tìm chéo điều khoản thực tế.
2. **Q06: Vì sao chia theo cấu trúc và giới hạn 800 token?**  
   - Để giữ nguyên điều khoản và bảng biểu; trần 800 token (`cl100k_base`, lớn nhất 788 tokens) đủ ngữ cảnh mà không quá tải prompt.
3. **Q08: Vì sao chọn top-5? Đã so sánh đủ cấu hình chưa?**  
   - Đã đo retrieval tại $k=1, 3, 5$. Khi sinh câu trả lời, nhóm cố định top-5 để so sánh công bằng cả 3 retriever.
4. **Q09: Hit Rate, Evidence Recall, All Evidence Hit và MRR khác gì nhau?**  
   - Hit Rate: có ít nhất 1 đoạn đúng; Recall: tỷ lệ đoạn đúng tìm được ($r/m$); All Evidence: tìm đủ 100% ($r=m$); MRR: nghịch đảo hạng của đoạn đúng đầu tiên.
5. **Q10: BM25 hay BGE-M3 tốt hơn?**  
   - Tùy mục tiêu: BM25 tốt nhất ở Top-1 (Recall@1 = 80%); BGE-M3 tốt nhất ở độ phủ Top-5 (Recall@5 = 89.17%, Hit@5 = 95%).
6. **Q11: So sánh có/không RAG có công bằng không?**  
   - Công bằng: dùng chung Qwen2.5-1.5B, cùng system prompt, cùng greedy decoding (temperature=0, seed=42), tối đa 768 tokens.
7. **Q14: Đánh giá chất lượng trả lời thế nào? Hạn chế là gì?**  
   - Chấm 3 mức (0: sai, 1: một phần, 2: đúng chính). Kết quả sơ bộ do GPT chấm có giải thích; chưa có chấm mù độc lập.
