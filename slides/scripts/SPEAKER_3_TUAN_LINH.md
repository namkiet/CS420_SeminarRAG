# Kịch bản Thuyết trình Trực tuyến — Speaker 3

> **Hình thức:** Trực tuyến (Google Meet / Zoom / MS Teams)  
> **Diễn giả:** Bùi Trọng Tuấn Lĩnh (`24125066`)  
> **Nhiệm vụ:** Phần 3 — *Chất lượng Trả lời, 5 Ca lỗi, Thảo luận & Hậu kiểm*  
> **Thời lượng:** **05:00 phút** (`10:00 – 15:00`) | **Slides:** 13–20  
> **Thiết lập:** Bật mic ngay khi Lê Huy xong, bấm `Space` chuyển slide (lưu ý **3 lần bấm Space ở Slide 15**), dùng chuột chỉ bảng số liệu.

---

## Bảng Thời gian & Checkpoints (Speaker 3)

| Slide | Tiêu đề | Mốc thời gian | Thời lượng | Thao tác |
| :---: | :--- | :---: | :---: | :--- |
| **13** | 4-Way Answer Quality | `10:00 – 11:00` | 60s | Bật mic, bấm `Space`, chỉ +45–50 pp. |
| **14** | 5 Failure Archetypes | `11:00 – 12:05` | 65s | Bấm `Space`, chỉ 5 lỗi (Q07, Q01, Q05, Q13, Q19). |
| **15** | RAG vs Hallucination | `12:05 – 12:55` | 50s | Bấm `Space`. **Slide này bấm Space 3 lần!** |
| **16** | Limitations | `12:55 – 13:45` | 50s | Bấm `Space`, rê chuột qua 5 giới hạn. |
| **17** | Verification & Maintenance | `13:45 – 14:30` | 45s | Bấm `Space`, chỉ tuple GenXAI & Bảng biểu. |
| **18** | Conclusions | `14:30 – 14:55` | 25s | Bấm `Space`, chốt câu màu xanh ở đáy. |
| **19** | References | `14:55 – 14:58` | 03s | Bấm `Space` lướt qua tài liệu tham khảo. |
| **20** | Thank You & Q&A | `14:58 – 15:00` | 02s | Bấm `Space`, cảm ơn và mời đặt câu hỏi. |

> [!IMPORTANT]
> **Checkpoint `14:30`:** Phải bấm sang Slide 18 (Conclusions). Đọc rõ câu chốt màu xanh ở đáy và kết thúc đúng `14:55 – 15:00`.

---

## Chi tiết Từng Slide

### Slide 13: Experiment 2: 4-Way Answer Quality (`13_generation_quality.tex`)
- **Thời lượng:** `10:00 – 11:00` (60s)
- **Trên màn hình:** Bảng Table 5 đánh giá 80 câu trả lời; dòng nổi bật: *+45.0 to +50.0 pp accuracy gain*.
- **Thao tác:** `[ACTION]:` Bật mic, bấm `Space`. `[MOUSE]:` Chỉ Baseline ($0/20$), 3 hàng RAG ($10/20, 9/20, 10/20$), và cột cuối ($0/20$ Citations).

#### Tiếng Việt:
> "Cảm ơn Huy. Em là **Tuấn Lĩnh**, em xin trình bày phần 3.  
> Bảng trên đánh giá **80 câu trả lời** trong Task 6: `[MOUSE: Bảng]`  
> - **RAG tăng độ chính xác rõ rệt:** Baseline không RAG chỉ đạt **0/20 (0%)** và có tới 75% câu chứa thông tin bịa đặt. Khi dùng RAG, tỷ lệ đúng tăng lên **50.0%** (TF-IDF, BGE-M3) và **45.0%** (BM25) — tức tăng **+45 đến +50 điểm phần trăm**.  
> - **Giảm ảo giác:** Thông tin sai ngoài nguồn giảm từ 75% xuống còn 30% ở BGE-M3.  
> - **Nhưng vẫn còn 2 vấn đề lớn:**  
>   1. BGE-M3 có Recall@5 cao hơn (89.17%) nhưng độ chính xác cuối cùng vẫn hòa TF-IDF ở mức 50%.  
>   2. `[MOUSE: Cột cuối]` **Cả 60 câu trả lời RAG đều không tự tạo được mã trích dẫn hợp lệ.**"

