# Kịch bản Thuyết trình Trực tuyến (Online Presentation Script) — Speaker 1

> **Hình thức:** Thuyết trình Trực tuyến (Google Meet / Zoom / MS Teams)  
> **Diễn giả:** Trịnh Võ Nam Kiệt (`24125013`)  
> **Nhiệm vụ:** Trình bày Phần 1 — *Lý thuyết Nền tảng, Kiến trúc Pipeline & Mô hình Xác suất*  
> **Thời lượng quy định:** Đúng **05:00 phút** (từ `00:00` đến `05:00`)  
> **Phạm vi Slides:** Slide 01 đến Slide 07 (7 slides)  
> **Thiết lập Kỹ thuật:** Bật Webcam góc quay ngang mắt, Mic kiểm tra không vọng/ồn, chia sẻ màn hình toàn màn hình (`Ctrl + L` chế độ Presentation trên Adobe Acrobat / Foxit / Trình duyệt), dùng **chuột (Mouse Cursor)** làm con trỏ chỉ dẫn trực tiếp.

---

## Bảng Phân bổ Thời gian & Pacing Checkpoints (Speaker 1)

| Slide | Tiêu đề Slide | Mốc thời gian | Thời lượng | Thao tác Trực tuyến (Online Actions) |
| :---: | :--- | :---: | :---: | :--- |
| **01** | Title Page | `00:00 – 00:35` | 35s | Chia sẻ màn hình, kiểm tra nhanh mic/hình ảnh, mở đầu tự tin. |
| **02** | Outline Roadmap | `00:35 – 01:00` | 25s | Bấm `Space` chuyển Slide 02, quét chuột qua 3 phần trình bày. |
| **03** | Introduction & Guiding Question | `01:00 – 01:50` | 50s | Bấm `Space` sang Slide 03, rê chuột nhấn mạnh Guiding Question. |
| **04** | Knowledge Grounding Paradigms | `01:50 – 02:40` | 50s | Bấm `Space` sang Slide 04, lướt chuột qua bảng 3 phương pháp. |
| **05** | RAG Architecture & Failures | `02:40 – 03:30` | 50s | Bấm `Space` sang Slide 05, rê chuột theo 6 bước sơ đồ luồng. |
| **06** | Probabilistic Modeling | `03:30 – 04:15` | 45s | Bấm `Space` sang Slide 06, chỉ chuột vào dấu $\sum$ và $\prod$. |
| **07** | Worked Numerical Example | `04:15 – 04:55` | 40s | Bấm `Space` sang Slide 07, rê chuột qua 2 số **0.5280** và **0.4692**. |
| **--** | **Online Handoff** | `04:55 – 05:00` | 05s | Nhường lời và nhắc bạn Lê Huy bật mic tiếp quản. |

> [!TIP]
> **Pacing Checkpoint Online (Mốc 04:15):** Khi đồng hồ bấm giờ góc màn hình chạm `04:15`, bạn **bắt buộc phải đang ở Slide 07**. Không phân tích lan man ở Slide 06; chốt ngay kết quả tính toán $0.5280$ vs $0.4692$ để nhường lời cho Huy đúng `04:55 – 05:00`.

---

## Chi tiết Kịch bản Từng Slide (Slide-by-Slide Delivery)

### Slide 01: Title Page (`01_title.tex`)
- **Thời lượng:** `00:00 – 00:35` (35 giây)
- **Hiển thị trên màn hình:** Slide bìa Beamer xanh chuẩn mực, tiêu đề đề tài S07, tên và MSSV 3 thành viên, thông tin FIT HCMUS.
- **Thao tác Trực tuyến:**
  - `[ACTION]:` Nhìn thẳng vào webcam (không nhìn lệch xuống phím), bật Unmute mic, nét mặt nghiêm túc, phong thái đĩnh đạc.
  - `[SCREEN]:` Đảm bảo slide đang ở chế độ Full Screen (`Ctrl + L`), không để lộ thanh taskbar hay cửa sổ chat.

