# Bộ Kịch bản Thuyết trình Trực tuyến (Online Seminar Scripts) — S07 RAG

Tài liệu hướng dẫn phối hợp và kịch bản chi tiết cho 3 thành viên trong buổi thuyết trình seminar trực tuyến (Google Meet / Zoom / MS Teams).

---

## 1. Phân chia File Kịch bản Cá nhân

Mỗi thành viên có một file kịch bản độc lập được biên soạn tỉ mỉ theo từng giây, có đầy đủ **lời thoại Tiếng Việt & Tiếng Anh**, **hướng dẫn thao tác phím / chuột**, **tín hiệu chuyển giao trực tuyến (Online Handoff Cues)** và **câu hỏi Q&A phụ trách**:

- **Speaker 1 (00:00 – 05:00):** [`SPEAKER_1_NAM_KIET.md`](SPEAKER_1_NAM_KIET.md) — *Lý thuyết Nền tảng, Kiến trúc Pipeline & Mô hình Xác suất* (Slides 01–07)
- **Speaker 2 (05:00 – 10:00):** [`SPEAKER_2_LE_HUY.md`](SPEAKER_2_LE_HUY.md) — *Corpus HCMUS, Thực nghiệm Retrieval & Worked Example Q01* (Slides 08–12)
- **Speaker 3 (10:00 – 15:00):** [`SPEAKER_3_TUAN_LINH.md`](SPEAKER_3_TUAN_LINH.md) — *Chất lượng Sinh ngữ 4 Nhánh, 5 Ca lỗi, Thảo luận & Hậu kiểm* (Slides 13–20)

---

## 2. Quy ước Thao tác Trình chiếu Trực tuyến (Online Presentation Protocol)

### 2.1. Thiết lập Màn hình & Âm thanh
1. **Chia sẻ màn hình (Screen Sharing):**
   - Đề xuất: **Speaker 1 (Nam Kiệt)** mở file [`slides/main.pdf`](../main.pdf) ở chế độ toàn màn hình (`Ctrl + L` trên Adobe Acrobat / Foxit Reader / Trình duyệt) và phụ trách share toàn bộ màn hình từ đầu đến cuối.
   - Khi Lê Huy hoặc Tuấn Lĩnh nói, người nói có thể trực tiếp nói khẩu lệnh tự nhiên: *"Nhờ Kiệt chuyển slide 8 giúp mình"* hoặc người share chủ động bấm phím `Space` khi người nói dứt câu chuyển ý.
   - *Phương án dự phòng:* Cả 3 thành viên đều mở sẵn file `main.pdf` trên máy cá nhân để sẵn sàng share thay thế nếu người share chính gặp sự cố mạng.
2. **Quy tắc Bật / Tắt Mic (Mic Etiquette):**
   - Chỉ người đang thuyết trình mới **Unmute mic**. Hai thành viên còn lại để **Mute** để tránh tạp âm vọng hoặc tiếng gõ phím.
   - Khi chuyển giao (ví dụ mốc 04:55 và 09:55): Người nói trước phát tín hiệu $\to$ Người nói sau bật mic, xác nhận $\to$ Người nói trước tắt mic.
3. **Con trỏ chuột thay cho Bút Laser (Virtual Mouse Pointer):**
   - Người share màn hình dùng chuột rê nhẹ hoặc khoanh tròn quanh các số liệu trọng tâm (như số **0.5280** ở Slide 07, con số **80.00%** và **89.17%** ở Slide 10, hay bảng 5 ca lỗi ở Slide 14).
4. **Lưu ý Đặc biệt tại Slide 15 (3 Cú Bấm Phím):**
   - Slide 15 (`15_discussion_hallucination.tex`) được thiết kế xuất hiện dần dần qua **3 lần bấm phím Space**:
     - *Bấm lần 1:* Hiện câu hỏi và chữ **NO** màu đỏ.
     - *Bấm lần 2:* Hiện tiếp Phần 2 (Paradigm Shift & Grounding Fallacy).
     - *Bấm lần 3:* Hiện tiếp Phần 3 (Cascading Errors & Corroboration).

---

## 3. Quy trình Dự phòng Mất kết nối Mạng (Network Failover Protocol)

Trong trường hợp bất khả kháng khi một thành viên bị rớt mạng hoặc mất tiếng đột ngột:
- Nếu **Nam Kiệt** bị ngắt kết nối: **Tuấn Lĩnh** chủ động bật mic nói thay phần lý thuyết của Kiệt.
- Nếu **Lê Huy** bị ngắt kết nối: **Nam Kiệt** chủ động nói thay phần thực nghiệm retrieval của Huy.
- Nếu **Tuấn Lĩnh** bị ngắt kết nối: **Lê Huy** chủ động nói thay phần kết luận và chuyển sang phiên Q&A.

---

## 4. Phối hợp trong Phiên Hỏi & Đáp Trực tuyến (15:00 – 20:00)

- Khi Giảng viên hoặc thành viên lớp đặt câu hỏi qua Micro hoặc gõ vào ô Chat của Google Meet / Zoom:
  - Cả 3 thành viên cùng chú ý lắng nghe, ghi chú nhanh từ khóa vào giấy hoặc chat nhóm riêng (Zalo/Messenger).
  - Thành viên phụ trách mảng đó (theo bảng phân công trong script) chủ động bật mic: *"Dạ em xin phép Thầy được trả lời câu hỏi này ạ..."*.
  - Các thành viên còn lại có thể bổ sung sau khi bạn mình hoàn thành câu trả lời: *"Dạ em xin bổ sung thêm một ý nhỏ..."*.
