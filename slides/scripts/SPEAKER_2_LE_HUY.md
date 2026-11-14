# Kịch bản Thuyết trình Trực tuyến (Online Presentation Script) — Speaker 2

> **Hình thức:** Thuyết trình Trực tuyến (Google Meet / Zoom / MS Teams)  
> **Diễn giả:** Trần Đăng Lê Huy (`24125057`)  
> **Nhiệm vụ:** Trình bày Phần 2 — *Corpus HCMUS, Thực nghiệm Retrieval & Worked Example Q01*  
> **Thời lượng quy định:** Đúng **05:00 phút** (từ `05:00` đến `10:00`)  
> **Phạm vi Slides:** Slide 08 đến Slide 12 (5 slides)  
> **Thiết lập Kỹ thuật:** Bật Unmute mic ngay khi Nam Kiệt kết thúc, kiểm tra webcam sáng rõ, dùng **chuột (Mouse Cursor)** làm con trỏ chỉ dẫn bảng số liệu và ranking.

---

## Bảng Phân bổ Thời gian & Pacing Checkpoints (Speaker 2)

| Slide | Tiêu đề Slide | Mốc thời gian | Thời lượng | Thao tác Trực tuyến (Online Actions) |
| :---: | :--- | :---: | :---: | :--- |
| **08** | HCMUS Regulatory Corpus | `05:00 – 05:55` | 55s | Bật mic (Unmute), bấm `Space` sang Slide 08, rê chuột 4 văn bản. |
| **09** | Retrieval Setup & Protocol | `05:55 – 06:45` | 50s | Bấm `Space` sang Slide 09, chỉ chuột vào 4 chỉ số đánh giá. |
| **10** | Exp 1: Retrieval Benchmark | `06:45 – 07:45` | 60s | Bấm `Space` sang Slide 10, khoanh chuột BM25 80% vs BGE-M3 89.17%. |
| **11** | Worked Example Q01 Retrieval | `07:45 – 08:50` | 65s | Bấm `Space` sang Slide 11, chỉ chuột vào Hạng 1 Cosine 0.6271. |
| **12** | Worked Example Q01 Output | `08:50 – 09:55` | 65s | Bấm `Space` sang Slide 12, đối chiếu Baseline 0/2 vs RAG 2/2. |
| **--** | **Online Handoff** | `09:55 – 10:00` | 05s | Bàn giao lời và nhắc bạn Tuấn Lĩnh bật mic tiếp quản. |

> [!TIP]
> **Pacing Checkpoint Online (Mốc 08:50):** Khi đồng hồ chạm `08:50`, bạn **bắt buộc phải đang ở Slide 12**. Tập trung nêu bật sự đối lập: Baseline (suy diễn sai môn nào cũng phải thi đạt) vs Grounded RAG (nêu đúng tiên quyết phải thi đạt, học trước chỉ cần hoàn thành quá trình học). Sau đó bàn giao đúng `09:55 – 10:00`.

---

## Chi tiết Kịch bản Từng Slide (Slide-by-Slide Delivery)

### Slide 08: Experimental Corpus: HCMUS Regulations (`08_corpus.tex`)
- **Thời lượng:** `05:00 – 05:55` (55 giây)
- **Hiển thị trên màn hình:** Bảng 4 văn bản quy chế D01–D04 (51 trang, 162 chunks, trần 800 tokens); Benchmark 20 câu / 30 gold evidence.
- **Thao tác Trực tuyến:**
  - `[ACTION]:` Bật mic (Unmute), nhìn thẳng webcam, phong thái mạch lạc.
  - `[BUTTON]:` Nhấn phím `Space` (hoặc báo *"Nhờ Kiệt chuyển slide 8 giúp mình"*) sang Slide 08.
  - `[MOUSE CURSOR]:` Lướt chuột qua 4 văn bản D01, D02, D03, D04 trên bảng.

