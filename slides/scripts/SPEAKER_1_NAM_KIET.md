# Kịch bản Thuyết trình Trực tuyến — Speaker 1

> **Hình thức:** Trực tuyến (Google Meet / Zoom / MS Teams)  
> **Diễn giả:** Trịnh Võ Nam Kiệt (`24125013`)  
> **Nhiệm vụ:** Phần 1 — *Lý thuyết Nền tảng, Pipeline & Mô hình Xác suất*  
> **Thời lượng:** **05:00 phút** (`00:00 – 05:00`) | **Slides:** 01–07  
> **Thiết lập:** Bật webcam, kiểm tra mic, share toàn màn hình (`Ctrl + L`), dùng chuột để chỉ dẫn.

---

## Bảng Thời gian & Checkpoints (Speaker 1)

| Slide | Tiêu đề | Mốc thời gian | Thời lượng | Thao tác |
| :---: | :--- | :---: | :---: | :--- |
| **01** | Title Page | `00:00 – 00:35` | 35s | Share màn hình, kiểm tra mic, mở đầu. |
| **02** | Outline | `00:35 – 01:00` | 25s | Bấm `Space`, rê chuột qua 3 phần. |
| **03** | Introduction | `01:00 – 01:50` | 50s | Bấm `Space`, chỉ chuột vào câu hỏi chính. |
| **04** | Grounding Paradigms | `01:50 – 02:40` | 50s | Bấm `Space`, rê chuột qua bảng 3 phương pháp. |
| **05** | RAG Architecture | `02:40 – 03:30` | 50s | Bấm `Space`, rê chuột theo sơ đồ 6 bước. |
| **06** | Probabilistic Modeling | `03:30 – 04:15` | 45s | Bấm `Space`, chỉ vào dấu $\sum$ và $\prod$. |
| **07** | Numerical Example | `04:15 – 04:55` | 40s | Bấm `Space`, chỉ vào **0.5280** và **0.4692**. |
| **--** | **Handoff** | `04:55 – 05:00` | 05s | Nhường lời cho Lê Huy. |

> [!TIP]
> **Checkpoint `04:15`:** Phải đang ở Slide 07. Chốt nhanh $0.5280$ vs $0.4692$ rồi nhường lời cho Huy đúng `04:55`.

---

## Chi tiết Từng Slide

### Slide 01: Title Page (`01_title.tex`)
- **Thời lượng:** `00:00 – 00:35` (35s)
- **Trên màn hình:** Slide bìa S07, tên 3 thành viên, FIT HCMUS.
- **Thao tác:** `[ACTION]:` Nhìn webcam, bật mic, đảm bảo đang Full Screen (`Ctrl + L`).

#### Tiếng Việt:
> "Dạ em chào Thầy và các bạn. Mọi người nghe rõ và thấy slide chưa ạ? `[pause 1s]` Dạ em cảm ơn.  
> Hôm nay nhóm em trình bày đề tài **S07: Retrieval-Augmented Generation (RAG)**.  
> Nhóm gồm 3 thành viên: em là **Nam Kiệt**, bạn **Lê Huy** và bạn **Tuấn Lĩnh**.  
> Nhóm em kết hợp lý thuyết xác suất RAG của Lewis (2020) với thực nghiệm trên 4 văn bản quy chế của trường Khoa học Tự nhiên."

#### English:
> "Good morning, Professor and classmates. Can everyone hear me and see the screen? `[pause 1s]` Great, thank you.  
> Today our team presents **S07: Retrieval-Augmented Generation (RAG)**.  
> Our team has three members: **Nam Kiet**, **Le Huy**, and **Tuan Linh**.  
> We combine the RAG theory from Lewis et al. (2020) with an empirical test on four official HCMUS regulation documents."

- **Chuyển slide:** `"Sau đây là lộ trình bài nói hôm nay."` $\to$ Bấm `Space`.

---

### Slide 02: Outline (`02_outline.tex`)
- **Thời lượng:** `00:35 – 01:00` (25s)
- **Trên màn hình:** 3 phần trình bày, mỗi người 5 phút.
- **Thao tác:** `[MOUSE]:` Rê chuột qua mục 1 $\to$ 2 $\to$ 3.

