# Bảng Tổng hợp Yêu cầu Dự án Nghiên cứu RAG

---

## Bảng 1: G1. Research & Theoretical Foundation

| Task | Subtasks | Requirement | Deliverable |
| :--- | :--- | :--- | :--- |
| **Task 1: Xác định problem statement và research question** | - Xác định vấn đề hallucination của LLM.<br>- Mục tiêu của RAG và phạm vi nghiên cứu. | Làm rõ câu hỏi nghiên cứu: *Does providing external documents eliminate hallucinations in language models?* | Problem statement, research question và research objectives. |
| **Task 2: Nghiên cứu nền tảng RAG** | - Tìm hiểu parametric memory, non-parametric memory.<br>- Phân biệt RAG với fine-tuning và việc đưa toàn bộ tài liệu vào prompt. | Giải thích được cơ chế và sự khác biệt giữa các phương pháp bằng lời của nhóm. | Phần Background và sơ đồ so sánh các phương pháp. |
| **Task 3: Đọc và tổng hợp research papers** | - Đọc paper bắt buộc của Lewis et al. (2020), tập trung vào RAG-Sequence và RAG-Token.<br>- Đọc paper khuyến nghị của Schneider (2024) về evidence attribution và verification. | - Trình bày mục tiêu, đóng góp, phương pháp và phát hiện của paper.<br>- Phân biệt kết quả từ nghiên cứu gốc với kết quả của nhóm. | Bảng tổng hợp paper và phần Literature Review. |
| **Task 4: Phân tích pipeline RAG** | Mô tả các bước: ingestion, chunking, indexing, retrieval, prompt augmentation và answer generation; xác định failure points ở từng bước. | Pipeline phải đầy đủ và có giải thích cách lỗi tại mỗi bước ảnh hưởng đến kết quả. | Sơ đồ RAG pipeline và phân tích failure points. |
| **Task 5: Giải thích phương trình RAG-Sequence** | - Định nghĩa các ký hiệu.<br>- Giải thích công thức và thực hiện ví dụ tính toán từng bước. | Nêu miền giá trị, đơn vị thích hợp, giả định mô hình và ít nhất một numerical example chính xác. | Phần giải thích phương trình, ví dụ số và diễn giải kết quả. |

---

## Bảng 2: G2. Implementation & Evaluation

| Task | Subtasks | Requirement | Deliverable |
| :--- | :--- | :--- | :--- |
| **Task 1: Xây dựng knowledge corpus** | Thu thập và chuẩn hóa tài liệu nguồn. | Corpus gồm khoảng 5–10 trang tài liệu công khai hoặc được cấp phép phù hợp; nguồn phải xác minh được. | Bộ tài liệu corpus và danh sách nguồn. |
| **Task 2: Xây dựng bộ câu hỏi tham chiếu** | Soạn câu hỏi, đáp án chuẩn và xác định nguồn hỗ trợ từng đáp án. | Có 15–20 câu hỏi với reference answers và verifiable sources. | Bộ câu hỏi đánh giá kèm đáp án và nguồn tham chiếu. |
| **Task 3: Xây dựng và cấu hình retrieval system** | Chia tài liệu thành chunks, xây dựng chỉ mục và triển khai TF-IDF/BM25 hoặc embedding-based cosine similarity. | Có ít nhất hai cấu hình chunk size hoặc hai giá trị $k$ để đánh giá so sánh. | Code retrieval, cấu hình thực nghiệm và tập chunks. |
| **Task 4: Đánh giá retrieval performance** | Chạy retrieval trên bộ câu hỏi, xác định tài liệu/chunk liên quan và tính các chỉ số đánh giá. | Sử dụng top-$k$ hit rate hoặc Recall@$k$; so sánh ít nhất hai cấu hình. | Bảng Recall@$k$ và phần nhận xét kết quả. |
| **Task 5: Thực hiện worked example** | Chọn một câu hỏi, trình bày các chunks được truy xuất, cách đưa evidence vào prompt và câu trả lời có citation. | Thể hiện rõ mối liên hệ giữa câu hỏi, evidence được truy xuất và câu trả lời. | Một ví dụ hoàn chỉnh từ câu hỏi đến câu trả lời có trích dẫn. |
| **Task 6: So sánh câu trả lời có và không có retrieval** | Chạy cùng bộ câu hỏi trong điều kiện có và không có retrieval. | Nếu có LLM, thực hiện so sánh câu trả lời giữa hai điều kiện. Nếu không có LLM, tập trung vào phân tích retrieval và minh họa cách chèn evidence vào prompt. | Bảng so sánh câu trả lời hoặc báo cáo phân tích retrieval thay thế. |
| **Task 7: Phân tích failure cases và đề xuất cải thiện** | Xác định lỗi do không truy xuất được evidence, truy xuất sai tài liệu, citation không liên quan hoặc câu trả lời vượt quá evidence. | Phân tích ít nhất 3 failure cases, đồng thời đề xuất cơ chế verification và cập nhật tài liệu. | Bảng phân tích lỗi, nguyên nhân, ảnh hưởng và hướng khắc phục. |