#### Kịch bản Thuyết trình (Tiếng Việt):
> "Dạ cảm ơn bạn Kiệt. Kính thưa Thầy và các bạn, em là **Lê Huy**, em xin phép trình bày phần thực nghiệm của đề tài.  
> Để kiểm chứng mô hình RAG trên môi trường hành chính học thuật thực tế, nhóm em đã thu thập và chuẩn hóa **4 văn bản quy chế chính thức của Trường ĐH Khoa học Tự nhiên**: `[MOUSE: Bảng]`  
> 1. **D01:** Quy chế đào tạo trình độ đại học năm 2026 (21 trang).  
> 2. **D02:** Quy chế đánh giá điểm rèn luyện 2020 và bản sửa đổi 2023 (16 trang).  
> 3. **D03:** Định mức học phí năm học 2026–2027 cho khóa 2022 trở về sau (5 trang).  
> 4. **D04:** Chuẩn ngoại ngữ trong quá trình học và khi tốt nghiệp (9 trang).  
> Tổng quy mô là **51 trang văn bản pháp lý** — mở rộng hơn so với gợi ý 5–10 trang của đề bài nhằm thử thách khả năng định vị điều khoản chéo.  
> Toàn bộ tài liệu được cấu trúc thành 80 điều mục và chia thành **162 chunks** dưới trần 800 token `cl100k_base`.  
> Đi kèm là bộ benchmark gồm **20 câu hỏi đa dạng** với **30 nhóm bằng chứng vàng (gold evidence)** được đối chiếu độc lập và cách ly hoàn toàn khỏi chỉ mục tìm kiếm."

#### English Presentation Script:
> "Thank you, Kiệt. Good morning, Professor and everyone. I am **Le Huy**, and I will present the empirical evaluation of our research.  
> To evaluate RAG within a realistic institutional setting, our team collected and curated **four authoritative regulatory documents from HCMUS**: `[MOUSE: Table]`  
> 1. **D01:** Academic Regulations 2026 (21 pages).  
> 2. **D02:** Student Conduct Assessment Regulations 2020 & 2023 Amendment (16 pages).  
> 3. **D03:** Tuition Fee Rates for AY 2026–2027 for Cohort 2022 onwards (5 pages).  
> 4. **D04:** Foreign Language Exit Standards (9 pages).  
> The corpus spans **51 pages of administrative text** — exceeding the 5–10 page guideline to rigorously test cross-article retrieval.  
> The corpus was structured into 80 parent sections and segmented into **162 chunks** capped at an 800-token ceiling using the `cl100k_base` tokenizer.  
> We paired this corpus with an evaluation benchmark of **20 questions associated with 30 gold evidence groups**, strictly sequestered from the search index."

- **Transition Cue:** `"Tiếp theo, em xin giới thiệu 3 mô hình retrieval và giao thức đánh giá."`  
  `[ACTION]:` Nhấn `Space` sang Slide 09.

---

### Slide 09: Retrieval Configurations & Evaluation Protocol (`09_retrieval_setup.tex`)
- **Thời lượng:** `05:55 – 06:45` (50 giây)
- **Hiển thị trên màn hình:** Bảng 3 cấu hình TF-IDF, BM25, Dense BGE-M3; định nghĩa 4 chỉ số retrieval tại $k \in \{1, 3, 5\}$.
- **Thao tác Trực tuyến:**
  - `[MOUSE CURSOR]:` Chỉ chuột vào hàng BM25 ($k_1=1.5, b=0.75$), sau đó chỉ vào 1024 chiều của BGE-M3.