#### Tiếng Việt:
> "Bài nói 15 phút được chia đều 5 phút cho mỗi người:  
> - **Phần 1:** Em nói về lý thuyết nền tảng, pipeline và công thức Sequence/Token.  
> - **Phần 2:** Bạn Lê Huy trình bày bộ dữ liệu 51 trang quy chế HCMUS, so sánh 3 bộ tìm kiếm và ví dụ Q01.  
> - **Phần 3:** Bạn Tuấn Lĩnh phân tích chất lượng 80 câu trả lời, 5 lỗi thực tế và cách kiểm chứng GenXAI."

#### English:
> "Our 15-minute talk is split evenly—five minutes each:  
> - **Part 1:** I cover the theory, pipeline, and Sequence vs. Token math.  
> - **Part 2:** Le Huy presents our 51-page HCMUS corpus, compares three retrievers, and walks through Q01.  
> - **Part 3:** Tuan Linh analyzes answer quality, five failure cases, and our GenXAI verification loop."

- **Chuyển slide:** `"Chúng ta bắt đầu với câu hỏi nghiên cứu chính."` $\to$ Bấm `Space`.

---

### Slide 03: Introduction (`03_intro_question.tex`)
- **Thời lượng:** `01:00 – 01:50` (50s)
- **Trên màn hình:** Câu hỏi: *Does providing external documents eliminate hallucinations?* và 4 ý chính.
- **Thao tác:** `[MOUSE]:` Khoanh chuột quanh câu hỏi chính.

#### Tiếng Việt:
> "Các LLM hiện nay lưu toàn bộ kiến thức trong trọng số tĩnh (**Parametric Memory**). `[pause 1s]`  
> Vì vậy, mô hình dễ bị ảo giác, kiến thức cũ theo thời gian và không kiểm tra được nguồn.  
> RAG giải quyết bằng cách thêm **Non-parametric Memory** — một kho tài liệu bên ngoài dễ cập nhật mà không cần train lại.  
> Nhưng câu hỏi chính của nhóm là: `[nhấn mạnh]` **Đưa tài liệu bên ngoài vào có hết ảo giác không?** `[pause 1s]` Hay lỗi chỉ chuyển sang các bước khác trong hệ thống? Nhóm sẽ trả lời bằng số liệu thực nghiệm."

#### English:
> "Standard LLMs store all knowledge in static weights (**parametric memory**). `[pause 1s]`  
> Because of this, they hallucinate, get outdated, and cannot show sources.  
> RAG fixes this by adding **non-parametric memory**—an external document index that is easy to update without retraining.  
> Still, our main question is: `[emphasize]` **Does providing external documents eliminate hallucinations?** `[pause 1s]` Or does it just move errors into the pipeline? We will answer this with real test data."

- **Chuyển slide:** `"Trước tiên, hãy so sánh RAG với các cách khác."` $\to$ Bấm `Space`.

---

### Slide 04: Knowledge Grounding Paradigms (`04_paradigms.tex`)
- **Thời lượng:** `01:50 – 02:40` (50s)
- **Trên màn hình:** Bảng so sánh Fine-Tuning, Long-Context, RAG.
- **Thao tác:** `[MOUSE]:` Rê chuột qua từng hàng: Fine-Tuning $\to$ Long-Context $\to$ RAG.

#### Tiếng Việt:
> "Bảng này so sánh 3 cách đưa kiến thức vào LLM:  
> - **Fine-Tuning:** `[MOUSE: Hàng 1]` Sửa trực tiếp trọng số; tốn GPU, dễ quên kiến thức cũ, đổi quy chế là phải train lại.  
> - **Long-Context:** `[MOUSE: Hàng 2]` Nhét hết tài liệu vào prompt; tốn nhiều token và dễ sót ý ở giữa (*Lost-in-the-Middle*).  
> - **RAG:** `[MOUSE: Hàng 3]` Tách riêng phần sinh chữ (LLM) và phần lưu sự thật (kho tài liệu).  
> Trong bài báo gốc của Lewis (2020), RAG-Sequence đạt **44.5 Exact Match** trên Natural Questions, vượt mô hình **T5-11B** (36.6) lớn gấp 50 lần."

