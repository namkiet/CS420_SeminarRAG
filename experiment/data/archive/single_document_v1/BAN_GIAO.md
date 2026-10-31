# Bàn giao G2 Task 1–2

## Những gì đã có

| Hạng mục | Kết quả |
|---|---|
| Chủ đề thử nghiệm | Hỏi đáp một phần Quy chế đào tạo đại học HCMUS năm 2026 bằng RAG |
| Nguồn | QĐ 3087/QĐ-KHTN ngày 29/09/2026, liên kết từ website HCMUS |
| Corpus | 6 trang nguồn: PDF 4–8 và 21; trang in 3–7 và 20 |
| Bộ câu hỏi | 20 câu, có đáp án tham chiếu, ý cần có và bằng chứng |
| Độ đa dạng | 5 câu tra cứu trực tiếp, 7 câu diễn đạt lại, 8 câu kết hợp nhiều đoạn |
| Kiểm chứng đã làm | Đọc ảnh 6 trang, chép sạch tiếng Việt, kiểm tra 29 đoạn evidence có trong đúng trang corpus |

Nguồn công bố: https://hcmus.edu.vn/quy-che-dao-tao-trinh-do-dai-hoc-nam-2026/

PDF gốc: https://drive.google.com/file/d/1F8OeurGoDyZCeMTql3enqYUpH72Z6Mpn/view?usp=drivesdk

## Vì sao chọn nguồn và phạm vi này?

Tài liệu có nguồn công bố chính thức, số quyết định, ngày ban hành và nội dung có thể đối chiếu. Các quy định có cả định nghĩa, số liệu, điều kiện và ngoại lệ, phù hợp để xây dựng câu hỏi dễ lẫn nếu truy xuất không đủ ngữ cảnh. Phạm vi 6 trang nguồn đáp ứng quy mô nhỏ của đề seminar, không cần thu thập toàn website.

Trang PDF 21 được thêm để giữ điều khoản chuyển tiếp. Các Điều 25–26 cùng trang được giữ làm ngữ cảnh và nội dung gây nhiễu tự nhiên. Bộ câu hỏi không đại diện toàn bộ quy chế hay mọi nhu cầu của sinh viên.

## Cách chuẩn bị dữ liệu

1. Theo liên kết từ trang công bố HCMUS tới PDF gốc; lưu nguyên file và ghi SHA-256 trong `sources.json`.
2. Chọn trang PDF 4–8 và 21; giữ trang in và điều/khoản làm metadata. PDF gốc 21 trang chỉ là bản lưu đối chiếu.
3. Lớp văn bản OCR có nhiều lỗi tiếng Việt. Bản sạch được chép/hiệu chỉnh từ ảnh trang, bỏ mộc/chữ ký/số trang rời và nối dòng; không tự thay đổi các ngưỡng hay quan hệ điều kiện.
4. Viết câu hỏi dựa trên nội dung đã chọn, tạo đáp án bằng lời của nhóm và các ý cần có để chấm linh hoạt.
5. Gắn từng câu với một hoặc nhiều đoạn trích cụ thể. Đáp án tính toán ở Q04 là phép tính do nhóm xây dựng, không phải một kết quả thực nghiệm được văn bản công bố.
6. Kiểm tra tự động mỗi đoạn evidence có trong đúng trang đã chỉ định. Kiểm tra này xác nhận sự nhất quán của dữ liệu, không chứng minh một mình rằng bản chép đúng; phần đối chiếu ảnh được thực hiện riêng.

## Cách dùng cho Task 3–4

- Chỉ index `processed/D01_corpus.txt` hoặc nội dung các trang trong `D01_pages.json`. Không index câu hỏi, đáp án chuẩn, tài liệu hướng dẫn hoặc toàn bộ PDF 21 trang.
- Nếu chunking theo trang, chú ý câu nối trang 5–6 ở Điều 5(1)(a) và trang 7–8 ở Điều 7(3). Bản TXT đã nối hai câu này.
- Truyền trường `question` cho retrieval. Giữ `reference_answer`, `expected_key_points` và `evidence` ở phía đánh giá.
- Với từng cấu hình chunking, đọc các chunks và ánh xạ các đoạn bằng chứng sang tập chunk liên quan. Không chỉ xem cả tài liệu D01 là một gold document: corpus chỉ có một tài liệu nên đo ở cấp tài liệu sẽ không phân biệt được vị trí bằng chứng.
- `relevant_chunk_ids` đang để rỗng có chủ đích vì Task 3 chưa tạo chunks. Không suy ra rằng câu hỏi không có đáp án.
- Khi một đoạn bằng chứng bị chia vào nhiều chunks, xác định trước quy tắc liên quan/đủ bằng chứng. Lưu nhãn riêng cho từng cấu hình; không tái sử dụng ID của cấu hình khác.
- Phân biệt: Hit@k kiểm tra có ít nhất một chunk liên quan trong top-k; Recall@k là tỷ lệ chunk liên quan được tìm thấy trên tổng tập chunk liên quan đã gán nhãn. Với câu cần nhiều bằng chứng, Hit@k không đủ để kết luận đã có toàn bộ thông tin trả lời.
- So sánh ít nhất hai chunk size hoặc hai giá trị k theo đề. Phần này do người làm Task 3–4 thực hiện; chưa có bảng kết quả retrieval trong bộ bàn giao này.

