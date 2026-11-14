# Kịch bản Thuyết trình Trực tuyến (Online Presentation Script) — Speaker 3

> **Hình thức:** Thuyết trình Trực tuyến (Google Meet / Zoom / MS Teams)  
> **Diễn giả:** Bùi Trọng Tuấn Lĩnh (`24125066`)  
> **Nhiệm vụ:** Trình bày Phần 3 — *Chất lượng Sinh ngữ 4 Nhánh, 5 Ca lỗi, Thảo luận & Hậu kiểm*  
> **Thời lượng quy định:** Đúng **05:00 phút** (từ `10:00` đến `15:00`)  
> **Phạm vi Slides:** Slide 13 đến Slide 20 (8 slides)  
> **Thiết lập Kỹ thuật:** Bật Unmute mic ngay khi Lê Huy kết thúc, kiểm tra webcam, dùng phím `Space` hoặc `Mũi tên phải` để chuyển slide và điều khiển **3 bước click tại Slide 15**, dùng **chuột (Mouse Cursor)** làm con trỏ chỉ dẫn bảng số liệu và lỗi sai.

---

## Bảng Phân bổ Thời gian & Pacing Checkpoints (Speaker 3)

| Slide | Tiêu đề Slide | Mốc thời gian | Thời lượng | Thao tác Trực tuyến (Online Actions) |
| :---: | :--- | :---: | :---: | :--- |
| **13** | Exp 2: 4-Way Answer Quality | `10:00 – 11:00` | 60s | Bật mic (Unmute), bấm `Space` sang Slide 13, rê chuột +45–50 pp. |
| **14** | 5 Failure Archetypes | `11:00 – 12:05` | 65s | Bấm `Space` sang Slide 14, chỉ chuột 5 ca lỗi (Q07, Q01, Q05, Q13, Q19). |
| **15** | Discussion: RAG vs Hallucination | `12:05 – 12:55` | 50s | Bấm `Space` sang Slide 15. **Slide này có 3 cú bấm Space hiện dần!** |
| **16** | Limitations & Boundaries | `12:55 – 13:45` | 50s | Bấm `Space` sang Slide 16, quét chuột 5 giới hạn nghiên cứu. |
| **17** | Verification & Maintenance | `13:45 – 14:30` | 45s | Bấm `Space` sang Slide 17, chỉ chuột tuple GenXAI & Bảng biểu. |
| **18** | Conclusions & Key Takeaways | `14:30 – 14:55` | 25s | Bấm `Space` sang Slide 18, chốt thông điệp màu xanh ở đáy slide. |
| **19** | Key References | `14:55 – 14:58` | 03s | Bấm `Space` lướt qua Slide 19 danh mục tài liệu tham khảo. |
| **20** | Thank You & Q&A | `14:58 – 15:00` | 02s | Bấm `Space` sang Slide 20, dứt lời cảm ơn, mời Thầy và các bạn đặt câu hỏi. |

> [!IMPORTANT]
> **Pacing Checkpoint Online (Mốc 14:30):** Khi đồng hồ bấm giờ chạm `14:30`, bạn **bắt buộc phải bấm sang Slide 18 (Conclusions)**. Hãy đọc dõng dạc câu thông điệp cốt lõi màu xanh ở đáy slide và kết thúc bài thuyết trình ở mốc `14:55 – 15:00`, không để chuông báo hết giờ ngắt lời.

---

## Chi tiết Kịch bản Từng Slide (Slide-by-Slide Delivery)