#### English:
> "Thank you, Le Huy. I am **Tuan Linh**, and I will present Part 3 on **80 generated answers** in Task 6: `[MOUSE: Table]`  
> - **RAG boosts accuracy:** The baseline scores **0 / 20 (0%)** with 75% unsupported claims. RAG jumps to **50.0%** for TF-IDF and BGE-M3, and **45.0%** for BM25—a **+45 to +50 percentage point gain**.  
> - **Fewer hallucinations:** Unsupported claims drop from 75% down to 30% with BGE-M3.  
> - **However, two bottlenecks remain:**  
>   1. BGE-M3 has higher Recall@5 (89.17%), yet ties with TF-IDF at 50% answer accuracy.  
>   2. `[MOUSE: Last column]` **All 60 RAG answers failed to generate valid citation IDs.**"

- **Chuyển slide:** `"Hãy xem 5 ca lỗi thực tế để hiểu nguyên nhân."` $\to$ Bấm `Space`.

---

### Slide 14: Empirical Failure Modes (`14_failure_archetypes.tex`)
- **Thời lượng:** `11:00 – 12:05` (65s)
- **Trên màn hình:** Bảng Table 6 gồm 5 ca lỗi: Q07, Q01, Q05, Q13, Q19.
- **Thao tác:** `[MOUSE]:` Rê chuột qua từng mã: Q07 $\to$ Q01 $\to$ Q05 $\to$ Q13 $\to$ Q19.

#### Tiếng Việt:
> "Bảng Table 6 tổng hợp 5 ca lỗi tiêu biểu ở từng bước: `[MOUSE: Bảng]`  
> 1. **Q07 — Sót khi tìm kiếm:** Đoạn khung điểm rèn luyện 65–79 nằm ngoài Top-5, nên mô hình đoán bừa là '50 điểm' cho sinh viên 68 điểm.  
> 2. **Q01 — Nhiễu từ khóa:** Đoạn tiếng Anh ở hạng 2 làm TF-IDF/BM25 bị phân tâm khỏi Điều 3 ở hạng 1.  
> 3. **Q05 — Cắt mất điều kiện:** Mô hình nhận đủ Điều 19 nhưng chỉ nói cần đủ tín chỉ để tốt nghiệp, bỏ sót điều kiện rèn luyện và quốc phòng.  
> 4. **Q13 — Đọc nhầm cột bảng:** Ở bảng học phí D03, mô hình đọc nhầm cột C1 (488k) thay vì C5 (1.014k vs 974k), tính ra chênh lệch 0 đồng.  
> 5. **Q19 — Bịa số hiệu:** Mô hình tự bịa ra số hiệu quyết định không có thật."

#### English:
> "Table 6 shows five failure types across the pipeline: `[MOUSE: Table]`  
> 1. **Q07 — Retrieval Miss:** The 65–79 conduct score chunk missed top-5, so the model guessed '50 points' for a 68-point score.  
> 2. **Q01 — Distractor Noise:** A rank-2 English rule distracted TF-IDF and BM25 away from Article 3.  
> 3. **Q05 — Missing Conditions:** The model got Article 19 but claimed credits alone are enough to graduate, skipping conduct and defense rules.  
> 4. **Q13 — Table Column Mix-up:** On tuition table D03, it read column C1 (488k) instead of C5 (1,014k vs.\ 974k), getting zero difference.  
> 5. **Q19 — Fake Metadata:** The model invented a decision number that does not exist."

- **Chuyển slide:** `"Từ 5 lỗi này, ta trả lời câu hỏi ban đầu."` $\to$ Bấm `Space`.

---

### Slide 15: Discussion: Does RAG Eliminate Hallucinations? (`15_discussion_hallucination.tex`)
- **Thời lượng:** `12:05 – 12:55` (50s)
- **Trên màn hình:** Hiện dần 3 phần qua **3 lần bấm Space**.
- **Thao tác:**
  - Lần 1: Hiện Câu hỏi & chữ **NO** đỏ.
  - Nói xong $\to$ `[BẤM SPACE LẦN 2]` hiện Phần 2.
  - Nói xong $\to$ `[BẤM SPACE LẦN 3]` hiện Phần 3.

#### Tiếng Việt:

> *(Trạng thái 1: Câu hỏi & chữ **NO** đỏ)*  
> "Quay lại câu hỏi đầu bài: **Đưa tài liệu bên ngoài vào có hết ảo giác không?** `[pause 1s]`  
> Câu trả lời là: `[nhấn mạnh]` **KHÔNG! RAG không xóa được ảo giác, mà chỉ đổi chỗ phát sinh lỗi.**"

