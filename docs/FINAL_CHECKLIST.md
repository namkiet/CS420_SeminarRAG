# G3 Task 7 — Checklist nghiệm thu

**Rà ngày 09/11/2026**, đối chiếu [yêu cầu G1–G3](TASKS.md), repo tại commit `01e4876` và [note Task 3](../report/G3_TASK3_REVIEW.md). Hai file Q&A/checklist được bổ sung trong đợt này; chưa thay report, outline hay kết quả gốc.

**Kết luận: chưa đủ bộ sản phẩm để nộp cuối.** Đã có report và kết quả thực nghiệm; còn sửa outline/nguồn worked example, hoàn thiện deck và xác nhận chạy thử. Phân công bên dưới là đề xuất theo phần đang phụ trách.

Quy ước: **Đạt** = có tài liệu/bằng chứng hiện tại; **Cần sửa** = đã xác định nội dung cần chỉnh; **Chưa có** = thiếu sản phẩm; **Chưa xác nhận** = cần kiểm tra thực tế. Đạt một mục không đồng nghĩa toàn bộ hệ thống không có lỗi.

## 1. Nội dung nghiên cứu và thực nghiệm

| Mục | Trạng thái | Bằng chứng / việc còn lại | Phụ trách đề xuất |
|---|---|---|---|
| Research question, nền tảng, phân biệt paper và kết quả nhóm | Đạt | [Report](../report/S07_Bao_Cao_RAG_HCMUS.pdf) trình bày RAG và giới hạn của kết luận từ 20 câu. | Kiệt, Lĩnh |
| Pipeline đầy đủ và failure points | Đạt | Sơ đồ ở report trang 4; [pipeline chi tiết](../research/G1_Task4_RAG_Pipeline.md). | Kiệt |
| Công thức và numerical example | Đạt | Report trang 3: Sequence=0,5280; Token=0,4692; không gọi triển khai Qwen là huấn luyện lại Lewis. | Kiệt |
| Corpus công khai, nguồn và phiên bản | Đạt | [sources.json](../experiment/data/sources.json), 4 PDF và 51 trang đã đối chiếu; giữ phạm vi áp dụng từng văn bản. Người phụ trách đã xác nhận kiểm tra dữ liệu. | Huy |
| Phạm vi corpus so với gợi ý đề | Chưa xác nhận | Đề gợi ý khoảng 5–10 trang, nhóm dùng 51; report đã nêu khác biệt. Đối chiếu cách giảng viên áp dụng yêu cầu này trước khi nộp. | Nhóm |
| 15–20 câu hỏi có đáp án và nguồn | Đạt | [questions.json](../experiment/data/questions.json): 20 câu, 30 nhóm evidence; đáp án chuẩn không được đưa vào chỉ mục/prompt sinh. | Huy |
| Chunking và retrieval code | Đạt | [162 chunks](../experiment/data/chunks/chunks_by_structure.json), 80 đơn vị cha; trần 800 token, lớn nhất 788. Có TF-IDF/BM25/embedding. | Huy, Kiệt, Lĩnh |
| So sánh ít nhất hai cấu hình retrieval | Đạt | [CSV benchmark](../experiment/results/rag_methods_2026-11-08/retrieval_summary.csv) có k=1/3/5; không cần khẳng định đã thử nhiều chunk size. | Huy |
| Hit Rate / Recall@k có định nghĩa và mẫu số | Đạt | Report trang 6 và [benchmark](../experiment/results/rag_methods_2026-11-08/README.md); phân biệt Hit, Evidence Recall, All Evidence, MRR. | Huy |
| Worked example trong report | Đạt | Report trang 5 có Q01 → evidence → prompt/đáp án; đã phân biệt citation do nhóm bổ sung với output thật. | Kiệt, Lĩnh |
| Nguồn worked example dùng để làm slides | Cần sửa | [G2_TASK_5.md](../research/G2_TASK_5.md) còn T01–T05: score, model 1.5B/7B, citation, trang/ý Điều 18 và kết luận vượt ví dụ. Dùng [note sửa](../report/G3_TASK3_REVIEW.md). | Kiệt |
| So sánh có/không retrieval | Đạt | [Task 6 bốn nhánh](../experiment/results/task6_4way/README.md): đủ 80 output, cùng Qwen/system/config; không lấy baseline khác lần chạy. | Huy |
| Điểm nội dung và citation được tách riêng | Đạt | [CSV chấm](../experiment/results/task6_4way/manual_review.csv) có lý do; nguồn gốc GPT được công khai, người phụ trách đã xác nhận kiểm tra. Không mô tả là chấm mù độc lập. | Huy |
| Kết luận đúng với bảng điểm | Đạt | TF-IDF/embedding cùng 10/20, BM25 9/20, baseline 0/20; cả 60 đáp án RAG thiếu citation-ID hợp lệ. Đây là hạn chế cần báo cáo. | Huy, Lĩnh |
| Ít nhất 3 failure cases | Đạt | Report trang 7 có 5 ca của lần mới, gồm Q07/Q01/Q05/Q13/Q19; không trộn lỗi cũ với output mới. | Lĩnh |
| Đề xuất verification và cập nhật tài liệu | Đạt | Report trang 7–8; ghi rõ là đề xuất, chưa chứng minh hiệu quả bằng thí nghiệm bổ sung. | Lĩnh |