### Slide 13: Experiment 2: 4-Way Answer Quality (`13_generation_quality.tex`)
- **Thời lượng:** `10:00 – 11:00` (60 giây)
- **Hiển thị trên màn hình:** Bảng Table 5 trải dài toàn màn hình đối chiếu 4 nhánh trên 80 câu trả lời; dòng in đậm: *+45.0 to +50.0 pp accuracy gain over unaugmented baseline*.
- **Thao tác Trực tuyến:**
  - `[ACTION]:` Bật mic (Unmute), nhìn thẳng webcam, tư thế vững vàng.
  - `[BUTTON]:` Nhấn phím `Space` sang Slide 13.
  - `[MOUSE CURSOR]:` Chỉ chuột vào hàng Baseline ($0/20$), quét qua 3 hàng RAG ($10/20, 9/20, 10/20$), rồi chỉ vào cột cuối cùng ($0/20$ Valid Citations).

#### Kịch bản Thuyết trình (Tiếng Việt):
> "Dạ cảm ơn bạn Lê Huy. Kính thưa Thầy và các bạn, em là **Tuấn Lĩnh**, em xin phép tiếp nối phần 3 của bài báo cáo.  
> Trên slide là kết quả đánh giá chất lượng sinh ngữ trên toàn bộ **80 câu trả lời** từ thực nghiệm kiểm soát 4 nhánh của Task 6: `[MOUSE: Bảng]`  
> - **Hiệu quả vượt bậc của RAG:** Nhánh Baseline thuần tham số hoàn toàn bất lực trước quy chế trường, đạt **0/20 câu đúng (0%)** và có tới 75% câu chứa ảo giác bịa đặt. Khi được trang bị RAG, tỷ lệ đúng nội dung chính tăng vọt lên **50.0% ở TF-IDF và BGE-M3**, và **45.0% ở BM25** — tức tạo ra mức cải thiện từ **+45 đến +50 điểm phần trăm**.  
> - **Tỷ lệ phát biểu sai giảm mạnh:** Các khẳng định ngoài nguồn giảm từ 75% xuống chỉ còn 30% ở BGE-M3.  
> - **Tuy nhiên, hai điểm nghẽn thực nghiệm lớn lộ diện:**  
>   1. Dù BGE-M3 có Recall@5 áp đảo (89.17%), độ chính xác cuối cùng của nó vẫn bị chặn ở mức 50% (đồng hạng với TF-IDF).  
>   2. `[MOUSE: Cột cuối]` **Toàn bộ 60 câu trả lời RAG đều thất bại trong việc tự sinh mã citation-ID hợp lệ**, dù prompt đã ép khuôn rất chặt chẽ."

#### English Presentation Script:
> "Thank you, Le Huy. Moving to Part 3, I am **Tuan Linh**, and I will present our controlled evaluation of **80 generated answers** across four experimental conditions in Task 6: `[MOUSE: Table]`  
> - **The Dramatic Impact of RAG:** The purely parametric baseline completely fails on university regulations, scoring **0 / 20 correct (0%)** with a 75% hallucination rate. Augmenting with RAG dramatically elevates core factual accuracy to **50.0% for TF-IDF and BGE-M3**, and **45.0% for BM25** — representing a massive **+45 to +50 percentage point lift**.  
> - **Substantial Reduction in Hallucination:** Unsupported claims decrease from 75% down to 30% under BGE-M3.  
> - **However, two critical bottlenecks emerge:**  
>   1. Despite leading Evidence Recall@5 (89.17%), BGE-M3 ties with TF-IDF at 50% answer accuracy.  
>   2. `[MOUSE: Last column]` **All 60 RAG completions failed to autonomously generate valid citation identifiers**, exposing a fundamental instruction-following limitation."

- **Transition Cue:** `"Để hiểu vì sao Recall cao mà độ chính xác vẫn dừng ở 50%, chúng ta hãy cùng mổ xẻ 5 ca lỗi thực tế."`  
  `[ACTION]:` Nhấn `Space` sang Slide 14.

---