#### Kịch bản Thuyết trình (Tiếng Việt):
> "Nhóm triển khai thực nghiệm đối sánh độc lập 3 đại diện tiêu biểu cho bước Retrieval: `[MOUSE: Bảng]`  
> - **TF-IDF:** Mô hình từ khóa thưa cơ bản, sử dụng tần suất unigram, bigram và khoảng cách cosine.  
> - **BM25:** Mô hình từ khóa nâng cao, có cơ chế bão hòa tần suất từ ($k_1=1.5$) và phạt độ dài văn bản ($b=0.75$).  
> - **BGE-M3:** Mô hình nhúng ngôn ngữ dày đặc (Dense Neural Embedding), ánh xạ văn bản thành vector chuẩn hóa 1024 chiều.  
> Để đánh giá khoa học, nhóm đo lường 4 chỉ số macro trên 20 câu hỏi tại các ngưỡng $k = 1, 3, 5$:  
> - **Evidence Recall@$k$:** Tỷ lệ nhóm bằng chứng vàng tìm được trên tổng số bằng chứng bắt buộc.  
> - **Hit Rate@$k$:** Tỷ lệ câu hỏi tìm được ít nhất một bằng chứng liên quan.  
> - **All Evidence Hit@$k$:** Tỷ lệ câu hỏi tìm đủ 100% bằng chứng.  
> - **MRR@$k$:** Thứ hạng nghịch đảo của bằng chứng đầu tiên."

#### English Presentation Script:
> "We implemented and benchmarked three distinct retrieval models: `[MOUSE: Table]`  
> - **TF-IDF:** Standard sparse baseline using unigram and bigram term weighting with sublinear TF.  
> - **BM25:** Advanced lexical model incorporating term saturation ($k_1=1.5$) and document length normalization ($b=0.75$).  
> - **BGE-M3:** State-of-the-art multilingual dense embedding model mapping texts into normalized 1024-dimensional vectors.  
> We evaluate retrieval performance across four macro-averaged metrics at cut-offs $k \in \{1, 3, 5\}$:  
> - **Evidence Recall@$k$:** The proportion of necessary gold evidence groups retrieved ($r/m$).  
> - **Hit Rate@$k$:** Binary check if at least one gold evidence group is found ($r \ge 1$).  
> - **All Evidence Hit@$k$:** Binary check if 100% of gold groups are present ($r = m$).  
> - **MRR@$k$:** The mean reciprocal rank of the first relevant chunk."

- **Transition Cue:** `"Sau đây là kết quả định lượng chi tiết của vòng thực nghiệm 1."`  
  `[ACTION]:` Nhấn `Space` sang Slide 10.

---

### Slide 10: Experiment 1: Retrieval Performance (`10_retrieval_results.tex`)
- **Thời lượng:** `06:45 – 07:45` (60 giây)
- **Hiển thị trên màn hình:** Bảng Table 4 trải dài 100% màn hình với các số liệu đơn nhất từng ô, 4 bullets phân tích.
- **Thao tác Trực tuyến:**
  - `[MOUSE CURSOR]:` Khoanh chuột vào con số **80.00%** của BM25 tại cột Recall@1, sau đó khoanh vào **89.17%** và **95.00%** của BGE-M3 tại $k=5$.
  - `[TONE]:` Nhấn giọng mạnh mẽ ở câu cảnh báo cuối cùng.

#### Kịch bản Thuyết trình (Tiếng Việt):
> "Bảng Table 4 trên slide thể hiện sự phân hóa rất rõ giữa hai trường phái:  
> - **BM25 áp đảo hoàn toàn ở thứ hạng đầu tiên:** `[MOUSE: Cột Recall@1]` BM25 đạt Recall@1 lên tới **80.00%** và MRR@5 đạt **0.8667**. Điều này chứng minh từ khóa chính xác là vũ khí cực mạnh để nhận diện mã hiệu điều luật như 'Điều 3' hay 'Khoản 3'.  
> - **Dense BGE-M3 dẫn đầu ở độ phủ Top-5:** `[MOUSE: Cột Recall@5]` Khi mở rộng đến $k=5$, BGE-M3 vươn lên dẫn đầu với Recall@5 đạt **89.17%** và Hit Rate@5 đạt tới **95.00%** nhờ khả năng bắt được ngữ nghĩa diễn đạt tự do của người hỏi.  
> - **Hiện tượng bão hòa:** Các phương pháp từ khóa bị chững lại từ $k=3$ đến $k=5$, trong khi BGE-M3 tiếp tục tăng thêm 7.5%.  
> `[nhấn mạnh]` **Tuy nhiên, bài học thực nghiệm đắt giá nhất ở đây là:** Hit@5 đạt 95% KHÔNG ĐỒNG NGHĨA câu trả lời đạt độ chính xác 95%! Quá trình sinh ngữ phía sau vẫn đối mặt với rất nhiều rủi ro."

