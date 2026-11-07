# G2 Task 3–4: BM25-only retrieval (Okapi BM25 — Lucene Non-negative IDF)

Đã chạy 20 câu hỏi trên 162 chunks, trần chunk 800 token.

## Cấu hình

- **Okapi BM25 (biến thể non-negative IDF của Apache Lucene)** với `n-gram (1, 2)`, lowercase, giữ dấu tiếng Việt và token một ký tự/chữ số; không dùng stopword tiếng Anh.
- Token hóa theo regex `r'(?u)\b\w+\b'` sau chuẩn hóa Unicode NFC và khoảng trắng (cùng không gian từ vựng với TF-IDF khi `ngram_range=(1, 2)`).
- Tham số cố định trước khi chạy: `k1 = 1.5`, `b = 0.75`, `avgdl = 382.52` (tính trên tổng n-gram trong phạm vi `(1, 2)`).
- Chỉ fit vocabulary, `df`, `idf`, `|d|` và `avgdl` trên `chunks[*].text`. Không fit câu hỏi, đáp án hoặc nhãn liên quan.
- Không lọc tài liệu theo gold, không sửa câu hỏi, không mở rộng truy vấn hoặc điều chỉnh `k1`, `b` sau khi xem điểm.
- Hòa điểm giữ thứ tự corpus; query không có từ vựng chung trả danh sách rỗng, không lấy chunk điểm 0.

## Công thức toán học (Okapi BM25 — Lucene Non-negative IDF)

Điểm xếp hạng giữa câu hỏi $q$ và chunk $d$ được tính theo công thức Okapi BM25 với thành phần IDF không âm:

$$\text{IDF}(t) = \ln\!\left(1 + \frac{N - \text{df}(t) + 0.5}{\text{df}(t) + 0.5}\right)$$

$$\text{score}(q, d) = \sum_{t \in q \cap V} \text{qtf}(t, q) \cdot \text{IDF}(t) \cdot \frac{\text{tf}(t, d) \cdot (k_1 + 1)}{\text{tf}(t, d) + k_1 \cdot \left(1 - b + b \cdot \frac{|d|}{\text{avgdl}}\right)}$$

Trong đó:
- $N = 162$: tổng số chunks trong chỉ mục; $|V| = 9817$: kích thước tập từ vựng `n-gram (1, 2)`.
- $\text{df}(t)$: số chunks chứa n-gram $t$ ($0 < \text{df}(t) \le N$).
- $\text{tf}(t, d)$, $\text{qtf}(t, q)$: số lần xuất hiện của n-gram $t$ trong chunk $d$ và trong câu hỏi $q$.
- $|d| = \sum_{t \in V} \text{tf}(t, d)$: độ dài chunk $d$; $\text{avgdl} = \frac{1}{N}\sum_{d=1}^{N} |d| = 382.52$.
- $k_1 = 1.5$: hệ số bão hòa tần suất từ; $b = 0.75 \in [0, 1]$: hệ số chuẩn hóa độ dài tài liệu.
- **Lý do dùng biến thể non-negative IDF (`1 + ...` của Lucene thay vì Robertson–Spärck Jones 1994 trần):** Công thức 1994 $\ln\frac{N - \text{df}(t) + 0.5}{\text{df}(t) + 0.5}$ nhận giá trị **âm** khi $\text{df}(t) > N/2$. Trong tập `162` chunks này có **41** từ/cụm từ xuất hiện ở trên một nửa số chunks (như `'quy chế'`, `'học'`, `'phần'`, `'đại'`), nên nếu không cộng `1 +` bên trong $\ln(\cdot)$, các chunk chứa từ khóa đúng của câu hỏi sẽ bị phạt điểm âm.

## Kết quả

| k | Hit Rate@k | Chunk Recall@k | Evidence Recall@k | Đủ mọi bằng chứng@k | MRR@k |
|---|---:|---:|---:|---:|---:|
| 1 | 85.00% | 70.00% | 80.00% | 75.00% | 0.8500 |
| 3 | 90.00% | 76.67% | 84.17% | 80.00% | 0.8667 |
| 5 | 90.00% | 78.33% | 84.17% | 80.00% | 0.8667 |

Tại k=5: tìm được ít nhất một bằng chứng cho 18/20 câu; đủ mọi bằng chứng cho 16/20 câu.
Không trúng bằng chứng trong top-5: Q07, Q14.
Chưa đủ mọi bằng chứng trong top-5: Q07, Q14, Q16, Q17.

## Đối chiếu với TF-IDF và BGE-M3 Embedding trên cùng 162 chunks

### 1. Theo quy ước chuẩn `align_gold` (phần thân + chú giải bảng lặp xác thực)

| k | Phương pháp | Hit Rate@k | Chunk Recall@k | Evidence Recall@k | Đủ mọi bằng chứng@k | MRR@k |
|---:|---|---:|---:|---:|---:|---:|
| 1 | TF-IDF cosine | 75.00% | 63.33% | 70.83% | 65.00% | 0.7500 |
| 1 | **BM25-only** | **85.00%** | **70.00%** | **80.00%** | **75.00%** | **0.8500** |
| 1 | BGE-M3 dense | 70.00% | 55.00% | 65.00% | 60.00% | 0.7000 |
| 3 | TF-IDF cosine | 90.00% | 74.17% | 82.50% | 75.00% | 0.8250 |
| 3 | **BM25-only** | **90.00%** | **76.67%** | **84.17%** | **80.00%** | **0.8667** |
| 3 | BGE-M3 dense | 85.00% | 73.33% | 81.67% | 75.00% | 0.7667 |
| 5 | TF-IDF cosine | 90.00% | 75.83% | 82.50% | 75.00% | 0.8250 |
| 5 | **BM25-only** | **90.00%** | **78.33%** | **84.17%** | **80.00%** | **0.8667** |
| 5 | BGE-M3 dense | 95.00% | 82.50% | 89.17% | 80.00% | 0.7867 |