#### English:
> "This table compares three ways to ground LLMs:  
> - **Fine-Tuning** `[MOUSE: Row 1]` updates weights directly; it costs a lot of GPU time and needs retraining whenever rules change.  
> - **Long-Context** `[MOUSE: Row 2]` puts all text in the prompt; token cost grows fast, and models miss middle details (*Lost-in-the-Middle*).  
> - **RAG** `[MOUSE: Row 3]` separates language generation from fact storage, keeping prompts short and easy to update.  
> Lewis et al. (2020) showed RAG-Sequence reached **44.5 Exact Match** on Natural Questions, beating **T5-11B** (36.6), which is 50 times larger."

- **Chuyển slide:** `"Hệ thống RAG chạy qua 6 bước như sau."` $\to$ Bấm `Space`.

---

### Slide 05: RAG Architecture & Failures (`05_pipeline.tex`)
- **Thời lượng:** `02:40 – 03:30` (50s)
- **Trên màn hình:** Sơ đồ 6 bước và 3 nhóm lỗi.
- **Thao tác:** `[MOUSE]:` Rê chuột từ bước 1 đến bước 6.

#### Tiếng Việt:
> "Hệ thống RAG gồm 6 bước nối tiếp nhau. `[MOUSE: Sơ đồ]` Lỗi có thể xảy ra ở bất kỳ bước nào:  
> 1. **Trước truy xuất (Pre-Retrieval):** Quét OCR sai bảng biểu; hoặc cắt chunk làm tách rời ngoại lệ khỏi điều luật chính.  
> 2. **Truy xuất (Retrieval):** Bỏ sót đoạn đúng ngoài Top-$k$; hoặc bị đánh lừa bởi đoạn văn trùng từ khóa.  
> 3. **Sau truy xuất (Post-Retrieval):** Dù có đoạn đúng trong prompt, LLM vẫn có thể đọc nhầm cột bảng, bỏ sót điều kiện hoặc bịa mã trích dẫn."

#### English:
> "A standard RAG pipeline has six steps. `[MOUSE: Flow]` Errors can happen at any step:  
> 1. **Pre-Retrieval:** Bad OCR breaks tables; poor chunking splits exceptions from their main rules.  
> 2. **Retrieval:** Gold chunks fall outside top-$k$, or matching keywords trick the search.  
> 3. **Post-Retrieval:** Even with the right text in the prompt, the LLM can misread table columns, skip conditions, or fake citations."

- **Chuyển slide:** `"Tiếp theo là hai công thức xác suất của Lewis et al."` $\to$ Bấm `Space`.

---

### Slide 06: Probabilistic Modeling (`06_formulation.tex`)
- **Thời lượng:** `03:30 – 04:15` (45s)
- **Trên màn hình:** Công thức RAG-Sequence và RAG-Token.
- **Thao tác:** `[MOUSE]:` Chỉ dấu $\sum$ ngoài $\prod$ (Sequence), rồi dấu $\sum$ trong $\prod$ (Token).

#### Tiếng Việt:
> "Lewis và cộng sự xem tài liệu $z$ là biến ẩn, tính tổng xác suất trên Top-$k$ đoạn văn. `[pause 1s]`  
> Khác biệt chính là vị trí dấu tổng $\sum$ và dấu tích $\prod$:  
> - **RAG-Sequence:** `[MOUSE: Công thức 1]` Dấu $\sum$ ở ngoài. Cả câu trả lời $y$ dựa trên **cùng một tài liệu $z$**, giúp văn phong và ngữ cảnh thống nhất.  
> - **RAG-Token:** `[MOUSE: Công thức 2]` Dấu $\sum$ ở trong từng bước $i$. Mô hình đổi tài liệu linh hoạt ở mỗi từ, hợp để tổng hợp thông tin từ nhiều nguồn.  
> Mọi xác suất đều nằm trong $[0, 1]$."

#### English:
> "Lewis et al. treat retrieved documents $z$ as latent variables summed over the top-$k$ passages. `[pause 1s]`  
> The difference is the order of sum $\sum$ and product $\prod$:  
> - **RAG-Sequence** `[MOUSE: Eq 1]` puts $\sum$ outside $\prod$. The whole answer $y$ uses **one document $z$**, keeping the context consistent.  
> - **RAG-Token** `[MOUSE: Eq 2]` puts $\sum$ inside $\prod$. It can switch documents at every token $i$, which helps combine facts from multiple sources.  
> All probabilities stay in $[0, 1]$."

