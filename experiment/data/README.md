# Corpus HCMUS — 4 tài liệu, đủ 51/51 trang

Phiên bản hiện tại: `full_document_v3`. Mọi trang của bốn PDF đã có văn bản trong corpus; không chọn bỏ điều, khoản hoặc phụ lục theo bộ câu hỏi.

## Tài liệu và nguồn

| Mã | Văn bản | Trang PDF trong corpus | PDF gốc |
|---|---|---|---|
| D01 | Quy chế đào tạo 2026, QĐ3087 ngày 29/09/2026 | 1–21 (21/21) | [Mở PDF](raw/D01_quy_che_dao_tao_2026.pdf) |
| D02 | Quy chế điểm rèn luyện 2020, phụ lục và sửa đổi QĐ2739 ngày 12/12/2023 | 1–16 (16/16) | [Mở PDF](raw/D02_quy_che_diem_ren_luyen_2020_sua_2023.pdf) |
| D03 | Học phí 2026–2027, QĐ3317 ngày 14/10/2026, khóa 2022–2026 | 1–5 (5/5) | [Mở PDF](raw/D03_hoc_phi_2026_2027_K2022_ve_sau.pdf) |
| D04 | Học ngoại ngữ và chuẩn ngoại ngữ tốt nghiệp, QĐ2464 ngày 11/08/2026 | 1–9 (9/9) | [Mở PDF](raw/D04_chuan_ngoai_ngu_tot_nghiep_2026.pdf) |
| **Tổng** | **4 tài liệu** | **51/51** | |

Nguồn công bố:

- D01: https://hcmus.edu.vn/quy-che-dao-tao-trinh-do-dai-hoc-nam-2026/
- D02: https://hcmus.edu.vn/quy-che-danh-gia-ket-qua-ren-luyen-sinh-vien-he-chinh-quy/
- D03: https://hcmus.edu.vn/thong-bao-nop-hoc-phi-hoc-ky-1-2026-2027-chuong-trinh-dai-tra/
- D04: https://hcmus.edu.vn/quy-dinh-ve-viec-hoc-ngoai-ngu-va-chuan-trinh-do-ngoai-ngu-khi-tot-nghiep-dai-hoc/

## Đọc và dùng dữ liệu

- [Corpus gộp toàn bộ](processed/corpus_all.md).
- [D01 toàn bộ](processed/D01_corpus.md), [D02 toàn bộ](processed/D02_corpus.md), [D03 toàn bộ](processed/D03_corpus.md), [D04 toàn bộ](processed/D04_corpus.md).
- [Đầu vào retrieval theo trang](processed/corpus_pages.json): `doc_id`, `pdf_page`, `section`, `text`, URL, phiên bản và trạng thái chất lượng.
- [Báo cáo độ phủ](coverage_report.json): danh sách trang của từng PDF, kiểm tra thiếu/trùng và trạng thái kiểm chứng.
- [Metadata nguồn](sources.json), [thống kê](corpus_manifest.json).
- [20 câu hỏi và bằng chứng](questions.md), [JSON đánh giá](questions.json).

Mọi điều của quy chế đào tạo, kể cả các Điều 1–2, 8–24 từng bị loại, đã được đưa trở lại. Giữ cả phụ lục gốc, bản sửa đổi điểm rèn luyện, căn cứ văn bản, bảng và công thức; không tóm tắt để thay thế nội dung các trang. Dấu mộc/chữ ký hình ảnh vẫn có trong PDF gốc, không được chuyển thành nội dung quy định mới.

## Độ phủ và chất lượng là hai việc khác nhau

**Đủ 51 trang không có nghĩa mọi ký tự OCR đã được kiểm chứng chính xác.**