### 2. Theo quy ước `body_only` (chỉ tính phần thân — quy ước gốc của notebook Kaggle)

| k | TF-IDF (`body_only` Evidence Recall) | **BM25-only** (`body_only` Evidence Recall) | BGE-M3 dense (`body_only` Evidence Recall) |
|---:|---:|---:|---:|
| 1 | 69.17% | **75.83%** | 60.83% |
| 3 | 82.50% | **82.50%** | 77.50% |
| 5 | 82.50% | **82.50%** | 85.00% |

## Nhận xét kết quả

- **Ảnh hưởng của k (`k = 1, 3, 5`):** Bước tăng rõ nhất của BM25 diễn ra từ `k=1` lên `k=3` (`Hit Rate` từ `85.00%` lên `90.00%`, `Evidence Recall` từ `80.00%` lên `84.17%`, tỷ lệ câu đủ mọi bằng chứng từ `75.00%` lên `80.00%`). Từ `k=3` lên `k=5`, `Chunk Recall` tăng thêm (`76.67%` lên `78.33%`) nhờ thu hồi thêm mảnh thay thế có chú giải lặp.
- **BM25-only vs. TF-IDF cosine (cùng ma trận `162 x 9817` đặc trưng `(1, 2)`, `nnz = 37865`):** BM25 vượt TF-IDF ở mọi giá trị `k`, rõ nhất tại `k=1` (`Hit Rate@1` +10 điểm %, `Evidence Recall@1` +9.17 điểm %, `MRR@1` +0.1000) nhờ bão hòa tần suất từ (`k1 = 1.5`) và chuẩn hóa độ dài theo `|d|/avgdl` (`b = 0.75`). BM25 đưa bằng chứng đúng lên hạng 1 ở `Q05`, `Q16`, chọn ngay mảnh chứa cả dòng ngành lẫn chú giải ở `Q12`, và kéo mảnh thiếu của `Q15` từ hạng 11 (TF-IDF) vào hạng 3.
- **BM25-only vs. BGE-M3 dense embedding (bù trừ giữa khớp từ khóa và ngữ nghĩa):** Tại `k=1` và `k=3` (cũng như `MRR` ở cả 3 mức `k`), **BM25-only vượt BGE-M3** (`Hit Rate@1`: `85.00%` so với `70.00%`; `Evidence Recall@1`: `80.00%` so với `65.00%`; `MRR@5`: `0.8667` so với `0.7867`) do văn bản quy chế có nhiều mốc điều khoản, mã cột (`C5`), mức điểm và thuật ngữ chính xác (`Q06`, `Q08`, `Q10` đạt hạng 1 ở BM25 nhưng hạng 2–3 ở BGE-M3; `Q15` lấy đủ 3/3 mảnh ở `k=3` với BM25 trong khi BGE-M3 thiếu mảnh IELTS 4.5 ở ngoài top-5). Ngược lại, tại `k=5`, **BGE-M3 vượt lên về độ phủ rộng** (`Hit Rate@5 = 95.00%`, `Evidence Recall@5 = 89.17%`, cùng đạt `All Evidence@5 = 80.00%` như BM25) nhờ bắt được ngữ nghĩa khi câu hỏi lệch từ khóa nguyên văn (`Q14` hỏi `khóa tuyển 2020` trên văn bản ghi `2022–2026` được BGE-M3 xếp hạng 5 trong khi BM25 xếp hạng 13; `Q16` lấy được 2/3 mảnh trong top-5). Sự bù trừ này là cơ sở thực nghiệm trực tiếp để đề xuất **Hybrid Retrieval (BM25 + Dense Embedding)** ở phần cải thiện.

## Quy ước chấm

- Gold được ánh xạ tự động từ 30 quote có sẵn, đúng tài liệu/trang và nguyên văn sau chuẩn hóa Unicode/khoảng trắng. Không dùng điểm BM25 để tạo gold.
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
- Chỉ mục BM25 được lưu trong `experiment/outputs/bm25/index.joblib` (Git bỏ qua), có thể tạo lại bằng lệnh chạy. Chỉ tải file joblib do chính mình tạo/tin cậy.

## Chạy lại từ thư mục gốc repo (với `uv venv`)

```powershell
uv venv --allow-existing .venv
uv pip install --python .venv -r experiment/requirements-bm25.txt
uv run --python .venv python experiment/bm25_retrieval.py --ks 1 3 5
```

Tra cứu riêng:

```powershell
uv run --python .venv python experiment/bm25_retrieval.py --query "Học phần tiên quyết là gì?" --top-k 5
```

## Giới hạn

Đây là kết quả trên bộ 20 câu hiện tại, chưa phải tập test độc lập đã duyệt. Nhãn chỉ bao phủ các quote đã chọn, không khẳng định đã liệt kê mọi đoạn trả lời tương đương. OCR và human review vẫn pending; cần nhóm kiểm tra chéo nhãn. Điểm retrieval không phải độ chính xác câu trả lời của LLM. Chưa thực hiện generation trong lần chạy BM25 này.

Tham khảo công thức: Robertson, S., & Zaragoza, H. (2009). *The Probabilistic Relevance Framework: BM25 and Beyond*; Kamphuis, C., et al. (2020). *Which BM25 Do You Mean? A Large-Scale Reproducibility Study of Scoring Variants* (ECIR 2020 — biến thể Lucene non-negative IDF).