### Slide 14: Empirical Failure Modes: 5 Representative Cases (`14_failure_archetypes.tex`)
- **Thời lượng:** `11:00 – 12:05` (65 giây)
- **Hiển thị trên màn hình:** Bảng 5 ca lỗi thực tế Table 6: Q07, Q01, Q05, Q13, Q19 kèm nguyên nhân gốc rễ.
- **Thao tác Trực tuyến:**
  - `[MOUSE CURSOR]:` Lần lượt rà chuột qua từng mã câu hỏi: Q07 $\to$ Q01 $\to$ Q05 $\to$ Q13 $\to$ Q19.

#### Kịch bản Thuyết trình (Tiếng Việt):
> "Bảng Table 6 tổng hợp 5 ca lỗi điển hình đại diện cho sự cố tại từng mắt xích trong pipeline: `[MOUSE: Bảng]`  
> 1. **Q07 — Lỗi Bỏ sót Truy xuất (Retrieval Omission):** Bằng chứng về khung điểm rèn luyện Khá (65–79 điểm) nằm ngoài Top-5, khiến mô hình tự suy diễn thành '50 điểm' cho sinh viên đạt 68 điểm.  
> 2. **Q01 — Lỗi Nhiễu Từ khóa (Distractor Interference):** Dù đoạn Điều 3 xếp hạng 1, nhưng đoạn về chuẩn tiếng Anh ở hạng 2 có từ khóa tương đồng đã làm mô hình TF-IDF/BM25 bị phân tâm, sinh sai trọng tâm.  
> 3. **Q05 — Lỗi Cắt gọt Điều kiện (Condition Pruning):** Mô hình nhận đủ Điều 19 nhưng tự ý kết luận rằng chỉ cần tích lũy đủ tín chỉ là tốt nghiệp, bỏ sót hoàn toàn tiêu chuẩn đạo đức và giáo dục quốc phòng.  
> 4. **Q13 — Lỗi Đọc lệch Cột Bảng (Tabular Misalignment):** Với bảng học phí phức tạp D03, mô hình đọc nhầm sang cột C1 (488.000đ) thay vì cột C5 (1.014.000đ và 974.000đ), dẫn đến tính sai chênh lệch thành 0 đồng.  
> 5. **Q19 — Lỗi Bịa đặt Metadata:** Mô hình tự tạo ra số hiệu quyết định không hề tồn tại trong văn bản."

#### English Presentation Script:
> "Table 6 details five representative failure archetypes tracing errors across the entire pipeline: `[MOUSE: Table]`  
> 1. **Q07 — Retrieval Omission:** The chunk containing the 65–79 conduct score band fell outside top-5; lacking evidence, the generator fabricated an 'average 50 points' for a 68-point score.  
> 2. **Q01 — Distractor Interference:** Although Article 3 ranked first, an adjacent English prerequisite chunk at rank 2 distracted TF-IDF and BM25 into irrelevant topics.  
> 3. **Q05 — Condition Pruning:** The model received Article 19 but asserted that credit accumulation alone suffices for graduation, omitting disciplinary criteria and physical education.  
> 4. **Q13 — Tabular Misalignment:** When interpreting tuition table D03, the generator misread column C1 (488k) instead of column C5 (1,014k vs.\ 974k), falsely concluding zero difference.  
> 5. **Q19 — Metadata Hallucination:** The model hallucinated a non-existent administrative decision suffix number."

- **Transition Cue:** `"Từ 5 ca lỗi thực nghiệm này, chúng ta có thể trả lời trực diện câu hỏi nghiên cứu định hướng ban đầu."`  
  `[ACTION]:` Nhấn `Space` sang Slide 15.

---