> `[BẤM SPACE LẦN 2]` *(Hiện Phần 2)*  
> "RAG giúp sửa lỗi thiếu kiến thức, tăng độ đúng từ 0% lên 50%. Nhưng nó cho thấy **Ngụy biện Ngữ cảnh (The Grounding Fallacy)**: có tài liệu là *điều kiện cần*, chứ *chưa đủ* để đảm bảo câu trả lời đúng."

> `[BẤM SPACE LẦN 3]` *(Hiện Phần 3)*  
> "Lỗi giờ đây tích lũy qua từng bước: tìm sót, nhiễu đoạn, sót điều kiện và đọc nhầm bảng.  
> Điều này khớp với **GenXAI (Schneider, 2024)** và **RAGTruth (ACL 2024)**."

#### English:

> *(State 1: Question & red **NO**)*  
> "Back to our main question: **Does providing external documents eliminate hallucinations?** `[pause 1s]`  
> Our answer is: `[emphasize]` **NO! RAG does not remove hallucinations; it changes where they come from.**"

> `[PRESS SPACE 2ND TIME]` *(Reveals Part 2)*  
> "RAG fixes missing knowledge, lifting accuracy from 0% to 50%. But it shows **The Grounding Fallacy**: giving documents is *necessary*, not *sufficient*, for truthful answers."

> `[PRESS SPACE 3RD TIME]` *(Reveals Part 3)*  
> "Errors now build up across the pipeline: missed chunks, distractors, skipped conditions, and misread tables.  
> This matches **Schneider (2024, GenXAI)** and **RAGTruth (ACL 2024)**."

- **Chuyển slide:** `"Tiếp theo là các giới hạn của nghiên cứu."` $\to$ Bấm `Space`.

---

### Slide 16: Limitations (`16_limitations.tex`)
- **Thời lượng:** `12:55 – 13:45` (50s)
- **Trên màn hình:** 5 giới hạn của nghiên cứu.
- **Thao tác:** `[MOUSE]:` Rê chuột qua 5 dòng.

#### Tiếng Việt:
> "Nghiên cứu có **5 giới hạn** cần lưu ý: `[MOUSE: 5 bullets]`  
> 1. **Số câu hỏi ít:** Bộ test có 20 câu, nên mỗi câu đổi kết quả làm lệch 5.0%.  
> 2. **Phạm vi dữ liệu:** 51 trang từ 1 trường; 29 trang OCR chưa được kiểm tra lại từng chữ.  
> 3. **Cách chấm điểm:** Task 6 dùng GPT hỗ trợ chấm, chưa có người chấm mù độc lập.  
> 4. **Mô hình nhỏ:** Dùng Qwen 1.5B; các mô hình lớn hơn (7B/72B) sẽ đọc bảng tốt hơn.  
> 5. **Chi phí token:** RAG làm prompt dài từ 236 lên hơn 3.000 tokens — tốn chi phí và chậm hơn khoảng 12 lần."

#### English:
> "Our study has **five limitations**: `[MOUSE: 5 bullets]`  
> 1. **Small Benchmark:** With 20 queries, one question shifts accuracy by 5.0 percentage points.  
> 2. **Corpus Scope:** 51 pages from one university; 29 OCR pages were not checked character-by-character.  
> 3. **Grading:** Task 6 used GPT-assisted review without double-blind human grading.  
> 4. **Small Model:** We used Qwen 1.5B; larger models (7B/72B) handle tables better.  
> 5. **Token Cost:** Top-5 RAG grows prompts from 236 to over 3,000 tokens—about $12\times$ higher cost and latency."

- **Chuyển slide:** `"Từ đây, nhóm đề xuất hai hướng cải tiến."` $\to$ Bấm `Space`.

---

### Slide 17: Proposed Improvements (`17_verification_maintenance.tex`)
- **Thời lượng:** `13:45 – 14:30` (45s)
- **Trên màn hình:** 2 khối: Verification Loop (GenXAI) & Chuẩn hóa bảng, quản lý phiên bản.
- **Thao tác:** `[MOUSE]:` Chỉ tuple $\langle\text{Claim}, \text{Cohort}, \text{Chunk ID}, \text{Quote}\rangle$, rồi chỉ Khối 2.

#### Tiếng Việt:
> "Nhóm đề xuất hai giải pháp nâng cấp: `[MOUSE: Khối 1]`  
> 1. **Vòng lặp Hậu kiểm (GenXAI):**  
>    - Tách câu trả lời thành 4 phần: Luận điểm, Khóa áp dụng, Mã chunk và Trích dẫn gốc.  
>    - Dùng mô hình NLI kiểm tra đối chiếu; nếu thiếu bằng chứng thì tự động trả lời *'Không đủ thông tin'*.  
> 2. **Chuẩn hóa Bảng & Cập nhật Dữ liệu:** `[MOUSE: Khối 2]`  
>    - Chuyển bảng học phí nhiều cột thành dạng key-value để tránh đọc nhầm cột như Q13.  
>    - Dùng mã băm SHA-256 để tự động cập nhật khi có quy chế mới."