---

## Bảng 3: G3. Report, Slides & Seminar

| Task | Subtasks | Requirement | Deliverable |
| :--- | :--- | :--- | :--- |
| **Task 1: Tổng hợp kết quả và thảo luận** | Tổng hợp lý thuyết, kết quả thực nghiệm, điểm mạnh, điểm yếu và điều kiện áp dụng của RAG. | Phân biệt phát hiện từ paper với kết quả do nhóm tự thực hiện; không khái quát quá mức từ thí nghiệm nhỏ. | Phần Results and Discussion và Conclusion. |
| **Task 2: Viết báo cáo nghiên cứu** | Viết và tích hợp các phần Abstract, Introduction, Background/Paper Review, Method/Worked Example, Results and Discussion, Conclusion và References. | Báo cáo tiếng Việt, khổ A4, dài 6–10 trang, không tính references và appendices. | Báo cáo research-style hoàn chỉnh. |
| **Task 3: Kiểm tra nguồn và tính chính xác** | Kiểm tra citation, hình ảnh, bảng, phương trình, dataset và các AI tools đã sử dụng. | Trích dẫn đầy đủ và tự xác minh các nhận định do AI tạo ra. | Báo cáo đã kiểm tra nguồn và danh mục tài liệu tham khảo. |
| **Task 4: Chuẩn bị seminar slides** | Chuyển nội dung nghiên cứu thành slides, ưu tiên pipeline, phương trình, worked example, bảng Recall@$k$ và failure analysis. | Có 8–12 slides nội dung; hình và phương trình có nguồn; nội dung rõ ràng, tránh sao chép nguyên văn. | Bộ slides thuyết trình hoàn chỉnh. |
| **Task 5: Chuẩn bị kịch bản thuyết trình** | Phân chia nội dung, thời lượng và trách nhiệm trình bày giữa các thành viên. | Thuyết trình trong 15 phút; tất cả thành viên đều phải trình bày. | Presentation script hoặc speaker notes. |
| **Task 6: Chuẩn bị Q&A** | Dự kiến các câu hỏi về lý thuyết RAG, phương trình, lựa chọn retrieval method, kết quả thực nghiệm, hallucination và limitations. | Có khả năng giải thích và bảo vệ các quyết định kỹ thuật; mỗi thành viên phải trả lời ít nhất một câu hỏi. | Bộ câu hỏi dự kiến và câu trả lời tham khảo. |
| **Task 7: Review và nghiệm thu** | Đối chiếu báo cáo, slides và kết quả thực nghiệm với toàn bộ yêu cầu trong đề. | Có pipeline RAG, worked example, bảng Recall@$k$, ít nhất 3 failure cases, ví dụ số hoặc minh họa thuật toán và evidence-supported comparison. | Checklist nghiệm thu và bộ sản phẩm cuối cùng để nộp. |