## 2. Report, slides và buổi trình bày

| Mục | Trạng thái | Bằng chứng / việc còn lại | Phụ trách đề xuất |
|---|---|---|---|
| Report tiếng Việt A4, 6–10 trang nội dung | Đạt | [PDF hiện tại](../report/S07_Bao_Cao_RAG_HCMUS.pdf): 8 trang nội dung + 1 references; đủ các phần chính, đã rà bố cục trong Task 3. | Lĩnh |
| Caption, baseline wording, nguồn và khai báo AI | Cần sửa | Bổ sung/làm rõ R03–R07 trong [note Task 3](../report/G3_TASK3_REVIEW.md); không tự điền model ID hay coi lỗi truy cập publisher là DOI sai. | Lĩnh |
| Outline thống nhất dữ liệu với report/log | Cần sửa | [OUTLINE.md](../slides/OUTLINE.md) còn S01–S07 mức P1; sau đó sửa S08–S11. Ưu tiên corpus, metric, score Q01, citation và run của failure cases. | Kiệt; Huy/Lĩnh đối chiếu |
| Deck hoàn chỉnh có 8–12 slides nội dung | Chưa có | Hiện chỉ có outline dự kiến 12 slide tổng, 10 slide nội dung; chưa có PPTX hoặc PDF deck. | Kiệt |
| Font, bảng, hình, phương trình và nguồn trên deck | Chưa xác nhận | Render/xem deck cuối; kiểm tra tính đọc được và không cắt hình, bảng hoặc công thức. Outline không thay bước này. | Huy, nhóm |
| Phân vai và timeline 15 phút | Đạt | Outline đã chia Kiệt 0–5 phút, Huy 5–10, Lĩnh 10–15. Đây là kế hoạch, chưa phải thời lượng đo. | Nhóm |
| Chạy thử đủ ba người trong 15 phút | Chưa xác nhận | Bấm giờ, ghi thời lượng từng người và tổng; rút gọn nếu vượt. Mọi người đều phải trình bày. | Nhóm |
| Bộ Q&A có đáp án, người chính/dự phòng, nguồn | Đạt | [QA.md](QA.md): 15 câu bao phủ lý thuyết, toán, retrieval, kết quả, hallucination và limitations. | Huy |
| Mỗi thành viên trả lời ít nhất một câu | Chưa xác nhận | Tập Kiệt Q03, Huy Q09/Q10, Lĩnh Q13; đổi câu để kiểm tra hiểu nội dung. Xác nhận thực tế trong phiên Q&A. | Nhóm |
| Thông tin thành viên hoàn chỉnh | Đạt | Đã cập nhật đầy đủ thông tin: Bùi Trọng Tuấn Lĩnh (`24125066`). | Lĩnh |

## 3. Bộ sản phẩm để nộp

| Sản phẩm | Hiện trạng |
|---|---|
| [Report PDF](../report/S07_Bao_Cao_RAG_HCMUS.pdf) | Có; rà lại sau khi cập nhật các note nguồn/caption. |
| Deck PPTX/PDF trong [slides/](../slides/) | Chưa có bản hoàn chỉnh. |
| [Code, corpus và hướng dẫn thực nghiệm](../experiment/README.md) | Có; giữ nguyên kết quả gốc và ghi đúng phiên bản/lần chạy. |
| [Retrieval benchmark](../experiment/results/rag_methods_2026-11-08/README.md) và [Task 6 bốn nhánh](../experiment/results/task6_4way/README.md) | Có; là hai nguồn khác nhau, không ghép điểm giữa các run. |
| [Note kiểm tra](../report/G3_TASK3_REVIEW.md), [Q&A](QA.md), checklist này | Có; checklist cần cập nhật sau khi nhóm sửa và chạy thử. |

## 4. Thứ tự chốt

- [ ] Kiệt sửa outline và worked example theo S01–S11/T01–T05; Huy kiểm số liệu, Lĩnh kiểm failure cases.
- [ ] Lĩnh làm rõ các mục report R03–R07 và hoàn thiện thông tin thành viên.
- [ ] Hoàn thiện deck, xuất PDF và rà hình/bảng/phương trình/citation.
- [ ] Cả nhóm chạy thử 15 phút và luyện Q&A; mỗi người trả lời ít nhất một câu.
- [ ] Đối chiếu yêu cầu phạm vi corpus; kiểm lại report/deck/bảng kết quả sau các chỉnh sửa.
- [ ] Chốt đúng các file cần nộp theo hướng dẫn lớp, cập nhật checklist và commit/push phiên bản cuối.

**Ghi nhận sau chạy thử:** ngày `…`; Kiệt `…` phút; Huy `…` phút; Lĩnh `…` phút; tổng `…` phút. Người rà bản cuối: `…`. Trạng thái nghiệm thu cuối: `…`.