#### Kịch bản Thuyết trình (Tiếng Việt):
> *(Kiểm tra nhanh 3 giây đầu nếu vừa vào phòng):*  
> "Dạ em kính chào Thầy và các bạn. Dạ Thầy và các bạn có nghe rõ âm thanh và thấy slide em đang chia sẻ không ạ? `[pause 1s]` Dạ em xin cảm ơn.  
> Hôm nay, nhóm em xin phép được trình bày đề tài seminar môn Nhập môn Trí tuệ Nhân tạo với chủ đề: **S07: Retrieval-Augmented Generation (RAG) — Grounding LLM Responses in Documents**.  
> Đề tài được thực hiện bởi nhóm 3 thành viên: em là **Trịnh Võ Nam Kiệt**, cùng hai bạn **Trần Đăng Lê Huy** và **Bùi Trọng Tuấn Lĩnh**.  
> Mục tiêu cốt lõi của nghiên cứu là kết hợp giữa **mô hình hóa xác suất nền tảng** của Lewis et al. tại NeurIPS 2020 với việc **đo lường thực nghiệm độc lập** trên 4 văn bản quy chế đào tạo chính thức của Trường Đại học Khoa học Tự nhiên."

#### English Presentation Script:
> *(Quick audio/visual check):*  
> "Good morning, Professor and fellow classmates. Could everyone hear me clearly and see my shared screen? `[pause 1s]` Great, thank you.  
> Today, our team is pleased to present our seminar topic **S07: Retrieval-Augmented Generation (RAG) — Grounding LLM Responses in Documents**.  
> Our team consists of three members: myself, **Nam Kiet**, together with **Le Huy** and **Tuan Linh**.  
> The core objective of our work is to bridge the **probabilistic theoretical foundations** established by Lewis et al. at NeurIPS 2020 with an **independent empirical investigation** across four official academic regulations at VNU-HCM University of Science."

- **Transition Cue:** `"Sau đây, em xin điểm qua lộ trình của bài thuyết trình hôm nay."`  
  `[ACTION]:` Nhấn phím `Space` hoặc `Mũi tên phải` để sang Slide 02.

---

### Slide 02: Outline Roadmap (`02_outline.tex`)
- **Thời lượng:** `00:35 – 01:00` (25 giây)
- **Hiển thị trên màn hình:** Lộ trình 3 phần nội dung đánh số 1, 2, 3 kèm tên người trình bày và mốc thời gian 5 phút.
- **Thao tác Trực tuyến:**
  - `[MOUSE CURSOR]:` Rê nhẹ con trỏ chuột theo thứ tự 3 mục lớn 1 $\to$ 2 $\to$ 3.

#### Kịch bản Thuyết trình (Tiếng Việt):
> "Bài thuyết trình 15 phút của nhóm em được phân bổ cân bằng cho cả 3 thành viên — mỗi người đảm nhiệm đúng 5 phút:  
> - **Phần 1 (00:00 – 05:00):** Em sẽ trình bày lý thuyết nền tảng, kiến trúc pipeline và mô hình xác suất Sequence và Token.  
> - **Phần 2 (05:00 – 10:00):** Bạn Lê Huy sẽ công bố kết quả thực nghiệm trên 51 trang quy chế HCMUS, đối sánh 3 mô hình retrieval và phân tích worked example.  
> - **Phần 3 (10:00 – 15:00):** Bạn Tuấn Lĩnh sẽ mổ xẻ chất lượng sinh ngữ 4 nhánh, phân tích 5 ca lỗi thực tế và đề xuất cơ chế hậu kiểm GenXAI."

#### English Presentation Script:
> "Our 15-minute presentation is equally divided among the three members — exactly five minutes each:  
> - **Part 1 (00:00 – 05:00):** I will cover the theoretical foundations, the end-to-end RAG pipeline, and the mathematical formulations of RAG-Sequence versus RAG-Token.  
> - **Part 2 (05:00 – 10:00):** Le Huy will present our empirical benchmark across 51 pages of HCMUS regulatory documents, comparing three retrieval configurations and a worked example.  
> - **Part 3 (10:00 – 15:00):** Tuan Linh will analyze four-way generation quality, dissect five representative failure archetypes, and propose a GenXAI verification loop."

- **Transition Cue:** `"Ngay sau đây, chúng ta cùng đi vào câu hỏi nghiên cứu định hướng của đề tài."`  
  `[ACTION]:` Nhấn `Space` sang Slide 03.

---

