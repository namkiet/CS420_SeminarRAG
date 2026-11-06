# Đánh giá output RAG ngày 07/11/2026

**Kết luận: retrieval đã có ích, nhưng generator hiện tại chưa đủ tin cậy để dùng như chatbot tư vấn quy chế.** Bộ output phù hợp để làm baseline và phân tích lỗi cho seminar. Có tài liệu truy hồi không loại bỏ việc model trả lời sai.

## Phạm vi và cách đánh giá

Đã đọc đủ **20 cặp đáp án baseline/RAG**, đối chiếu `reference_answer`, `expected_key_points`, các quote và prompt/context thực tế trong `answers_comparison.json`; đọc thêm câu demo trong `custom_answer.json`. Lần chạy được đánh giá là bản FP32 + SDPA ngày 05/11, không dùng output dấu `!` của lần thử trước.

Đây là đánh giá định tính của Codex theo dữ liệu đã lưu, **chưa phải nhóm chấm độc lập và đối chiếu lại toàn bộ PDF gốc**. OCR/reference vẫn đang chờ duyệt. Các tỷ lệ dưới đây mô tả đúng bộ 20 câu này, không phải ước lượng độ chính xác trên câu hỏi mới.

Phân loại nội dung, tách riêng trích dẫn:

- **Đúng chính:** trả đúng nội dung chính cần hỏi, không thêm kết luận sai đáng kể. Không đồng nghĩa có trích dẫn hợp lệ hoặc mọi ý đều được context hỗ trợ.
- **Một phần:** có ý đúng nhưng thiếu ý cần thiết, mở rộng phạm vi hoặc thêm phát biểu chưa đúng điều kiện.
- **Sai:** sai một kết luận trọng yếu, số liệu, đối tượng hoặc điều kiện của câu hỏi.
- **Không trả lời:** chỉ sinh placeholder, không có đáp án thực chất.
- **Từ chối:** nói không đủ thông tin; không tính là trả lời đúng, cũng không tự động coi là bịa đáp án. Một số baseline từ chối vẫn kèm tên trường không đúng nguồn.

## Kết quả nội dung

| Phân loại | Không RAG | Có RAG |
|---|---:|---:|
| Đúng nội dung chính | 0/20 | **9/20 (45%)** |
| Đúng một phần/có lỗi phạm vi | 2/20 | 3/20 |
| Sai nội dung trọng yếu | 13/20 | 7/20 |
| Không có đáp án thực chất | 0/20 | 1/20 |
| Từ chối trả lời | 5/20 | 0/20 |

RAG cải thiện rõ các câu tra cứu trực tiếp như Q02, Q06, Q10, Q18, Q20. Tuy nhiên, **8/20 câu RAG sai hoặc không có đáp án**, và ba câu còn lại chỉ đúng một phần. Không được diễn giải Hit@5 = 95% thành độ chính xác trả lời 95%.

Các câu đúng chính: **Q01, Q02, Q06, Q09, Q10, Q15, Q17, Q18, Q20**. Q15 và Q17 còn thiếu một phần bằng chứng tham chiếu trong context, nên nội dung trùng reference chưa chứng minh grounding đầy đủ.

## Đối chiếu từng câu

| Câu | Baseline | RAG | Nhận xét về đáp án RAG |
|---|---|---|---|
| Q01 | Sai | Đúng chính | Phân biệt được tiên quyết phải học và thi đạt, học trước phải hoàn thành quá trình học. |
| Q02 | Sai | Đúng chính | Đúng 45–50 giờ, 60 phút/giờ và tổng khối lượng học tập. |
| Q03 | Sai | Sai | Mở đầu bằng **8–20 tín chỉ** thay vì **12–25** cho đại trà/tài năng; trộn hệ đào tạo và tự mâu thuẫn. Bị cắt ở 384 output token. |
| Q04 | Một phần | Sai | Nói quy định mới chỉ áp dụng khóa 2025 trở về trước, đảo ngược phạm vi của Điều 27. |
| Q05 | Sai | Không trả lời | Chỉ xuất **`[TBC_ID]`**, dù top-1 đã có đủ các điều kiện tốt nghiệp. |
| Q06 | Sai | Đúng chính | Quy tổng 112 điểm về 100 điểm. |
| Q07 | Một phần | Sai | Trả **Trung bình, 50 điểm** thay vì **Khá**; dùng nhầm quy định cho sinh viên nghỉ học/không đăng ký học phần. |
| Q08 | Sai | Một phần | Ý Trung bình 50 điểm đúng. Phần bổ sung về tính thời gian nghỉ học thiếu điều kiện và ngoại lệ. |
| Q09 | Sai | Đúng chính | Công thức và phép tính `(70 + 80 + 90) / 3 = 80` đúng. |
| Q10 | Sai | Đúng chính | Đúng thời hạn 15 ngày kể từ công bố dự kiến. |
| Q11 | Sai | Một phần | Đúng 15 tiết/tín chỉ học phí và tổng số tiết; thiếu thành phần mức thu theo năm học. Có nhãn nguồn giả. |
| Q12 | Từ chối | Sai | Chọn **C4 = 734.000** thay vì **C5 = 1.014.000 đồng** cho khối giáo dục chuyên nghiệp ngành AI. |
| Q13 | Từ chối | Sai | Có hai giá đúng nhưng gọi sai cột C1 và tính **1.014.000 − 974.000 = 230.000**; đúng là **40.000 đồng**. |
| Q14 | Từ chối | Một phần | Kết luận không dùng cho khóa 2020 đúng; phạm vi phải là **2022–2026**, không phải mọi khóa từ 2022 trở lên. |
| Q15 | Từ chối | Đúng chính | Đúng “có cơ sở được xét miễn” và 488.000 đồng/tín chỉ học phí. Context còn thiếu đoạn xác nhận IELTS 4.5. |
| Q16 | Từ chối | Sai | Nói đại trà và tài năng khóa 2024 cùng IELTS 4.5; tài năng phải **5.0/bậc 4**, đại trà **4.5/bậc 3** theo reference. |
| Q17 | Sai | Đúng chính | Đúng “không tự động” và yêu cầu nộp chứng chỉ trước hồ sơ tốt nghiệp; chưa giải thích đủ chuẩn trong quá trình học. |
| Q18 | Sai | Đúng chính | Đúng cuối học kỳ 6 và không tiếp tục đăng ký/học chuyên ngành khi chưa đạt. |
| Q19 | Sai | Sai | Chọn khoản dành cho chứng chỉ **có ghi hiệu lực**, trong khi hỏi chứng chỉ **không ghi hiệu lực**; bỏ mốc 2 năm. |
| Q20 | Sai | Đúng chính | Đủ đơn đăng ký, bản sao đúng hình thức và CCCD đối chiếu. |