### Slide 15: Discussion: Does RAG Eliminate Hallucinations? (`15_discussion_hallucination.tex`)
- **Thời lượng:** `12:05 – 12:55` (50 giây)
- **Hiển thị trên màn hình:** Slide có hiệu ứng hiện dần 3 phần qua từng cú bấm phím.
- **Thao tác Trực tuyến (ĐẶC BIỆT LƯU Ý 3 LẦN BẤM SPACE):**
  - Khi vừa sang Slide 15 (Lần 1): Màn hình chỉ có Câu hỏi & chữ **NO** đỏ.
  - Nói xong câu đầu $\to$ `[BẤM SPACE LẦN 2]` để hiện Phần 2 (2 bullets về Paradigm Shift & Grounding Fallacy).
  - Nói xong Phần 2 $\to$ `[BẤM SPACE LẦN 3]` để hiện Phần 3 (2 bullets về Cascading Errors & Y văn).

#### Kịch bản Thuyết trình (Tiếng Việt):

> *(Màn hình đang ở Trạng thái 1: Chỉ có Câu hỏi & chữ **NO** màu đỏ)*  
> "Quay trở lại câu hỏi nghiên cứu cốt lõi được đặt ra ở đầu bài: **Việc cung cấp tài liệu bên ngoài có thực sự loại bỏ ảo giác trong mô hình ngôn ngữ hay không?** `[pause 1s]`  
> Dựa trên toàn bộ kết quả thực nghiệm độc lập, câu trả lời dứt khoát của nhóm em là: `[nhấn mạnh]` **KHÔNG! RAG không triệt tiêu ảo giác, mà nó dịch chuyển bản chất và nguồn gốc phát sinh lỗi.**"

> `[ACTION]:` `[BẤM SPACE LẦN 2: HIỆN PHẦN 2]` *(Màn hình hiện thêm 2 bullets)*  
> "Thứ nhất, RAG giải quyết được sự thiếu hụt kiến thức tham số, giúp tỷ lệ đúng tăng từ 0% lên 50%. Nhưng nó lập tức làm nảy sinh **Ngụy biện về Ngữ cảnh (The Grounding Fallacy)**: Cung cấp tài liệu chỉ là *điều kiện cần*, hoàn toàn *không phải điều kiện đủ* để đảm bảo tính trung thực khách quan."

> `[ACTION]:` `[BẤM SPACE LẦN 3: HIỆN PHẦN 3]` *(Màn hình hiện thêm 2 bullets cuối)*  
> "Thứ hai, ảo giác giờ đây bắt nguồn từ chuỗi sai số tích lũy: từ việc bỏ sót bằng chứng, nhiễu từ khóa, đến việc cắt gọt điều kiện và đọc sai bảng biểu.  
> Kết luận này hoàn toàn tương đồng với phát hiện trong khung lý thuyết **GenXAI của Schneider (2024)** và tập ngữ liệu **RAGTruth tại ACL 2024**."

#### English Presentation Script:

> *(State 1: Header, Question & bold red **NO**)*  
> "Returning to our central guiding research question: **Does providing external documents eliminate hallucinations in language models?** `[pause 1s]`  
> Based on our rigorous empirical evidence, our definitive answer is: `[emphasize]` **NO! RAG does not eliminate hallucinations; it fundamentally transforms their nature and origin.**"

> `[ACTION]:` `[PRESS SPACE 2ND TIME: REVEAL PART 2]` *(Reveals Paradigm Shift & Grounding Fallacy)*  
> "First, RAG successfully bridges the parametric knowledge void, boosting accuracy from 0% to 50%. However, it exposes **The Grounding Fallacy**: providing relevant source documents is a *necessary* condition, but by no means a *sufficient* condition for factual truthfulness."

> `[ACTION]:` `[PRESS SPACE 3RD TIME: REVEAL PART 3]` *(Reveals Cascading Errors & Literature)*  
> "Second, hallucinations now cascade through pipeline failure points: retrieval misses, distractor confusion, condition pruning, and tabular misalignments.  
> This observation strongly corroborates the theoretical framework of **Schneider (2024, GenXAI)** and empirical findings from **RAGTruth (ACL 2024)**."

- **Transition Cue:** `"Để đánh giá kết quả này một cách khách quan, chúng ta cần nhìn nhận các giới hạn của nghiên cứu."`  
  `[ACTION]:` Nhấn `Space` sang Slide 16.

