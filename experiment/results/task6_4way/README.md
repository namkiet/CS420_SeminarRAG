# Task 6 — Kết quả Kaggle 4 nhánh và chấm AI ngày 08/11/2026

**Đã có 80 đáp án thật: 20 câu × không RAG / RAG TF-IDF / RAG BM25 / RAG embedding. Đã chấm sơ bộ bằng GPT; nhóm chưa duyệt độc lập.**

Nguồn là `s07_task6_4way_results.zip` người dùng tải từ Kaggle. SHA-256 archive: `d6e50bdd9631bb3252cb4fd9449ab5d0a843b0f1c11082ad6d1c0311eba7ad94`. Giữ nguyên archive gốc và các JSON đáp án/prompt, manifest, kế hoạch retrieval; điền điểm AI vào mẫu CSV đã tải. Mẫu điểm trống ban đầu vẫn nằm trong ZIP gốc.

**Phân biệt với benchmark khác:** [benchmark ba retriever ngày 08/11](../rag_methods_2026-11-08/README.md) có 60 đáp án, prompt riêng và output cap 384 token. Bộ này có 80 đáp án gồm baseline, output cap 768. Điểm và thứ tự phương pháp có thể khác; không gộp bảng, không suy một phương pháp tốt nhất từ hai cấu hình khác nhau.

## Kiểm tra tính hợp lệ của lần chạy

- Đủ Q01–Q20, mỗi câu có đủ 4 nhánh; không bỏ câu sai/khó khỏi mẫu số.
- Cùng Qwen2.5-1.5B-Instruct/revision, FP32 + SDPA, greedy, seed 42, max output 768; chạy trên Tesla T4.
- Hash corpus/câu hỏi/nguồn khớp repo; fingerprint cấu hình và retrieval plan khớp output.
- Đã dựng lại và kiểm tra cả 80 prompt từ câu hỏi và context IDs: cùng system prompt, baseline không có nguồn, không có reference answer do pipeline chèn vào prompt.
- Các nhánh RAG nhận đủ top-5 đã khóa. **0 chunks bị bỏ, 0 đáp án chạm trần output.**
- Không có đáp án RAG nào tạo citation `[chunk_id]` hợp lệ: **0/60**. Đúng nội dung và đúng citation được chấm tách biệt.

Chi tiết kiểm tra và quy ước được lưu trong [review_metadata.json](review_metadata.json). Các kiểm tra kỹ thuật không thay thế chấm nội dung hoặc xác minh OCR/PDF.

## Kết quả chấm sơ bộ

Điểm nội dung: `2` đúng nội dung trọng yếu và các điều kiện được hỏi; `1` đúng một phần/thiếu ý/có lỗi; `0` sai kết luận trọng yếu hoặc không trả lời. Completeness được chấm riêng 0–2; lỗi tên văn bản/provenance và khẳng định ngoài nguồn cũng ghi riêng. Không đồng nhất đáp án khớp reference với bằng chứng đã đủ trong prompt.

| Nhánh | Đúng chính | Một phần | Sai/không trả lời | Completeness trung bình (0–2) | Câu có khẳng định sai/ngoài nguồn gốc |
|---|---:|---:|---:|---:|---:|
| Không RAG | 0/20 — 0% | 3/20 | 17/20 | 0,15 | 15/20 — 75% |
| RAG TF-IDF | 10/20 — 50% | 5/20 | 5/20 | 1,25 | 8/20 — 40% |
| RAG BM25 | 9/20 — 45% | 6/20 | 5/20 | 1,20 | 7/20 — 35% |
| RAG embedding | 10/20 — 50% | 6/20 | 4/20 | 1,30 | 6/20 — 30% |

**Embedding và TF-IDF đồng hạng về tỷ lệ đúng nội dung chính.** Embedding nhỉnh hơn về completeness và ít khẳng định sai/ngoài nguồn hơn theo đánh giá AI này; chưa đủ cơ sở kết luận embedding tốt nhất nói chung. Cả ba nhánh đều không đạt yêu cầu citation-ID của prompt.

Nếu cần chọn một cặp để trình bày Task 6, có thể dùng **embedding RAG so với không RAG** vì đây là một nhánh trong nhóm có tỷ lệ đúng cao nhất. Tuy nhiên, vẫn phải trình bày bảng bốn nhánh và nói rõ TF-IDF đồng hạng, không bỏ các kết quả bất lợi.