## Các lỗi chính cần dùng trong seminar

### 1. Đã truy hồi đủ nhưng generator vẫn trả lời sai

- **Q03:** `D01_regulation_article_7_02` ở top-1 có sẵn cả mức 12–25 và các ngoại lệ. Model lấy số của chương trình khác rồi tiếp tục chép đoạn nguồn mâu thuẫn với kết luận đầu.
- **Q04:** `D01_regulation_article_27_01` ở top-1 ghi rõ khóa từ năm học 2026–2027 và cách xử lý khóa cũ. Model vẫn đảo ngược nhóm áp dụng.
- **Q05:** `D01_regulation_article_19_01` ở top-1 có đủ điều kiện tốt nghiệp, nhưng model chỉ trả placeholder.
- **Q19:** `D04_regulation_article_11_01` ở top-1 có cả hai trường hợp có/không ghi hiệu lực; model chọn sai khoản.

Đây là bằng chứng trực tiếp cho lỗi đọc hiểu/chọn điều kiện của generator. Tăng số đoạn truy hồi không tự giải quyết được những ca này.

### 2. Đọc bảng và tính toán chưa ổn

**Q12:** `D03_appendix_section_1_10` chứa cả dòng ngành AI và phần chú giải lặp: C4 là khối đại cương, C5 là khối chuyên nghiệp. Chú giải nằm trong `text`, thực tế đã được đưa vào prompt. Model vẫn trả 734.000 thay vì 1.014.000 đồng.

**Q13:** cùng chunk chứa cả AI và nhóm CNTT, có giá C5 lần lượt 1.014.000 và 974.000 đồng. Model đọc được hai giá nhưng đổi nhãn thành C1 và tính hiệu sai. Không nên gán lỗi này đơn thuần cho retrieval.

### 3. Một số câu thực sự thiếu bằng chứng truy hồi

- **Q07:** không lấy được đoạn ngưỡng 65–79 = Khá. Model dùng quy định khác về kết quả 50 điểm, thay vì nêu chưa đủ thông tin.
- **Q16:** có điều phân biệt tài năng khóa 2023 trở đi và bậc 4/6, nhưng thiếu chunk danh sách IELTS 5.0. Model còn bỏ qua khác biệt bậc 4 đã có.
- **Q15:** thiếu đoạn IELTS 4.5 dù câu trả lời trùng reference.
- **Q17:** thiếu đoạn giải thích hoàn thành Anh văn 1–4 là điều kiện về chuẩn trong quá trình học; đoạn yêu cầu chứng chỉ để tốt nghiệp đã được lấy.

### 4. Trích dẫn chưa đạt

**0/20 đáp án RAG có citation hợp lệ theo đúng mẫu `[chunk_id]` của prompt.** Đây là đánh giá về định dạng và ID, chưa phải thẩm định mọi kết luận được nguồn hỗ trợ.

- Audit cũ ghi 15 câu không có ID trong ngoặc vuông, 5 câu có nhãn ngoài context.
- Q05 trả `[TBC_ID]`; Q19 trả `[chunk_id]`.
- Q07 sinh `chunk_id_1` ngoài context nhưng audit không phát hiện vì mã không đặt trong ngoặc vuông.
- Q03 có nêu ID thật dưới dạng `[Chunk ID: ... - ...]`, nên không thể nói hoàn toàn không nhắc nguồn; dạng này không đúng hợp đồng citation, còn lẫn nguồn học phí không hỗ trợ kết luận về giới hạn tín chỉ.
- Các nhãn như `[TINH KIẾM]` hoặc `[TÀI LIỆU TRẢ LỜI]` là nhiễu đầu ra, không chứng minh có trích dẫn nguồn.