---

### Slide 16: Limitations & Applicability Boundaries (`16_limitations.tex`)
- **Thời lượng:** `12:55 – 13:45` (50 giây)
- **Hiển thị trên màn hình:** 5 gạch đầu dòng về cỡ mẫu 20 câu, 51 trang/29 trang OCR, đánh giá GPT, mô hình 1.5B, chi phí context.
- **Thao tác Trực tuyến:**
  - `[MOUSE CURSOR]:` Lần lượt di chuột qua 5 gạch đầu dòng.

#### Kịch bản Thuyết trình (Tiếng Việt):
> "Tuân thủ nghiêm ngặt chuẩn mực nghiên cứu khoa học, nhóm em thẳng thắn công bố **5 giới hạn của đề tài**: `[MOUSE: 5 bullets]`  
> 1. **Quy mô Benchmark:** Bộ câu hỏi gồm 20 câu, nghĩa là mỗi câu thay đổi kết quả sẽ làm dịch chuyển điểm số 5.0%. Cần thận trọng khi khái quát hóa kết luận.  
> 2. **Phạm vi Ngữ liệu:** 51 trang quy chế thuộc một trường đại học; 29 trang xử lý bằng OCR chưa được rà soát thủ công ở mức từng ký tự.  
> 3. **Phương pháp Đánh giá:** Điểm số Task 6 dựa trên thẩm định định tính có sự hỗ trợ của GPT (provisional review), chưa có vòng chấm mù độc lập (double-blind human review).  
> 4. **Năng lực Generator:** Thực nghiệm thực hiện trên mô hình nhỏ Qwen 1.5B; các mô hình lớn hơn như 7B hay 72B có thể suy luận bảng biểu tốt hơn.  
> 5. **Chi phí Ngữ cảnh:** RAG làm tăng chiều dài prompt từ 236 lên hơn 3.000 tokens — tức tăng độ trễ và chi phí API gấp hơn 12 lần."

#### English Presentation Script:
> "In accordance with academic rigor, we openly state **five limitations of our empirical study**: `[MOUSE: 5 bullets]`  
> 1. **Benchmark Scale:** Our benchmark comprises 20 curated queries, where a single question shift alters accuracy by 5.0 percentage points, necessitating cautious statistical interpretation.  
> 2. **Corpus Scope:** 51 pages from a single university; 29 OCR-processed pages lack exhaustive token-level human audit.  
> 3. **Review Methodology:** Factual accuracy scores stem from automated GPT-based qualitative review without double-blind human cross-annotation.  
> 4. **Generator Capacity:** Evaluated on a frozen 1.5B model; larger backbones (7B/72B) may exhibit superior tabular comprehension.  
> 5. **Context Overhead:** Top-5 RAG expands prompt length from 236 to over 3,000 tokens — representing an approximate $12\times$ latency and cost overhead."

- **Transition Cue:** `"Từ những hạn chế và ca lỗi thực tế này, nhóm đề xuất các giải pháp khắc phục cụ thể."`  
  `[ACTION]:` Nhấn `Space` sang Slide 17.

---

### Slide 17: Proposed Improvements: Verification & Maintenance (`17_verification_maintenance.tex`)
- **Thời lượng:** `13:45 – 14:30` (45 giây)
- **Hiển thị trên màn hình:** 2 khối đề xuất: Hậu kiểm Verification Loop (GenXAI) & Chuẩn hóa Bảng biểu, Sổ đăng ký phiên bản.
- **Thao tác Trực tuyến:**
  - `[MOUSE CURSOR]:` Chỉ chuột vào tuple 4 thành phần $\langle\text{Claim}, \text{Cohort}, \text{Chunk ID}, \text{Quote}\rangle$, sau đó chuyển sang khối 2.