#### English Presentation Script:
> "Table 4 illustrates a compelling trade-off between lexical precision and semantic coverage:  
> - **BM25 dominates early ranks:** `[MOUSE: Recall@1 column]` BM25 achieves a remarkable **80.00% Recall@1** and an MRR@5 of **0.8667**, demonstrating that exact lexical matching excels at locating specific regulatory clauses and article identifiers.  
> - **Dense BGE-M3 leads multi-passage coverage at $k=5$:** `[MOUSE: Recall@5 column]` BGE-M3 achieves the highest Recall@5 at **89.17%** and a 95.00% Hit Rate@5, successfully capturing semantic paraphrases.  
> - **Plateau Effect:** Lexical methods plateau beyond $k=3$, whereas BGE-M3 gains an additional 7.50 percentage points when expanding from $k=3$ to $k=5$.  
> `[emphasize]` **Crucial Takeaway:** A 95.00% Hit Rate@5 does NOT imply 95% answer accuracy! Downstream generation bottlenecks remain substantial."

- **Transition Cue:** `"Để thấy rõ sự phối hợp giữa Retriever và Generator, chúng ta cùng xem xét ví dụ thực tế tại câu hỏi Q01."`  
  `[ACTION]:` Nhấn `Space` sang Slide 11.

---

### Slide 11: Worked Example (Q01): Top-5 Candidate Chunks (`11_worked_example_retrieval.tex`)
- **Thời lượng:** `07:45 – 08:50` (65 giây)
- **Hiển thị trên màn hình:** Câu hỏi Q01 in đậm, bảng Top-5 chunks từ BGE-M3 (Rank 1 Cosine = 0.6271, trang 4 chứa Điều 3 Khoản 3(c)).
- **Thao tác Trực tuyến:**
  - `[MOUSE CURSOR]:` Chỉ vào câu hỏi Q01, sau đó chiếu thẳng vào Hạng 1 (`D01_regulation_article_3_03` - Cosine 0.6271).

#### Kịch bản Thuyết trình (Tiếng Việt):
> "Nhóm chọn câu hỏi benchmark **Q01**: `[MOUSE: Câu hỏi]`  
> *'Theo Quy chế 2026, học phần tiên quyết khác học phần học trước như thế nào?'*  
> Bảng trên slide là log xếp hạng thực tế của mô hình BGE-M3: `[MOUSE: Hàng 1]`  
> - **Hạng 1:** Mô hình xuất sắc đưa đúng đoạn chunk `D01_regulation_article_3_03` lên đầu với độ tương đồng Cosine là **0.6271** tại trang PDF số 4.  
> Đoạn văn này chứa **100% bằng chứng vàng**: Điều 3, Khoản 3(c) quy định:  
>   + Môn tiên quyết: bắt buộc sinh viên phải học và **'thi đạt'** mới được đăng ký môn học tiếp theo.  
>   + Môn học trước: chỉ yêu cầu sinh viên **'hoàn thành quá trình học tập'** (tức là đã tham gia học, không bắt buộc phải thi đạt ngay lúc đó).  
> - **Rủi ro Distractors:** `[MOUSE: Hàng 2--5]` Tuy nhiên, các vị trí từ Hạng 2 đến Hạng 5 lại là các điều khoản về miễn trừ tín chỉ và lập kế hoạch học tập, tiềm ẩn nguy cơ làm loãng sự chú ý của mô hình sinh."