### Slide 03: Introduction & Guiding Question (`03_intro_question.tex`)
- **Thời lượng:** `01:00 – 01:50` (50 giây)
- **Hiển thị trên màn hình:** Câu hỏi in đậm: *Does providing external documents eliminate hallucinations?* và 4 gạch đầu dòng.
- **Thao tác Trực tuyến:**
  - `[MOUSE CURSOR]:` Khoanh tròn chuột quanh dòng câu hỏi định hướng.
  - `[TONE]:` Hạ giọng trầm, nhấn mạnh tính nghịch lý giữa trí nhớ tham số và tài liệu bên ngoài.

#### Kịch bản Thuyết trình (Tiếng Việt):
> "Thưa Thầy, thách thức lớn nhất của các mô hình ngôn ngữ lớn hiện nay bắt nguồn từ **Parametric Memory** — toàn bộ tri thức được lưu tĩnh trong ma trận trọng số. `[pause 1s]`  
> Do đó, mô hình tất yếu gặp phải hiện tượng ảo giác (hallucination), tri thức bị đóng băng theo thời gian (cut-off staleness), và hoàn toàn không thể kiểm chứng nguồn gốc.  
> RAG ra đời để giải quyết vấn đề này bằng cách bổ sung **Non-parametric Memory** — một kho tài liệu bên ngoài có thể cập nhật nóng mà không cần đào tạo lại.  
> Tuy nhiên, câu hỏi nghiên cứu cốt lõi mà nhóm em đặt ra là: `[nhấn mạnh]` **Liệu việc cung cấp tài liệu bên ngoài có thực sự triệt tiêu được ảo giác trong LLM hay không?** `[pause 1s]` Hay nó chỉ dịch chuyển sai số sang các mắt xích khác trong quy trình?  
> Nhóm em sẽ trả lời trực diện câu hỏi này thông qua các bằng chứng định lượng cụ thể."

#### English Presentation Script:
> "The fundamental bottleneck of modern LLMs originates from **parametric memory** — knowledge is stored implicitly and statically within neural weights. `[pause 1s]`  
> Consequently, models inevitably suffer from factual hallucinations, temporal cutoff staleness, and a lack of auditability.  
> RAG addresses this by augmenting the generator with **non-parametric memory** — an external, hot-swappable document index that can be inspected and updated without retraining.  
> However, our guiding research question asks: `[emphasize]` **Does providing external documents actually eliminate hallucinations in language models?** `[pause 1s]` Or does it merely shift the origin of errors downstream into the pipeline?  
> Our presentation will directly answer this question with empirical evidence."

- **Transition Cue:** `"Để trả lời câu hỏi này, trước hết ta cùng so sánh RAG với các phương pháp neo kiến thức hiện có."`  
  `[ACTION]:` Nhấn `Space` sang Slide 04.

---

### Slide 04: Knowledge Grounding Paradigms (`04_paradigms.tex`)
- **Thời lượng:** `01:50 – 02:40` (50 giây)
- **Hiển thị trên màn hình:** Bảng 3 hàng đối chiếu Fine-Tuning, Long-Context, RAG và 3 bullets đúc kết.
- **Thao tác Trực tuyến:**
  - `[MOUSE CURSOR]:` Lần lượt di chuột qua từng hàng: Fine-Tuning $\to$ Long-Context $\to$ RAG.

#### Kịch bản Thuyết trình (Tiếng Việt):
> "Bảng trên slide tóm tắt 3 trường phái chính để neo tri thức vào LLM:  
> - **Fine-Tuning:** `[MOUSE: Hàng 1]` Can thiệp trực tiếp vào trọng số tham số; chi phí GPU rất đắt đỏ, nguy cơ quên thảm họa (catastrophic forgetting), và khi quy chế thay đổi bắt buộc phải đào tạo lại.  
> - **Long-Context:** `[MOUSE: Hàng 2]` Đưa toàn bộ tài liệu vào prompt; chi phí token tăng theo cấp số nhân và mô hình rất dễ bỏ sót dữ kiện do hiện tượng *Lost-in-the-Middle*.  
> - **RAG (Hybrid Memory):** `[MOUSE: Hàng 3]` Phân tách rõ ràng hai vai trò: mô hình tham số đóng vai trò bộ máy tổng hợp ngôn ngữ, còn chỉ mục tài liệu đóng vai trò kho lưu trữ sự thật có thể kiểm toán.  
> Minh chứng là trong bài báo gốc của Lewis et al., RAG-Sequence đạt **44.5 điểm Exact Match** trên Natural Questions, vượt trội hoàn toàn so với mô hình thuần tham số T5-11B lớn hơn nó gấp 50 lần."