- 22 trang đã có bản chép/khôi phục bảng theo ảnh, gắn `assistant_visual_transcription`.
- 29 trang có OCR toàn trang và một số sửa đoạn tham chiếu, gắn `ocr_needs_independent_review`. Có thể còn lỗi dấu tiếng Việt, khoảng trắng, số hoặc ký tự nhận dạng sai.
- Cả 51 trang vẫn có `human_review_status: pending`: chưa ghi nhận nhóm tự kiểm chứng độc lập.
- Bản OCR nguyên trạng của từng trang nằm trong `extracted/D01_ocr_pages.json` đến `D04_ocr_pages.json`, phục vụ đối chiếu, không đưa vào chỉ mục cùng bản chính vì gây lặp.
- Các bảng khó đã được chép lại trong `corrections/`: phụ lục rèn luyện, quy đổi điểm/xếp loại và kế hoạch/đánh giá Anh văn. Bảng học phí 27 ngành tiếp tục dùng bản đã đối chiếu.

Nhóm cần đối chiếu số liệu/điều kiện quan trọng với PDF khi làm thí nghiệm. `text_accuracy_fully_reviewed` hiện là `false`, không gắn nhãn dữ liệu đã sạch hoàn toàn.

## Phiên bản và các điều bị thay thế

- D01: giữ Điều 27 để xác định chuyển tiếp cho các khóa 2025 trở về trước.
- D02: trang 1–13 là quyết định, quy chế và phụ lục 2020; trang 14–16 là sửa đổi 2023. Giữ cả hai, không xóa bản gốc; khi hỏi theo phiên bản sau sửa đổi phải ưu tiên khoản được sửa. Metadata `revision_role` phân biệt hai vùng. Đây không phải văn bản hợp nhất chính thức.
- D02 có khác biệt số văn bản trong nguồn: trang đầu là 1028, phần sửa đổi dẫn chiếu 1208. Không tự sửa sự khác biệt này thành một con số duy nhất.
- D02 không được mặc định là mọi quy định mới nhất năm 2026. Sổ tay trực tuyến có bài trích lược theo Thông tư 40/2026 khác một số nội dung, nằm ngoài bộ bốn PDF này.
- D03: chỉ áp dụng năm học, chương trình và khóa nêu trong quyết định. Phân biệt tín chỉ học phí với tín chỉ học tập, và giữ ý nghĩa cột C1–C7 khi chia bảng.
- D04: phân biệt chuẩn trong quá trình học với chuẩn đầu ra; giữ chương trình và khóa tuyển.

## Tái tạo dữ liệu

Từ thư mục gốc repo:

```powershell
python -m pip install -r experiment/requirements.txt
python experiment/scripts/build_multi_document_dataset.py
```

Entry point cũ chuyển tới `build_full_document_dataset.py`. Script đọc bốn bản Markdown toàn văn, `source_catalog.json`, `page_review.json`, `questions.reference.json` và bản OCR lưu lại để kiểm tra. Không gọi mạng hoặc LLM, không cần model OCR khi chỉ build lại output. Script sẽ dừng nếu thiếu/trùng trang, PDF đổi hash hoặc mất bằng chứng.

Muốn chạy OCR lại từ PDF, xem hướng dẫn trong `experiment/README.md`. Không chạy OCR để tự ghi đè bản đã sửa bảng mà chưa kiểm tra.

## Bộ câu hỏi

Giữ 20 câu hỏi và 30 đoạn bằng chứng đã có, kiểm tra lại với corpus toàn bộ. Bộ 20 câu chưa bao phủ mọi điều khoản mới; không được mô tả nó là đánh giá đầy đủ mọi nội dung của 51 trang. `questions.reference.json` là đầu vào câu hỏi để chỉnh sửa lâu dài; `questions.json` và `questions.md` là output.

Không đưa câu hỏi/đáp án, `corrections/`, `extracted/` hoặc tài liệu hướng dẫn vào chỉ mục cùng corpus. Chỉ dùng `processed/corpus_pages.json`, sau đó gán gold chunks riêng theo từng cấu hình.