#### English Presentation Script:
> "Let us examine benchmark query **Q01**: `[MOUSE: Question]`  
> *'According to the 2026 Academic Regulations, how does a prerequisite course differ from a pre-learning course?'*  
> This table shows the empirical dense retrieval ranking from BGE-M3: `[MOUSE: Rank 1]`  
> - **Rank 1:** BGE-M3 correctly placed chunk `D01_regulation_article_3_03` at the top with a Cosine Similarity of **0.6271** on PDF page 4.  
> This passage contains **100% of the gold evidence**: Article 3, Clause 3(c) states that:  
>   + A prerequisite course requires students to have enrolled and **'passed'** the exam before taking course A.  
>   + A pre-learning course merely requires students to have **'completed the study process'** (without strictly requiring a passing grade).  
> - **Distractor Contexts:** `[MOUSE: Ranks 2--5]` However, ranks 2 through 5 introduce adjacent articles on credit transfers and scheduling, presenting potential distractors."

- **Transition Cue:** `"Vậy khi nhận được 5 đoạn văn này, mô hình ngôn ngữ sẽ sinh câu trả lời ra sao so với điều kiện không có tài liệu?"`  
  `[ACTION]:` Nhấn `Space` sang Slide 12.

---

### Slide 12: Worked Example (Q01): Grounded vs. Baseline Output (`12_worked_example_generation.tex`)
- **Thời lượng:** `08:50 – 09:55` (65 giây)
- **Hiển thị trên màn hình:** Bảng đối chiếu 2 hàng giữa Baseline (0/2 điểm) và Grounded RAG (2/2 điểm), kèm lưu ý citation của người audit.
- **Thao tác Trực tuyến:**
  - `[MOUSE CURSOR]:` Chỉ vào hàng Baseline, sau đó chuyển sang hàng Grounded RAG, rê chuột dưới cụm từ *"thi đạt"* và *"hoàn thành quá trình học tập"*.

#### Kịch bản Thuyết trình (Tiếng Việt):
> "Bảng trên slide đối chiếu trực diện kết quả sinh ngữ từ mô hình **Qwen2.5-1.5B-Instruct**: `[MOUSE: Bảng]`  
> - **Nhánh Baseline (Không có RAG):** Đạt **0/2 điểm**. Do chỉ dựa vào trí nhớ tham số rỗng về quy chế trường, mô hình suy diễn cảm tính và khẳng định hoàn toàn sai lệch rằng: *cả hai môn đều phải thi đạt trên trung bình*.  
> - **Nhánh Grounded RAG (Có ngữ cảnh BGE-M3):** Đạt trọn vẹn **2/2 điểm**. Nhờ được tiếp sức bởi chunk Điều 3 Khoản 3(c), mô hình đã phân biệt chuẩn xác 100% bản chất pháp lý: tiên quyết bắt buộc phải **'thi đạt'**, còn học trước chỉ cần **'hoàn thành quá trình học tập'**.  
> - **Lưu ý học thuật rất quan trọng:** Cả 60 câu trả lời RAG của mô hình Qwen đều **không tự sinh được citation-ID hợp lệ**; mã trích dẫn `[D01_regulation_article_3_03]` trên slide là do **nhóm em kiểm tra đối soát và bổ sung sau (human attribution)**."

#### English Presentation Script:
> "This table directly contrasts completions from **Qwen2.5-1.5B-Instruct** across both conditions: `[MOUSE: Table]`  
> - **Baseline (No RAG):** Scores **0 / 2**. Relying solely on parametric memory, the model speculates inaccurately, falsely asserting that *both course types require passing grades*.  
> - **Grounded RAG (BGE-M3):** Scores **2 / 2**. Conditioned on the retrieved Article 3 context, the model correctly differentiates the legal criteria: prerequisite demands **'passing'** the course, whereas pre-learning only requires **'completing the coursework'**.  
> - **Academic Verification Note:** All 60 RAG responses from Qwen **failed to autonomously output valid citation IDs**; the tag `[D01_regulation_article_3_03]` shown on the slide was **verified and appended post-hoc by our team during manual audit**."