## Các cặp minh họa nên dùng

| Câu | Quan sát từ output thật | Ý nghĩa |
|---|---|---|
| Q01 | Không RAG không phân biệt được hai khái niệm; embedding nêu đúng tiên quyết phải học và thi đạt, học trước chỉ yêu cầu hoàn thành quá trình học. TF-IDF/BM25 lạc sang ví dụ chuỗi Anh văn. | Minh họa một câu embedding có ích hơn các nhánh còn lại trong lần chạy này. |
| Q02 | Không RAG trả 30 giờ; cả ba RAG trả đúng 45–50 giờ, 60 phút/giờ và tổng khối lượng học tập. | Cung cấp nguồn cải thiện câu trả lời tra cứu trực tiếp, không chỉ riêng embedding. |
| Q05 | Không RAG, TF-IDF và embedding đều nói đủ tín chỉ là đủ tốt nghiệp. BM25 nêu được nhiều điều kiện nhưng bỏ điều kiện không đang bị đình chỉ. | Không có một nhánh trội trên mọi câu; đã có nguồn vẫn có thể trả lời sai. |
| Q12–Q13 | BM25/embedding trả đúng giá AI ở Q12 nhưng nhầm C1/C5 khi so sánh Q13. TF-IDF tính chênh 40.000 đúng ở Q13 nhưng gán nhãn C1 sai. | Tách lỗi đọc bảng, gán cột và phép tính; không chấm chỉ dựa vào một số xuất hiện đúng. |
| Q19 | TF-IDF nêu đúng 2 năm và các mốc nhưng bịa hậu tố quyết định; embedding bỏ thời hạn 2 năm. | Điểm nội dung, provenance và citation là các chiều riêng; không đánh đồng đáp án đúng chính với đáp án hoàn toàn đáng tin. |

Các điểm cần nhóm kiểm tra thêm: Q03, Q05, Q11, Q13–Q17, Q19. Ví dụ Q14 đúng kết luận/phạm vi nhưng thiếu lời nhắc tìm nguồn khác cho khóa 2020; Q15 trùng đáp án chuẩn chưa chứng minh toàn bộ ngưỡng IELTS được lấy trong prompt. Mọi điểm đều có lý do chi tiết trong CSV, không được trình bày là nhãn con người đã xác minh.

## Đoạn kết luận có thể dùng trong báo cáo

> Trên bộ 20 câu hỏi hiện tại, với cùng Qwen2.5-1.5B-Instruct và cấu hình sinh, nhánh không retrieval chưa có câu nào đạt mức đúng nội dung chính. TF-IDF RAG và embedding RAG cùng đạt 10/20 câu, BM25 RAG đạt 9/20 theo đánh giá AI sơ bộ. Kết quả cho thấy cung cấp tài liệu có thể cải thiện câu trả lời trong thí nghiệm này, nhưng chưa loại bỏ câu trả lời sai hoặc thiếu ý. Embedding có completeness trung bình cao hơn một chút, song đồng hạng TF-IDF về tỷ lệ đúng. Đặc biệt, cả 60 đáp án RAG đều không tuân thủ citation-ID. Cần nhóm kiểm tra độc lập điểm chấm và nguồn trước khi chốt kết luận.

## Đối chiếu Task 7 bạn cùng nhóm đã làm

Bạn cùng nhóm đã có [Task 7 cho lần chạy 05/11](../kaggle_2026-11-05/ERROR_ANALYSIS_AND_IMPROVEMENT_2026-11-07.md). Phân tích đó phù hợp output cũ và vẫn có giá trị. Task 6 mới không phủ nhận Task 7 cũ; hai tài liệu phải ghi rõ lần chạy thay vì gộp các con số.

Đã kiểm tra trực tiếp: hash corpus/câu hỏi/nguồn và SHA generator trùng nhau; **cả 20 câu embedding có cùng thứ tự context IDs và cùng user prompt/context**. System prompt khác, và output cap đổi từ 384 sang 768. Vì hai điều kiện thay đổi cùng lúc, chưa thể tách riêng tác động của mỗi thay đổi.