#### English Presentation Script:
> "This table contrasts the three primary knowledge grounding paradigms:  
> - **Fine-Tuning** `[MOUSE: Row 1]` modifies neural parameters directly; it incurs heavy GPU training costs, risks catastrophic forgetting, and requires full retraining whenever regulations change.  
> - **Long-Context Prompting** `[MOUSE: Row 2]` concatenates entire corpora into the context window; token costs scale quadratically, and attention dilutes due to the *Lost-in-the-Middle* phenomenon.  
> - **RAG represents a hybrid paradigm:** `[MOUSE: Row 3]` It decouples linguistic synthesis from factual storage, keeping contexts compact and the knowledge base modular.  
> In fact, Lewis et al. demonstrated that RAG-Sequence reached **44.5 Exact Match** on Natural Questions, significantly outperforming a purely parametric T5-11B model that was 50 times larger."

- **Transition Cue:** `"Để hiện thực hóa kiến trúc này, toàn bộ hệ thống phải vận hành qua một pipeline 6 bước."`  
  `[ACTION]:` Nhấn `Space` sang Slide 05.

---

### Slide 05: RAG Pipeline & Theoretical Failure Points (`05_pipeline.tex`)
- **Thời lượng:** `02:40 – 03:30` (50 giây)
- **Hiển thị trên màn hình:** Sơ đồ TikZ luồng 6 bước: Ingestion $\to$ Chunking $\to$ Indexing $\to$ Retrieval $\to$ Augmentation $\to$ Generation, và 3 nhóm failure points.
- **Thao tác Trực tuyến:**
  - `[MOUSE CURSOR]:` Rê chuột theo mũi tên từ hộp 1 đến hộp 6 trên sơ đồ.

#### Kịch bản Thuyết trình (Tiếng Việt):
> "Kiến trúc RAG chuẩn tắc vận hành qua 6 công đoạn tuần tự. `[MOUSE: Sơ đồ TikZ]` Điều quan trọng là: **sai số có thể phát sinh và lan truyền ở bất kỳ mắt xích nào**:  
> 1. **Khâu Tiền truy xuất (Pre-Retrieval):** Lỗi OCR khi quét PDF làm méo mó các bảng biểu học phí; hoặc thuật toán cắt chunk tùy tiện làm tách rời điều kiện ngoại lệ khỏi điều khoản gốc.  
> 2. **Khâu Truy xuất (Retrieval):** Hiện tượng bỏ sót bằng chứng vàng khiến ngưỡng điểm nằm ngoài Top-$k$; hoặc bị đánh lừa bởi các đoạn văn trùng từ khóa bề mặt nhưng sai bản chất (lexical distractors).  
> 3. **Khâu Hậu truy xuất (Post-Retrieval):** Ngay cả khi bằng chứng đã nằm trong prompt, LLM vẫn có thể đọc lệch cột bảng biểu, bỏ qua điều kiện phụ hoặc trích dẫn sai số hiệu quyết định.  
> Đây chính là nguồn gốc sản sinh ra các dạng ảo giác mới trong RAG."

#### English Presentation Script:
> "A standard RAG pipeline operates through six sequential stages. `[MOUSE: TikZ Flow]` Critically, **errors can originate and cascade at any single stage**:  
> 1. **Pre-Retrieval Failures:** OCR artifacts corrupt numerical tables; improper chunk boundaries sever administrative exemptions from their parent clauses.  
> 2. **Retrieval Failures:** False negative omissions occur when critical threshold clauses fall outside top-$k$; or lexical distractors mislead semantic search.  
> 3. **Post-Retrieval Failures:** Even with gold passages in the prompt, the generator may misalign table columns, prune secondary conditions, or fabricate citation identifiers.  
> These vulnerability points explain how new failure modes emerge within RAG systems."

- **Transition Cue:** `"Để hiểu cách mô hình kết hợp các tài liệu này bằng xác suất, chúng ta cùng xem xét hai phương trình toán học cốt lõi của Lewis et al."`  
  `[ACTION]:` Nhấn `Space` sang Slide 06.