- **Online Handoff Cue (Chuyển giao Trực tuyến 2: 09:55 – 10:00):**  
  > `[ACTION]:` Nhìn thẳng vào webcam, nở nụ cười, chuyển giao lời nói:  
  > **Tiếng Việt:** *"Mặc dù câu hỏi Q01 rất thành công, nhưng trên toàn bộ 20 câu hỏi, hệ thống vẫn bộc lộ nhiều ca lỗi tinh vi. Sau đây em xin nhường lại mic cho bạn Tuấn Lĩnh. Mời bạn Lĩnh bật mic tiếp tục phân tích các failure cases thực tế ạ."*  
  > **English:** *"While query Q01 was successful, subtle failure modes persist across our benchmark. I will now hand over to Tuan Linh. Linh, please unmute and present our failure cases analysis."*  
  > `[ACTION]:` Tắt mic (Mute).

---

## Chuẩn bị Hỏi & Đáp Q&A Trực tuyến (Speaker 2: Lê Huy)

Khi bước vào phiên Q&A trực tuyến (15:00 – 20:00), Lê Huy bật mic trả lời chính các câu hỏi về dữ liệu và thực nghiệm:
1. **Q05: Corpus gồm những gì? Vì sao 51 trang trong khi đề gợi ý 5–10 trang?**
   - *Key Point:* Gồm 4 văn bản (Đào tạo 21p, Rèn luyện 16p, Học phí 5p, Ngoại ngữ 9p). Nhóm mở rộng để kiểm tra khả năng định vị điều khoản chéo trên toàn văn quy chế, tránh việc trích chọn cục bộ có định kiến.
2. **Q06: Vì sao chia theo cấu trúc và đặt trần 800 token?**
   - *Key Point:* Giữ trọn vẹn ngữ cảnh điều khoản cha-con và bảng biểu; trần 800 token `cl100k_base` (thực tế chunk lớn nhất là 788 tokens) đảm bảo chứa đủ ngữ cảnh mà không làm quá tải context window.
3. **Q08: Vì sao chọn top-5? Đã đáp ứng yêu cầu so sánh 2 cấu hình chưa?**
   - *Key Point:* Đã đánh giá retrieval tại $k=1, 3, 5$ (đáp ứng yêu cầu ít nhất 2 giá trị $k$). Khi sinh ngữ, nhóm cố định top-5 để kiểm soát biến số công bằng giữa 3 retriever.
4. **Q09: Hit Rate, Evidence Recall, All Evidence Hit và MRR khác nhau thế nào?**
   - *Key Point:* Hit Rate (có ít nhất 1 gold); Evidence Recall (tỷ lệ gold tìm được $r/m$); All Evidence (phải đủ 100% gold $r=m$); MRR (nghịch đảo thứ hạng chunk đúng đầu tiên).
5. **Q10: Giữa BM25 và BGE-M3, mô hình nào tốt hơn trên quy chế HCMUS?**
   - *Key Point:* Tùy mục tiêu: BM25 tốt nhất cho Top-1 (Recall@1 = 80%); BGE-M3 tốt nhất cho Top-5 coverage (Recall@5 = 89.17%, Hit@5 = 95%).
6. **Q11: So sánh có/không RAG có công bằng không? Vì sao dùng Qwen?**
   - *Key Point:* Cực kỳ công bằng: cùng chung model Qwen2.5-1.5B, cùng system prompt, cùng tham số greedy decoding (temperature=0, seed=42), cùng trần 768 tokens.
7. **Q14: Phương pháp đánh giá chất lượng câu trả lời là gì? Hạn chế là gì?**
   - *Key Point:* Đánh giá 3 mức (0: sai; 1: một phần; 2: đúng chính). Kết quả sơ bộ do GPT chấm có lý do chi tiết; hạn chế là chưa có chấm mù độc lập (double-blind).