## Điểm cần giữ khi giải thích kết quả

- Bộ câu hỏi hỏi theo văn bản 2026. Q20 kiểm tra giới hạn áp dụng cho khóa cũ theo Điều 27; không dùng bộ dữ liệu để khẳng định mọi quy định áp dụng nguyên trạng cho sinh viên tuyển năm 2025 trở về trước.
- Điều 3(6) có cả nguyên tắc chung theo tỷ lệ và giới hạn rút ngắn theo từng hình thức. Q06 hỏi riêng điểm a; không suy ra thời gian tốt nghiệp sớm nhất chỉ từ 2/3 thời gian chuẩn.
- Q17 giữ nguyên câu ngoại trừ về tín chỉ tối thiểu, không tự thay “và” bằng “hoặc”.
- Q16 chỉ biết có dẫn chiếu hoãn thi tại Điều 14; Điều 14 nằm ngoài corpus nên không suy diễn điều kiện, hồ sơ hay hạn nộp hoãn thi.
- Bộ 20 câu đều có bằng chứng trong corpus, phù hợp đo retrieval trên câu có đáp án. Chưa đo khả năng từ chối câu hỏi ngoài phạm vi; nếu nhóm muốn kiểm tra thì tạo bộ phụ riêng và không đưa vào mẫu số Recall@k của tập có đáp án.
- Quy mô chỉ một nguồn, 6 trang và 20 câu do nhóm soạn. Không khái quát kết quả sang mọi miền dữ liệu hoặc khẳng định RAG loại bỏ hallucination.

## Nội dung tham khảo cho báo cáo

> Nhóm xây dựng một corpus nhỏ từ Quy chế đào tạo trình độ đại học năm 2026 của Trường Đại học Khoa học tự nhiên, ĐHQG-HCM, ban hành kèm Quyết định 3087/QĐ-KHTN ngày 29/09/2026. Corpus sử dụng sáu trang nguồn (trang PDF 4–8 và 21), tập trung vào học phần, tín chỉ, thời gian đào tạo, tổ chức đào tạo và đăng ký học tập, đồng thời giữ điều khoản chuyển tiếp. Văn bản được làm sạch dựa trên ảnh trang PDF do lớp OCR có nhiều lỗi nhận dạng tiếng Việt. Nhóm xây dựng 20 câu hỏi tham chiếu, gồm 5 câu tra cứu trực tiếp, 7 câu diễn đạt lại và 8 câu kết hợp nhiều đoạn bằng chứng. Mỗi câu hỏi có đáp án chuẩn, các ý cần có và vị trí bằng chứng theo tài liệu, trang và điều/khoản. Bộ dữ liệu được dùng làm đầu vào đánh giá retrieval; các kết quả retrieval và sinh câu trả lời sẽ được báo cáo riêng sau thực nghiệm.

Đoạn trên mô tả sản phẩm đã tạo với trợ lý AI. Trước khi dùng trong báo cáo, nhóm cần tự đọc và kiểm chứng, điều chỉnh cách diễn đạt cho đúng công việc thực tế của mình, đồng thời khai báo AI tools theo yêu cầu đề. Chưa có thành viên nào được ghi nhận là đã kiểm chứng độc lập; `human_review_status` hiện là `pending`.

## Công việc tiếp theo

1. Đọc `questions.md` cùng PDF gốc, ưu tiên các câu có ngoại lệ/phạm vi: Q06, Q09, Q15–Q17 và Q20.
2. Ghi nhận chỉnh sửa nếu có và đánh dấu `human_review_status` sau khi tự kiểm chứng.
3. Gửi corpus cùng bộ câu hỏi cho bạn làm Task 3–4; thống nhất cách gán gold chunks và tiêu chí đánh giá.
4. Chuẩn bị giải thích cách chọn nguồn, xây đáp án và giới hạn của bộ dữ liệu khi thuyết trình.