---

### Slide 06: Probabilistic Modeling: Sequence vs. Token (`06_formulation.tex`)
- **Thời lượng:** `03:30 – 04:15` (45 giây)
- **Hiển thị trên màn hình:** 2 công thức lớn RAG-Sequence và RAG-Token, giải thích ký hiệu $z$, $x$, $y$, $\eta$, $\theta$.
- **Thao tác Trực tuyến:**
  - `[MOUSE CURSOR]:` Chỉ chuột vào dấu $\sum$ nằm ngoài tích $\prod$ ở công thức Sequence, sau đó chỉ vào dấu $\sum$ nằm trong ngoặc vuông ở công thức Token.

#### Kịch bản Thuyết trình (Tiếng Việt):
> "Lewis và cộng sự mô hình hóa tài liệu truy xuất $z$ như một **biến ẩn (latent variable)** được lấy cận biên trên Top-$k$ đoạn văn có điểm số cao nhất. `[pause 1s]`  
> Điểm khác biệt mấu chốt nằm ở vị trí tương đối giữa toán tử lấy tổng $\sum$ và toán tử lấy tích $\prod$:  
> - **RAG-Sequence:** `[MOUSE: Công thức 1]` Đặt tổng $\sum$ ở ngoài cùng. Mô hình giả định toàn bộ câu trả lời $y$ được điều kiện hóa xuyên suốt trên **cùng một tài liệu $z$**. Điều này đảm bảo tính nhất quán về văn phong và ngữ cảnh pháp lý.  
> - **RAG-Token:** `[MOUSE: Công thức 2]` Đưa tổng $\sum$ vào bên trong từng bước sinh token $i$. Mô hình cho phép chuyển đổi tài liệu tham chiếu linh hoạt ở từng từ sinh ra, phù hợp cho bài toán tổng hợp dữ kiện từ nhiều nguồn khác nhau.  
> Toàn bộ xác suất đều nằm trong khoảng $[0, 1]$ và phản ánh quá trình giải mã tự hồi quy."

#### English Presentation Script:
> "Lewis et al. formalized retrieved documents $z$ as **latent variables** marginalized across the top-$k$ candidate passages. `[pause 1s]`  
> The mathematical distinction lies in the relative position of the summation $\sum$ and product $\prod$ operators:  
> - **RAG-Sequence** `[MOUSE: Equation 1]` places the summation outside the token product. The entire candidate sequence $y$ is conditioned on a **single passage $z$**, preserving thematic consistency.  
> - **RAG-Token** `[MOUSE: Equation 2]` places the summation inside the token factor. The model dynamically shifts document weighting at every single decoding step $i$, enabling multi-document factual synthesis.  
> All probabilities are dimensionless and bounded in $[0, 1]$ under causal autoregressive decoding."

- **Transition Cue:** `"Sau đây là ví dụ tính toán số cụ thể để thấy rõ sự khác biệt giữa hai mô hình."`  
  `[ACTION]:` Nhấn `Space` sang Slide 07.

---

### Slide 07: Worked Numerical Example ($k=2, T=2$) (`07_numerical_example.tex`)
- **Thời lượng:** `04:15 – 04:55` (40 giây)
- **Hiển thị trên màn hình:** Bảng 4 cột trải dài cân đối hết chiều rộng màn hình ($z_1, z_2$), 2 dòng tính $0.5280$ vs $0.4692$, kết luận về tính không giao hoán.
- **Thao tác Trực tuyến:**
  - `[MOUSE CURSOR]:` Chỉ vào hàng $z_1$, sau đó rê chuột gạch dưới hai con số in đậm **0.5280** và **0.4692**.

#### Kịch bản Thuyết trình (Tiếng Việt):
> "Nhóm xây dựng một ví dụ số chuẩn hóa với $k=2$ tài liệu có trọng số retriever lần lượt là $0.70$ và $0.30$ để sinh ra chuỗi gồm 2 token $a$ và $b$: `[MOUSE: Bảng]`  
> - Với **RAG-Sequence**, ta lấy tích xác suất token của từng tài liệu rồi nhân với trọng số retriever:  
>   $$0.70 \times (0.80 \times 0.90) + 0.30 \times (0.40 \times 0.20) = 0.5040 + 0.0240 = \mathbf{0.5280}$$  
> - Với **RAG-Token**, ta tính xác suất hỗn hợp tại từng vị trí token rồi nhân lại:  
>   $$(0.70 \times 0.80 + 0.30 \times 0.40) \times (0.70 \times 0.90 + 0.30 \times 0.20) = 0.6800 \times 0.6900 = \mathbf{0.4692}$$  
> Con số $0.5280$ khác $0.4692$ phản ánh tính **không giao hoán** giữa phép tổng và phép tích."

