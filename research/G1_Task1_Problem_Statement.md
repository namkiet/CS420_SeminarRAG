# G1 - Task 1: Xác định vấn đề và câu hỏi nghiên cứu

**Đề tài S07:** Retrieval-Augmented Generation (RAG): Grounding LLM Responses in Documents.

## 1. Đặt vấn đề (Problem statement)

Mô hình ngôn ngữ lớn (Large Language Model - LLM) có khả năng tạo câu trả lời bằng ngôn ngữ tự nhiên, nhưng việc sử dụng kiến thức lưu trong tham số còn gặp hạn chế về truy cập thông tin, cập nhật kiến thức và giải thích nguồn gốc câu trả lời. Lewis và cộng sự (2020) đề xuất Retrieval-Augmented Generation (RAG), kết hợp mô hình sinh với bộ truy hồi và kho tài liệu bên ngoài để hỗ trợ các tác vụ cần nhiều kiến thức. [1](https://arxiv.org/abs/2005.11401)

Trong bài toán hỏi đáp dựa trên tài liệu, người dùng cần kiểm tra được thông tin nào hỗ trợ câu trả lời. Một câu trả lời có cách diễn đạt hợp lý vẫn cần được đối chiếu với bằng chứng. Nghiên cứu này tập trung vào các phát biểu không được nội dung cung cấp hỗ trợ hoặc mâu thuẫn với nội dung đó, thay vì đánh giá độ trôi chảy của câu trả lời.

Việc truy hồi tài liệu không tự bảo đảm rằng mô hình sẽ sử dụng bằng chứng chính xác. Niu và cộng sự (2024), trong nghiên cứu RAGTruth, ghi nhận rằng các mô hình sử dụng RAG vẫn có thể sinh phát biểu thiếu căn cứ hoặc trái với nội dung truy hồi. Kết quả này cho thấy cần đánh giá câu trả lời bên cạnh việc kiểm tra các tài liệu tìm được. [2](https://aclanthology.org/2024.acl-long.585/)

Vì vậy, vấn đề nghiên cứu của seminar là xác định cách tài liệu bên ngoài hỗ trợ việc trả lời và những điều kiện khiến câu trả lời vẫn thiếu căn cứ. Nhóm sẽ xem xét riêng hai khâu: hệ thống có tìm được bằng chứng cần thiết hay không, và mô hình có tạo câu trả lời được bằng chứng đó hỗ trợ hay không. Cách tiếp cận này giúp tránh đồng nhất truy hồi thành công với trả lời chính xác.

**Phát biểu vấn đề:** Trong phạm vi hỏi đáp trên một kho tài liệu nhỏ, cần đánh giá khả năng truy hồi bằng chứng của RAG và, khi có mô hình sinh, kiểm tra mức độ câu trả lời bám sát bằng chứng. Từ đó, nghiên cứu xác định các lỗi còn tồn tại và điều kiện áp dụng, thay vì giả định rằng cung cấp tài liệu ngoài sẽ loại bỏ hoàn toàn hallucination.

## 2. Câu hỏi nghiên cứu (Research question)

### 2.1. Câu hỏi chính

> Does providing external documents eliminate hallucinations in language models?
>
> Việc cung cấp tài liệu bên ngoài có loại bỏ được hiện tượng hallucination trong mô hình ngôn ngữ không?

Đây là câu hỏi định hướng trong đề S07. [3](<../docs/S07_Seminar_RAG.pdf>)

### 2.2. Các câu hỏi cụ thể

1. **Khả năng tìm bằng chứng:** Với cùng bộ câu hỏi, hệ thống truy hồi tìm được bằng chứng cần thiết ở mức nào? Kết quả thay đổi ra sao giữa ít nhất hai cấu hình kích thước chunk hoặc giá trị top-k?
2. **Khả năng sử dụng bằng chứng:** Khi có LLM, câu trả lời trong điều kiện có retrieval khác gì so với điều kiện không có retrieval về độ chính xác và mức độ được tài liệu hỗ trợ?
3. **Lỗi còn tồn tại:** Những trường hợp thất bại xuất phát từ thiếu bằng chứng, truy hồi sai, trích dẫn không liên quan hay phát biểu vượt quá bằng chứng? Nhóm có thể đề xuất cách kiểm chứng và cải thiện nào từ các trường hợp quan sát được?

## 3. Mục tiêu nghiên cứu (Research objectives)

### 3.1. Mục tiêu tổng quát

Làm rõ vai trò của truy hồi tài liệu trong việc hỗ trợ LLM trả lời có căn cứ, đồng thời đánh giá các giới hạn của cách tiếp cận RAG thông qua một hệ thống minh họa quy mô nhỏ và các ví dụ có thể kiểm chứng.

### 3.2. Mục tiêu cụ thể

| Mã | Mục tiêu | Bằng chứng dùng để đánh giá việc hoàn thành |
| :--- | :--- | :--- |
| O1 | Giải thích cách kết hợp bộ truy hồi và mô hình sinh, cùng vai trò của tài liệu bên ngoài đối với câu trả lời. | Nội dung lý thuyết có trích nguồn, sơ đồ pipeline và một ví dụ hỏi đáp xuyên suốt. |
| O2 | Đánh giá khả năng truy hồi bằng chứng trên cùng một bộ câu hỏi tham chiếu, với ít nhất hai cấu hình. | Bảng top-k hit rate hoặc Recall@k, kèm định nghĩa chỉ số và kết quả theo từng câu hỏi. |
| O3 | Khi có LLM, so sánh câu trả lời có và không có retrieval, kiểm tra nội dung và trích dẫn dựa trên đáp án tham chiếu cùng tài liệu nguồn. | Bảng so sánh trên cùng câu hỏi, nêu phát biểu được hỗ trợ, thiếu căn cứ hoặc mâu thuẫn. |
| O4 | Xác định nguyên nhân và ảnh hưởng của ít nhất ba trường hợp thất bại, từ đó đề xuất cách kiểm chứng và cải thiện. | Bảng phân tích lỗi gắn với câu hỏi, bằng chứng, kết quả thực tế và đề xuất xử lý. |

Nếu không có LLM, mục tiêu O3 được giới hạn ở minh họa cách chèn bằng chứng truy hồi vào prompt. Khi đó, nhóm chỉ đánh giá được retrieval và thiết kế prompt; không có cơ sở thực nghiệm để kết luận mức thay đổi hallucination của mô hình sinh. Hướng thay thế này được đề S07 cho phép. [3](<../docs/S07_Seminar_RAG.pdf>)

## 4. Phạm vi nghiên cứu

### 4.1. Đối tượng và quy mô

Nghiên cứu tập trung vào bài toán hỏi đáp dựa trên tài liệu dạng văn bản thuộc một chủ đề hẹp. Các yêu cầu quy mô dưới đây bám theo đề S07; miền nội dung, tài liệu cụ thể và công cụ triển khai sẽ được nhóm thống nhất trước khi chạy thí nghiệm. [3](<../docs/S07_Seminar_RAG.pdf>)

| Thành phần | Phạm vi |
| :--- | :--- |
| Kho tài liệu | Khoảng 5-10 trang tài liệu công khai hoặc có quyền sử dụng phù hợp; giữ thông tin nguồn và vị trí bằng chứng. |
| Bộ câu hỏi | 15-20 câu hỏi có đáp án tham chiếu và nguồn kiểm chứng; xác định trước khi chạy đánh giá chính thức. |
| Bộ truy hồi | Triển khai nhẹ bằng TF-IDF/BM25 hoặc cosine similarity giữa embeddings. |
| Cấu hình so sánh | Ít nhất hai kích thước chunk hoặc hai giá trị k; sử dụng cùng corpus và bộ câu hỏi để đối chiếu. |
| Mô hình sinh | Tích hợp nếu có tài nguyên; khi so sánh có/không retrieval, giữ cùng mô hình và các thiết lập sinh liên quan, đồng thời ghi lại prompt. |
| Kết quả phân tích | Khả năng truy hồi, mức độ câu trả lời được bằng chứng hỗ trợ khi có LLM, tính phù hợp của trích dẫn và các trường hợp thất bại. |

### 4.2. Tiêu chí xem xét câu trả lời

Trong nghiên cứu này, nhóm dự kiến đánh giá riêng ba phương diện:

- **Độ chính xác:** nội dung trả lời có phù hợp với đáp án tham chiếu đã kiểm tra từ tài liệu nguồn hay không.
- **Mức độ bám sát bằng chứng:** các phát biểu có được nội dung truy hồi hỗ trợ hay không; có thêm thông tin hoặc diễn giải mâu thuẫn với bằng chứng không.
- **Khả năng kiểm chứng trích dẫn:** nguồn được dẫn có tồn tại và thực sự hỗ trợ phát biểu tương ứng hay không.

Một phát biểu không xuất hiện trong bằng chứng truy hồi chưa đủ để kết luận rằng nó sai trong thực tế. Ngược lại, việc trả lời đúng theo một tài liệu cũng không chứng minh rằng tài liệu đó luôn đúng hoặc còn hiệu lực. Vì vậy, nhóm cần ghi nhận riêng tính chính xác theo nguồn tham chiếu và mức độ bám sát bằng chứng, không gộp mọi trường hợp thành một loại lỗi.

### 4.3. Giới hạn của kết luận

Đây là nghiên cứu minh họa trong phạm vi seminar. Nhóm không đặt mục tiêu huấn luyện LLM từ đầu, tái hiện toàn bộ mô hình và benchmark trong paper Lewis và cộng sự, hoặc xây dựng hệ thống hỏi đáp quy mô lớn. Phần lý thuyết dựa trên paper gốc; hệ thống nhỏ của nhóm phục vụ kiểm tra các câu hỏi nghiên cứu trong phạm vi dữ liệu được chọn.

Các chỉ số retrieval chỉ phản ánh khả năng tìm bằng chứng theo quy ước đánh giá đã công bố. Chúng không trực tiếp đo hallucination của câu trả lời. Nếu không chạy mô hình sinh, nhóm sẽ không báo cáo kết quả thực nghiệm về hallucination.

Với bộ câu hỏi nhỏ, việc không quan sát thấy lỗi không đủ để khẳng định RAG loại bỏ hoàn toàn hallucination. Các kết luận sẽ được giới hạn theo corpus, câu hỏi, cấu hình và mô hình đã sử dụng. Kết quả từ tài liệu nghiên cứu và kết quả do nhóm thực hiện phải được trình bày tách biệt.

## 5. Đóng góp dự kiến

Seminar hướng đến ba đóng góp trong phạm vi học phần: trình bày vấn đề trả lời có căn cứ bằng một câu hỏi nghiên cứu rõ ràng; cung cấp một minh họa RAG có dữ liệu và kết quả kiểm chứng được; và giải thích những điều kiện dẫn đến thất bại thông qua phân tích bằng chứng cụ thể. Các đóng góp này sẽ được đánh giá sau khi thực nghiệm, không được xem là kết quả đã đạt được tại thời điểm xác lập vấn đề nghiên cứu.

## Tài liệu tham khảo

1. Lewis, P., et al. (2020). *Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks*. Advances in Neural Information Processing Systems, 33, 9459-9474. [Bản công bố NeurIPS](https://papers.neurips.cc/paper/2020/hash/6b493230205f780e1bc26945df7481e5-Abstract.html); [bản arXiv](https://arxiv.org/abs/2005.11401). Sử dụng phần Abstract và Introduction để xác lập động cơ nghiên cứu và ý tưởng kết hợp truy hồi với sinh ngôn ngữ.
2. Niu, C., Wu, Y., Zhu, J., Xu, S., Shum, K., Zhong, R., Song, J., & Zhang, T. (2024). *RAGTruth: A Hallucination Corpus for Developing Trustworthy Retrieval-Augmented Language Models*. Proceedings of the 62nd Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers), 10862-10878. [DOI: 10.18653/v1/2024.acl-long.585](https://doi.org/10.18653/v1/2024.acl-long.585). Tài liệu bổ sung cho nhận định rằng câu trả lời sử dụng RAG vẫn có thể thiếu căn cứ hoặc mâu thuẫn với nội dung truy hồi; không thay thế paper bắt buộc.
3. CS420 - Introduction to Artificial Intelligence. *[S07] Retrieval-Augmented Generation (RAG): Grounding LLM Responses in Documents*. Tài liệu giao seminar, mục I, II và IV. [Đề S07](<../docs/S07_Seminar_RAG.pdf>).

**Đối chiếu phân công:** [TASK.md](../docs/TASK.md), G1 - Task 1: xác định problem statement, research question, research objectives và phạm vi nghiên cứu.