#### Kịch bản Thuyết trình (Tiếng Việt):
> "Để RAG trở thành hệ thống đáng tin cậy trong môi trường hành chính, nhóm đề xuất hai giải pháp nâng cấp: `[MOUSE: Khối 1]`  
> 1. **Vòng lặp Hậu kiểm (Post-Generation Verification Loop theo GenXAI):**  
>    - Bóc tách câu trả lời thành các tuple nguyên tử: gồm Luận điểm, Khóa áp dụng, Mã chunk và Trích dẫn nguyên văn.  
>    - Áp dụng mô hình Natural Language Inference (NLI) để kiểm tra quan hệ kéo theo (entailment); nếu luận điểm không được bảo chứng 100% bởi trích dẫn, hệ thống sẽ tự động kích hoạt cơ chế từ chối trả lời an toàn (*'Thông tin chưa đủ căn cứ'*).  
> 2. **Tiền xử lý Bảng biểu & Quản trị Tri thức:** `[MOUSE: Khối 2]`  
>    - Chuyển đổi các bảng học phí đa cột thành cấu trúc Markdown/JSON key-value có gắn chặt tiêu đề cột để triệt tiêu lỗi đọc lệch cột như ở Q13.  
>    - Xây dựng sổ đăng ký phiên bản quy chế với mã băm SHA-256 để tự động cập nhật vector index khi có quyết định mới."

#### English Presentation Script:
> "To transform RAG into a dependable administrative decision system, we propose two architectural enhancements: `[MOUSE: Block 1]`  
> 1. **Post-Generation Verification Loop (Schneider, 2024 — GenXAI):**  
>    - Deconstruct model completions into atomic verifiable tuples: Claim, Applicable Cohort, Chunk ID, and Verbatim Quote.  
>    - Employ a Natural Language Inference (NLI) gate to verify factual entailment, triggering automatic abstention (*'Insufficient information'*) whenever evidence is lacking.  
> 2. **Tabular Structuring & Knowledge Base Maintenance:** `[MOUSE: Block 2]`  
>    - Convert complex multi-column tuition matrices into explicit key-value schemas to eliminate column misalignment (as in Q13).  
>    - Establish a versioned regulatory registry with SHA-256 hashes to automate index diffs whenever new circulars are enacted."

- **Transition Cue:** `"Sau đây là 4 thông điệp đúc kết của toàn bộ nghiên cứu."`  
  `[ACTION]:` Nhấn `Space` sang Slide 18.

---

### Slide 18: Conclusions & Core Takeaways (`18_conclusions.tex`)
- **Thời lượng:** `14:30 – 14:55` (25 giây)
- **Hiển thị trên màn hình:** 4 gạch đầu dòng đúc kết, câu thông điệp cốt lõi in đậm màu xanh ở đáy slide.
- **Thao tác Trực tuyến:**
  - `[MOUSE CURSOR]:` Rê chuột gạch dưới dòng chữ màu xanh ở đáy slide.
  - `[TONE]:` Đĩnh đạc, dõng dạc, dứt khoát.

#### Kịch bản Thuyết trình (Tiếng Việt):
> "Để khép lại bài thuyết trình, nhóm xin đúc kết **3 thông điệp then chốt**:  
> - **Thứ nhất:** RAG nâng độ chính xác thực tế từ 0% lên 50%, là cầu nối vững chắc bù đắp thiếu hụt kiến thức cho LLM.  
> - **Thứ hai:** BM25 vượt trội ở độ chính xác Top-1 (Recall@1 = 80%), trong khi BGE-M3 dẫn đầu ở độ phủ Top-5 (Hit@5 = 95%).  
> - **Thứ ba:** `[MOUSE: Đáy slide, đọc chậm và rõ]` **Cung cấp tài liệu bên ngoài giúp neo kiến thức cho mô hình, nhưng chỉ có cơ chế hậu kiểm khắt khe mới đảm bảo được sự tin cậy.**"