#### English Presentation Script:
> "We provide a standardized numerical example with $k=2$ passages having retriever weights of $0.70$ and $0.30$ generating a two-token sequence $(a, b)$: `[MOUSE: Table]`  
> - Under **RAG-Sequence**, sequence likelihoods are computed per passage and weighted:  
>   $$0.70 \times (0.80 \times 0.90) + 0.30 \times (0.40 \times 0.20) = 0.5040 + 0.0240 = \mathbf{0.5280}$$  
> - Under **RAG-Token**, intermediate mixture probabilities are calculated per step and multiplied:  
>   $$(0.70 \times 0.80 + 0.30 \times 0.40) \times (0.70 \times 0.90 + 0.30 \times 0.20) = 0.6800 \times 0.6900 = \mathbf{0.4692}$$  
> This numerical gap ($0.5280$ vs.\ $0.4692$) demonstrates the **non-commutativity** of $\sum$ and $\prod$."

- **Online Handoff Cue (Chuyển giao Trực tuyến 1: 04:55 – 05:00):**  
  > `[ACTION]:` Nhìn thẳng vào webcam, nở nụ cười, nói to rõ:  
  > **Tiếng Việt:** *"Để kiểm chứng mô hình toán học này trên dữ liệu văn bản thực tế, sau đây em xin nhường lời cho bạn Lê Huy. Mời bạn Huy bật mic trình bày phần thực nghiệm quy chế đào tạo HCMUS ạ."*  
  > **English:** *"To empirically evaluate these concepts on real-world institutional documents, I will now hand over to Le Huy. Huy, please unmute and present our HCMUS experimental evaluation."*  
  > `[ACTION]:` Tắt mic (Mute) để nhường kênh âm thanh cho Lê Huy. (Lưu ý: Nếu Kiệt là người chia sẻ màn hình thì Kiệt tiếp tục bấm phím chuyển slide theo khẩu lệnh của Huy; hoặc nếu Huy share màn hình thì Huy tiếp quản).

---

## Chuẩn bị Hỏi & Đáp Q&A Trực tuyến (Speaker 1: Nam Kiệt)

Khi bước vào phiên Q&A trực tuyến (15:00 – 20:00), Nam Kiệt bật mic trả lời chính 4 câu hỏi lý thuyết:
1. **Q02: Phân biệt Parametric vs Non-parametric memory? RAG khác Fine-tuning và Long-context thế nào?**
   - *Key Point:* Parametric là trọng số mạng (tĩnh, đắt đỏ). Non-parametric là index bên ngoài (cập nhật nóng). Qwen được giữ nguyên trọng số, không bị fine-tune lại bằng văn bản HCMUS.
2. **Q03: Bản chất phương trình RAG-Sequence và RAG-Token? Ví dụ số tính toán ra sao?**
   - *Key Point:* Sequence lấy tổng ngoài tích (nhất quán văn phong); Token lấy tích ngoài tổng (tổng hợp đa nguồn). Dẫn số $0.5280$ và $0.4692$ từ Slide 07.
3. **Q04: Nhóm có huấn luyện lại end-to-end mô hình Lewis không? Triển khai thực tế khác gì?**
   - *Key Point:* Không huấn luyện lại end-to-end. Nhóm triển khai theo trường phái hiện đại: retrieval-augmented prompting (lấy top-5 chèn vào context của Qwen2.5-1.5B-Instruct).
4. **Q07: Khác biệt kỹ thuật giữa TF-IDF, BM25 và BGE-M3?**
   - *Key Point:* TF-IDF dùng tần suất thưa. BM25 có bão hòa tần suất và phạt độ dài văn bản ($k_1=1.5, b=0.75$). BGE-M3 dùng mạng neural đa ngôn ngữ ánh xạ câu thành vector 1024 chiều.