Danh sách `sources` do pipeline gắn kèm là **nguồn đã cung cấp cho model**, không phải xác nhận model đã dùng đúng nguồn đó để trả lời.

## Cần hiểu lại chỉ số retrieval hiện tại

Metric gốc chỉ khớp quote trong **phần thân** (`text[body_char_start:]`) và `pdf_pages`. Cách này tránh tính ngữ cảnh biên tập như trích dẫn gốc, nhưng bỏ sót phần **chú giải nguồn được lặp lại**, có vị trí trong `context_source_spans`.

Kiểm tra bổ sung giữ nguyên vector/thứ hạng, xét quote trong toàn bộ `text`, đúng tài liệu và trang nguồn của thân hoặc ngữ cảnh, đồng thời xác nhận quote có trong prompt thực tế:

| Chỉ số tại k=5 | Metric gốc: chỉ phần thân | Audit: toàn context đã gửi |
|---|---:|---:|
| Hit@5 | 95% | 95% |
| Evidence Recall@5, trung bình theo câu | 85% | **89,17%** |
| All Evidence Hit@5 | 70% | **80%** |

Khác biệt nằm ở **Q12: 1/2 → 2/2 bằng chứng** và **Q13: 2/3 → 3/3 bằng chứng**, do chú giải C5 đã được lặp trong chunk. Đây là hai cách đo khác nhau; số mới là audit bổ sung và không ghi đè CSV gốc. Không được coi context có chú giải là một bằng chứng bị thiếu khỏi đầu vào generator.

Audit vẫn dùng nhãn/quote tham chiếu hiện tại, chưa thay thế duyệt nguồn gốc. Số câu khớp reference và số câu có đầy đủ bằng chứng trong prompt là hai đại lượng khác nhau.

## Câu demo hiện tại

Với câu “Điều kiện đăng ký học phần tiên quyết là gì?”, model chuyển sang liệt kê chuỗi Anh văn 1–4 và ngoại lệ học song song, thay vì nêu điều kiện chung **phải học và thi đạt học phần tiên quyết**. Nó còn gắn phần trả lời vào Quy chế đào tạo 2026 trong khi các ví dụ Anh văn đến từ D04.

Định nghĩa chung đã có trong `D01_regulation_article_3_03`, rank 4. Vì vậy đây cũng là lỗi lệch trọng tâm của generator. Câu demo không được tính vào mẫu 20 câu ở bảng trên. Khi trình bày một ca thành công, có thể dùng output Q02, Q06 hoặc Q20 đã kiểm tra.

## Ưu tiên cải thiện

1. **Generator và kiểm tra đáp án:** yêu cầu trả lời tập trung theo đúng đối tượng/khóa/loại chương trình; thử generator khác và so sánh trên cùng bộ câu. Không mặc định model lớn hơn sẽ sửa hết lỗi.
2. **Trích dẫn:** yêu cầu câu trả lời kèm ID và quote hỗ trợ; xác thực ID có trong context và quote có trong nguồn. Kiểm tra cú pháp không thay cho kiểm tra nguồn có hỗ trợ kết luận. Placeholder hoặc câu trả lời không đạt phải được gắn trạng thái lỗi/chưa đủ căn cứ.
3. **Bảng và số học:** trích riêng tên ngành, tên cột, giá trị và đơn vị trước khi trả lời; dùng phép tính xác định cho so sánh giá, rồi kiểm tra lại kết quả. Q13 phải cho ra 40.000.
4. **Retrieval nhiều bằng chứng:** xử lý tham chiếu điều/mục và truy vấn phụ cho ngưỡng điểm, loại chương trình và chứng chỉ; kiểm tra riêng Q07, Q15–Q17.
5. **Đánh giá:** tách coverage phần thân với coverage toàn context; bổ sung kiểm tra citation ngoài mẫu ngoặc vuông. Nhóm nên chấm chéo trước khi dùng số liệu chất lượng trả lời trong báo cáo.

Baseline và RAG cùng model/decoding nhưng system prompt khác nhau. Vì vậy bảng này so sánh hai pipeline đang có; chưa cô lập hoàn toàn ảnh hưởng riêng của retrieval. Bộ câu hỏi cũng chưa phải tập kiểm thử độc lập đã được con người xác nhận.

## File đi kèm

- [Nhãn đánh giá và audit từng bằng chứng](output_review_2026-11-07.json): có SHA-256 của file đáp án đã đánh giá.
- [Đáp án và prompt thực tế](answers_comparison.json).
- [Cấu hình lần chạy](run_manifest.json).

Các điểm trong `manual_review.csv` được giữ trống để nhóm chấm độc lập; đánh giá này không ghi đè chúng.
