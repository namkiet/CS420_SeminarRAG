# G2 Task 3–4: TF-IDF retrieval

Đã chạy 20 câu hỏi trên 162 chunks, trần chunk 800 token.

## Cấu hình

- TF-IDF unigram + bigram, lowercase, giữ dấu tiếng Việt và token một ký tự/chữ số; không dùng stopword tiếng Anh.
- Token hóa theo regex/khoảng trắng, không phải bộ tách từ tiếng Việt. Chuẩn hóa Unicode NFC và khoảng trắng.
- `tf = 1 + ln(count)`, `idf = ln((1 + N)/(1 + df)) + 1`; chuẩn hóa L2 rồi tích vô hướng để tính cosine.
- Chỉ fit vocabulary/IDF trên `chunks[*].text`. Không fit câu hỏi, đáp án hoặc nhãn liên quan.
- Không lọc tài liệu theo gold, không sửa câu hỏi, không mở rộng truy vấn hoặc điều chỉnh tham số sau khi xem điểm.
- Hòa điểm giữ thứ tự corpus; query không có từ vựng chung trả danh sách rỗng, không lấy chunk điểm 0.

## Kết quả

| k | Hit Rate@k | Chunk Recall@k | Evidence Recall@k | Đủ mọi bằng chứng@k | MRR@k |
|---|---:|---:|---:|---:|---:|
| 1 | 75.00% | 63.33% | 70.83% | 65.00% | 0.7500 |
| 3 | 90.00% | 74.17% | 82.50% | 75.00% | 0.8250 |
| 5 | 90.00% | 75.83% | 82.50% | 75.00% | 0.8250 |

Tại k=5: tìm được ít nhất một bằng chứng cho 18/20 câu; đủ mọi bằng chứng cho 15/20 câu.
Không trúng bằng chứng trong top-5: Q07, Q14.
Chưa đủ mọi bằng chứng trong top-5: Q07, Q14, Q15, Q16, Q17.

## Quy ước chấm

- Gold được ánh xạ tự động từ 30 quote có sẵn, đúng tài liệu/trang và nguyên văn sau chuẩn hóa Unicode/khoảng trắng. Không dùng điểm TF-IDF để tạo gold.
- Ngoài phần thân, chấp nhận chú giải bảng được lặp nếu quote có trong ngữ cảnh và được xác nhận bằng `context_source_spans` trên trang gốc. Tiêu đề biên tập không đủ điều kiện.
- Một evidence group có thể có nhiều chunk thay thế. Lấy bất kỳ chunk nào trong group là đã tìm được bằng chứng đó.
- Hit Rate@k: tỷ lệ câu tìm được ít nhất một chunk liên quan.
- Chunk Recall@k: số chunk liên quan tìm được chia tổng số chunk liên quan của câu. Vì chú giải có thể lặp nhiều nơi, không bắt buộc lấy mọi chunk thay thế để có đủ bằng chứng.
- Evidence Recall@k: số nhóm bằng chứng được tìm thấy chia tổng số nhóm cần thiết của câu.
- Đủ mọi bằng chứng@k: tỷ lệ câu mà mọi nhóm bằng chứng đều được tìm thấy. MRR@k: nghịch đảo hạng đầu tiên trúng gold trong top-k.
- Mọi chỉ số được lấy trung bình trên đủ 20 câu (macro), không bỏ câu khó. CSV ghi số thập phân 0–1, bảng này hiển thị phần trăm.
- `body_only_evidence_recall` trong CSV chỉ xét phần thân, dùng đối chiếu cách đo của notebook embedding cũ. Không so trực tiếp Evidence Recall có ngữ cảnh với metric cũ chỉ phần thân.

## Đọc output

- `retrieval_summary.csv`: kết quả tổng hợp tại từng k.
- `retrieval_per_question.csv`: kết quả từng câu/từng k.
- `evaluation_details.json`: cấu hình, phiên bản/hash, nhãn liên quan, evidence groups, top-k và hạng bằng chứng đầu tiên.
- Chỉ mục TF-IDF được lưu trong `experiment/outputs/tfidf/index.joblib` (Git bỏ qua), có thể tạo lại bằng lệnh chạy. Chỉ tải file joblib do chính mình tạo/tin cậy.

## Chạy lại từ thư mục gốc repo

```powershell
.\.venv\Scripts\python.exe -m pip install -r experiment/requirements-tfidf.txt
.\.venv\Scripts\python.exe experiment/tfidf_retrieval.py --ks 1 3 5
```

Tra cứu riêng:

```powershell
.\.venv\Scripts\python.exe experiment/tfidf_retrieval.py --query "Học phần tiên quyết là gì?" --top-k 5
```

## Giới hạn

Đây là kết quả trên bộ 20 câu hiện tại, chưa phải tập test độc lập đã duyệt. Nhãn chỉ bao phủ các quote đã chọn, không khẳng định đã liệt kê mọi đoạn trả lời tương đương. OCR và human review vẫn pending; cần nhóm kiểm tra chéo nhãn. Điểm retrieval không phải độ chính xác câu trả lời của LLM. Chưa thực hiện generation trong lần chạy TF-IDF này.

[Tài liệu TfidfVectorizer của scikit-learn](https://scikit-learn.org/1.7/modules/generated/sklearn.feature_extraction.text.TfidfVectorizer.html)