#### English Presentation Script:
> "In conclusion, our research delivers **three core takeaways**:  
> - **First:** RAG elevates empirical accuracy from 0% to 50%, effectively closing the parametric knowledge gap.  
> - **Second:** BM25 dominates top-1 precision (Recall@1 = 80%), while BGE-M3 maximizes aggregate coverage (Hit@5 = 95%).  
> - **Third:** `[MOUSE: Bottom line, slow and clear]` **External documents ground LLMs, but only rigorous verification ensures reliability.**"

- **Transition Cue:**  
  `[ACTION]:` Nhấn `Space` sang Slide 19 (lướt 2 giây) $\to$ Nhấn `Space` sang Slide 20.

---

### Slide 19 & 20: References & Thank You (`19_references.tex`, `20_qa.tex`)
- **Thời lượng:** `14:55 – 15:00` (5 giây)
- **Hiển thị trên màn hình:** Slide 20 hiển thị to, rõ: *Thank you for listening!* và *Any questions?*.
- **Thao tác Trực tuyến:**
  - `[ACTION]:` Nhìn thẳng vào webcam, tươi cười, gửi lời cảm ơn và mời tương tác qua mic hoặc khung chat.

#### Kịch bản Thuyết trình (Tiếng Việt):
> "Toàn bộ mã nguồn, dữ liệu thực nghiệm và báo cáo đã được lưu trữ công khai trên GitHub. Nhóm chúng em xin chân thành cảm ơn Thầy và các bạn đã chú ý lắng nghe!  
> Cả 3 thành viên nhóm em đã sẵn sàng tiếp nhận các câu hỏi phản biện từ Thầy và các bạn qua micro hoặc hộp thoại chat ạ!"

#### English Presentation Script:
> "All datasets, generation logs, and code artifacts are publicly available on GitHub. Thank you very much for your attention!  
> Our team is now fully prepared and welcomes any questions from the Professor and classmates via microphone or chat!"

---

## Chuẩn bị Hỏi & Đáp Q&A Trực tuyến (Speaker 3: Tuấn Lĩnh)

Khi bước vào phiên Q&A trực tuyến (15:00 – 20:00), Tuấn Lĩnh bật mic trả lời chính 4 câu hỏi then chốt về lỗi và độ tin cậy:
1. **Q01: Cung cấp tài liệu bên ngoài có loại bỏ hoàn toàn hallucination không?**
   - *Key Point:* Dứt khoát là KHÔNG. Nêu dẫn chứng bảng Task 6: Baseline đúng 0/20, RAG đạt 9–10/20 (vẫn còn 30–40% câu có phát biểu sai). RAG dịch chuyển lỗi sang pipeline.
2. **Q12: Câu trả lời đúng nội dung có đồng nghĩa với việc mô hình sinh citation đúng không?**
   - *Key Point:* Không. Phân biệt rõ đúng nội dung và truy vết nguồn gốc. Toàn bộ 60 đáp án RAG đều thiếu citation-ID hợp lệ. Trích dẫn trên slide là do nhóm đối chiếu thêm vào.
3. **Q13: Nêu 3 ca lỗi thực tế điển hình và phân tích nguyên nhân gốc rễ?**
   - *Key Point:* Nêu Q07 (missing threshold 65–79); Q05 (omission điều kiện tốt nghiệp dù có Điều 19); Q13 (đọc lệch cột C1 thay vì C5 ở bảng học phí).
4. **Q15: Nếu phát triển tiếp, nhóm đề xuất giải pháp hậu kiểm và cập nhật tài liệu ra sao?**
   - *Key Point:* GenXAI Verification Loop bóc tách tuple $\langle\text{Claim}, \text{Cohort}, \text{Chunk ID}, \text{Quote}\rangle$ qua NLI; chuẩn hóa bảng biểu thành JSON key-value; xây dựng sổ đăng ký phiên bản SHA-256.
