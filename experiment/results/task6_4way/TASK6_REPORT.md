# Task 6 — So sánh chất lượng câu trả lời

Số câu hỏi: 20; cùng generator và cấu hình; mỗi câu có bốn điều kiện.

**Loại đánh giá: AI qualitative review, non-blind, provisional. Human review: pending.**

| Nhánh | Đúng nội dung chính (2 điểm) | Đúng một phần | Có khẳng định ngoài nguồn/sai nguồn | Từ chối/không trả lời |
|---|---:|---:|---:|---:|
| baseline | 0/20 (0.0%) | 15.0% | 75.0% | 40.0% |
| tfidf | 10/20 (50.0%) | 25.0% | 40.0% | 0.0% |
| bm25 | 9/20 (45.0%) | 30.0% | 35.0% | 0.0% |
| embedding | 10/20 (50.0%) | 30.0% | 30.0% | 0.0% |

## So sánh từng cặp với baseline

| Nhánh RAG | Baseline chưa đúng → RAG đúng | Baseline đúng → RAG chưa đúng | Chênh accuracy (điểm %) |
|---|---:|---:|---:|
| tfidf | 10 | 0 | +50.0 |
| bm25 | 9 | 0 | +45.0 |
| embedding | 10 | 0 | +50.0 |

## Diễn giải

Nhánh RAG có tỷ lệ đúng nội dung chính cao nhất trong lần chấm này: **tfidf, embedding (50.0%)**. Đây là đồng hạng, không có một phương pháp vượt riêng về chỉ số này. Không suy ra phương pháp tốt nhất nói chung từ bộ 20 câu hiện tại.
Giữ bảng đủ bốn nhánh. Có thể chọn một nhánh tiêu biểu để minh họa với baseline, nhưng không bỏ kết quả các nhánh khác hoặc chọn lại câu hỏi để làm tăng điểm.

## Điểm từng câu (0 sai/không trả lời; 1 một phần; 2 đúng nội dung chính)

| Câu | Không RAG | TF-IDF | BM25 | Embedding |
|---|---:|---:|---:|---:|
| Q01 | 0 | 0 | 0 | 2 |
| Q02 | 1 | 2 | 2 | 2 |
| Q03 | 1 | 1 | 1 | 1 |
| Q04 | 0 | 0 | 0 | 0 |
| Q05 | 0 | 0 | 1 | 0 |
| Q06 | 0 | 2 | 2 | 2 |
| Q07 | 0 | 0 | 0 | 0 |
| Q08 | 0 | 2 | 2 | 1 |
| Q09 | 0 | 2 | 2 | 2 |
| Q10 | 0 | 2 | 2 | 2 |
| Q11 | 1 | 1 | 1 | 1 |
| Q12 | 0 | 0 | 2 | 2 |
| Q13 | 0 | 1 | 0 | 0 |
| Q14 | 0 | 2 | 1 | 2 |
| Q15 | 0 | 2 | 2 | 1 |
| Q16 | 0 | 1 | 0 | 1 |
| Q17 | 0 | 1 | 1 | 2 |
| Q18 | 0 | 2 | 2 | 2 |
| Q19 | 0 | 2 | 1 | 1 |
| Q20 | 0 | 2 | 2 | 2 |

Điểm được tổng hợp từ manual_review.csv, không phải cosine hoặc điểm BM25. Citation hợp lệ về ID không tự chứng minh kết luận được nguồn hỗ trợ. Đây là bộ câu hỏi nhỏ đã có sẵn, không phải test độc lập; cần người thứ hai kiểm tra chéo các đánh giá.