#### English:
> "We propose two improvements: `[MOUSE: Block 1]`  
> 1. **Verification Loop (GenXAI):**  
>    - Split answers into tuples: Claim, Applicable Cohort, Chunk ID, and Verbatim Quote.  
>    - Use an NLI check to verify support, and reply *'Insufficient information'* if ungrounded.  
> 2. **Table Formatting & Maintenance:** `[MOUSE: Block 2]`  
>    - Convert multi-column tables into key-value pairs to stop column mix-ups like Q13.  
>    - Track document versions with SHA-256 hashes to update the index automatically."

- **Chuyển slide:** `"Sau đây là 3 kết luận chính."` $\to$ Bấm `Space`.

---

### Slide 18: Conclusions (`18_conclusions.tex`)
- **Thời lượng:** `14:30 – 14:55` (25s)
- **Trên màn hình:** 4 ý tổng kết và câu chốt màu xanh ở đáy.
- **Thao tác:** `[MOUSE]:` Gạch dưới câu màu xanh ở đáy slide.

#### Tiếng Việt:
> "Nhóm xin chốt lại **3 ý chính**:  
> - **Thứ nhất:** RAG tăng độ chính xác từ 0% lên 50%.  
> - **Thứ hai:** BM25 tốt nhất ở Top-1 (Recall@1 = 80%), còn BGE-M3 tốt nhất ở Top-5 (Hit@5 = 95%).  
> - **Thứ ba:** `[MOUSE: Đáy slide, đọc rõ]` **Tài liệu bên ngoài giúp neo kiến thức cho LLM, nhưng chỉ có hậu kiểm chặt chẽ mới đảm bảo độ tin cậy.**"

#### English:
> "To wrap up, here are **three key takeaways**:  
> - **First:** RAG lifts accuracy from 0% to 50%.  
> - **Second:** BM25 leads top-1 precision (Recall@1 = 80%), while BGE-M3 leads top-5 coverage (Hit@5 = 95%).  
> - **Third:** `[MOUSE: Bottom line, clear]` **External documents ground LLMs, but only rigorous verification ensures reliability.**"

- **Chuyển slide:** Bấm `Space` sang Slide 19 (lướt 2s) $\to$ Bấm `Space` sang Slide 20.

---

### Slide 19 & 20: References & Thank You (`19_references.tex`, `20_qa.tex`)
- **Thời lượng:** `14:55 – 15:00` (5s)
- **Trên màn hình:** *Thank you for listening!* và *Any questions?*.
- **Thao tác:** `[ACTION]:` Nhìn webcam, cười, cảm ơn.

#### Tiếng Việt:
> "Toàn bộ code và dữ liệu đều có trên GitHub. Em cảm ơn Thầy và các bạn đã lắng nghe!  
> Nhóm em xin mời Thầy và các bạn đặt câu hỏi ạ."

#### English:
> "All code and data are on GitHub. Thank you for listening!  
> We are ready for your questions."

---

## Q&A Trực tuyến (Speaker 3: Tuấn Lĩnh)

1. **Q01: Đưa tài liệu vào có hết ảo giác không?**  
   - Không. Baseline đúng 0/20, RAG đạt 9–10/20 nhưng vẫn còn 30–40% câu chứa thông tin sai. Lỗi chuyển sang các bước trong pipeline.
2. **Q12: Trả lời đúng nội dung có đồng nghĩa trích dẫn đúng không?**  
   - Không. Cả 60 câu trả lời RAG đều thiếu mã citation hợp lệ; mã trên slide là do nhóm tự đối chiếu thêm vào.
3. **Q13: Nêu 3 ca lỗi điển hình?**  
   - Q07 (sót đoạn điểm 65–79), Q05 (bỏ sót điều kiện tốt nghiệp dù có Điều 19), Q13 (đọc nhầm cột C1 thay vì C5 ở bảng học phí).
4. **Q15: Hướng cải tiến hậu kiểm và cập nhật dữ liệu?**  
   - Dùng GenXAI kiểm tra tuple $\langle\text{Claim}, \text{Cohort}, \text{Chunk ID}, \text{Quote}\rangle$ qua NLI; chuyển bảng sang key-value; theo dõi phiên bản bằng SHA-256.