| Câu trong 8 ca lỗi nặng cũ | Lần embedding cũ 05/11 | Lần embedding mới | Đối chiếu |
|---|---|---|---|
| Q03 | Chọn sai 8–20 tín chỉ, tự mâu thuẫn và bị cắt output. | Có tối thiểu 12 và ngoại lệ đúng, thiếu tối đa 25; không bị cắt. | Cải thiện một phần; không còn dùng chẩn đoán cắt output cho lần mới. |
| Q04 | Đảo nhóm khóa áp dụng quy định mới. | Giữ nguyên đáp án sai đó. | Khớp, lỗi xử lý phạm vi vẫn còn. |
| Q05 | Chỉ sinh `[TBC_ID]`. | Khẳng định đủ tín chỉ là đủ tốt nghiệp. | Vẫn sai dù đã có nguồn, nhưng loại lỗi chuyển từ placeholder sang kết luận sai. |
| Q07 | Xếp 68 điểm thành Trung bình 50. | Vẫn trả Trung bình 50. | Khớp; thiếu ngưỡng xếp loại trong top-5 và chọn nhầm quy định. |
| Q12 | Trả 734.000, lấy nhầm cột. | Trả đúng 1.014.000. | Ca lỗi cũ đã không còn trong lần embedding mới. |
| Q13 | Hai giá đúng nhưng nhãn C1 sai, tính chênh 230.000 sai. | Lấy C1=488.000 cho cả hai ngành, kết luận chênh 0. | Vẫn lỗi đọc bảng, biểu hiện khác; không nói lần mới trừ ra 230.000. |
| Q16 | Cho hai nhóm cùng IELTS 4.5. | Phân biệt đúng bậc 3/6 và 4/6, chưa trả IELTS 4.5/5.0; gán sai số/ngày văn bản. | Cải thiện một phần; vẫn thiếu ngưỡng chứng chỉ trong context và trả chưa đủ câu hỏi. |
| Q19 | Trả nhầm nhánh chứng chỉ có ghi hiệu lực. | Chỉ nêu mốc bắt đầu, bỏ 2 năm và mốc kết thúc. | Vẫn chưa đáp ứng, nhưng không còn đúng nguyên mô tả lỗi cũ. |

Các kết luận chung vẫn thống nhất: đã nhận nguồn không đảm bảo LLM hiểu đúng; đọc điều kiện/cột bảng còn lỗi; citation và hậu kiểm chưa đạt; retrieval thiếu mảnh là vấn đề riêng. **Không dùng số 6/8 của Task 7 cũ để mô tả lần mới**, cũng không ghép accuracy 9/20 cũ với 10/20 mới như cùng một cấu hình. Lần mới có 4 câu embedding sai/không đạt điểm nội dung (Q04/Q05/Q07/Q13), 6 câu một phần và 10 câu đúng chính theo rubric AI hiện tại.

Khi tích hợp báo cáo: Task 6 dùng bảng bốn nhánh mới; Task 7 có thể giữ phân tích cũ với nhãn lần chạy, hoặc cập nhật ca lỗi theo output mới. Không cần làm lại công việc của bạn cùng nhóm chỉ vì các output mới khác; cần thống nhất nguồn số liệu và provenance.

## File và cách dùng

- [TASK6_REPORT.md](TASK6_REPORT.md): bảng tổng hợp và điểm từng câu, được tạo từ CSV.
- [answer_quality_summary.csv](answer_quality_summary.csv): số liệu tổng hợp 4 nhánh.
- [manual_review.csv](manual_review.csv): đủ 80 hàng điểm và lý do; `reviewer` ghi rõ GPT/AI, human review pending.
- [answers_comparison.json](answers_comparison.json): output mô hình thật và prompt đầy đủ.
- [generation_summary.csv](generation_summary.csv): token, thời gian, cờ cắt và citation-ID.
- [run_manifest.json](run_manifest.json), [retrieval_plan.json](retrieval_plan.json), [review_metadata.json](review_metadata.json): cấu hình và provenance.

Khi nhóm chỉnh điểm/duyệt lại, cập nhật reviewer/notes và trạng thái review. Tổng hợp lại từ thư mục gốc repo:

```powershell
python experiment/task6_comparison.py summarize --run-dir experiment/results/task6_4way
```

Lệnh này cập nhật CSV tổng hợp và `TASK6_REPORT.md`. Bảng diễn giải thủ công trong README này cần cập nhật tương ứng nếu điểm thay đổi.