- **Chuyển slide:** `"Hãy xem một ví dụ tính số cụ thể."` $\to$ Bấm `Space`.

---

### Slide 07: Numerical Example ($k=2, T=2$) (`07_numerical_example.tex`)
- **Thời lượng:** `04:15 – 04:55` (40s)
- **Trên màn hình:** Bảng $z_1, z_2$, hai phép tính ra **0.5280** và **0.4692**.
- **Thao tác:** `[MOUSE]:` Chỉ vào $z_1$, rồi gạch dưới **0.5280** và **0.4692**.

#### Tiếng Việt:
> "Ví dụ với $k=2$ tài liệu có trọng số $0.70$ và $0.30$ để sinh 2 token $a, b$: `[MOUSE: Bảng]`  
> - **RAG-Sequence:** Tính xác suất từng tài liệu rồi cộng lại:  
>   $$0.70 \times (0.80 \times 0.90) + 0.30 \times (0.40 \times 0.20) = 0.5040 + 0.0240 = \mathbf{0.5280}$$  
> - **RAG-Token:** Cộng xác suất ở từng bước rồi nhân lại:  
>   $$(0.70 \times 0.80 + 0.30 \times 0.40) \times (0.70 \times 0.90 + 0.30 \times 0.20) = 0.6800 \times 0.6900 = \mathbf{0.4692}$$  
> Hai kết quả khác nhau ($0.5280$ vs $0.4692$) vì phép tổng và phép tích **không giao hoán**."

#### English:
> "Here is an example with $k=2$ passages (weights $0.70$ and $0.30$) generating two tokens $(a, b)$: `[MOUSE: Table]`  
> - **RAG-Sequence:**  
>   $$0.70 \times (0.80 \times 0.90) + 0.30 \times (0.40 \times 0.20) = 0.5040 + 0.0240 = \mathbf{0.5280}$$  
> - **RAG-Token:**  
>   $$(0.70 \times 0.80 + 0.30 \times 0.40) \times (0.70 \times 0.90 + 0.30 \times 0.20) = 0.6800 \times 0.6900 = \mathbf{0.4692}$$  
> The gap ($0.5280$ vs.\ $0.4692$) shows that $\sum$ and $\prod$ do not commute."

- **Online Handoff (`04:55 – 05:00`):**  
  `[ACTION]:` Nhìn webcam, nói rõ:  
  - **Tiếng Việt:** *"Để kiểm chứng trên dữ liệu thực tế, em xin nhường lời cho bạn Lê Huy trình bày phần thực nghiệm quy chế HCMUS ạ. Mời Huy bật mic."*  
  - **English:** *"To test this on real documents, I will hand over to Le Huy for our HCMUS experiments. Huy, please unmute."*  
  `[ACTION]:` Tắt mic (Mute).

---

## Q&A Trực tuyến (Speaker 1: Nam Kiệt)

1. **Q02: Parametric vs Non-parametric? RAG khác Fine-tuning và Long-context thế nào?**  
   - Parametric là trọng số tĩnh (tốn kém khi train lại). Non-parametric là kho tài liệu ngoài (cập nhật nhanh). Qwen được giữ nguyên trọng số, không fine-tune trên quy chế.
2. **Q03: Khác biệt RAG-Sequence và RAG-Token?**  
   - Sequence lấy tổng ngoài tích (nhất quán 1 nguồn); Token lấy tích ngoài tổng (trộn nhiều nguồn). Ví dụ Slide 07 ra $0.5280$ vs $0.4692$.
3. **Q04: Có train lại end-to-end như Lewis không?**  
   - Không. Nhóm dùng cách hiện đại: lấy top-5 chunk đưa vào prompt cho Qwen2.5-1.5B-Instruct.
4. **Q07: Khác biệt TF-IDF, BM25 và BGE-M3?**  
   - TF-IDF đếm từ khóa thưa. BM25 thêm giới hạn lặp từ và phạt độ dài ($k_1=1.5, b=0.75$). BGE-M3 dùng mạng neural tạo vector ngữ nghĩa 1024 chiều.
