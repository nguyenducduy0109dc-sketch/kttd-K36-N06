# Ghi chú báo cáo Vòng 1 & Góp ý cải thiện - Tuần 6
- **Nhóm thực hiện:** K36-N06
- **Thành viên:** Nguyễn Đức Duy , Tùng Anh , Khang , Duy Anh , Phương
- **Đề tài:** Kiểm thử tự động Web the-internet bằng Selenium & Pytest

---

## 1. Các góp ý nhận được từ Giảng viên và Nhóm bạn (Ít nhất 3 góp ý)

### Góp ý 1: Về việc quản lý thời gian chờ (Wait) trong mã kiểm thử
- **Nội dung góp ý:** Nhóm hiện đang dùng `implicitly_wait(10)` cho toàn bộ driver. Cần tìm hiểu và áp dụng thêm `WebDriverWait` (Explicit Wait) kết hợp với `expected_conditions` cho các bài kiểm tra có phần tử tải động (Dynamic Loading) để test chạy ổn định hơn và tránh bị timeout ngẫu nhiên.

### Góp ý 2: Về cấu trúc mã nguồn và khả năng bảo trì (Page Object Model)
- **Nội dung góp ý:** Các locator (`By.ID`, `By.CSS_SELECTOR`) và thao tác đang viết trực tiếp bên trong từng hàm `test_*`. Nên chuyển đổi dần sang mô hình POM (Page Object Model) để tách riêng lớp giao diện (Page) và lớp kịch bản (Test Case), giúp dễ chỉnh sửa khi trang web đổi ID hay cấu trúc HTML.

### Góp ý 3: Về định dạng và cách lưu trữ ảnh minh chứng trên Git
- **Nội dung góp ý:** Cần chú ý lưu ảnh chụp màn hình đúng định dạng ảnh thật (PNG chuẩn xuất từ phần mềm Paint/Snipping Tool) trước khi commit; tránh tình trạng tạo file rỗng đổi tên khiến GitHub không thể hiển thị ảnh (lỗi invalid image source).

---

## 2. Kế hoạch và hành động nhóm sẽ cải thiện trong vòng tiếp theo

1. **Chuẩn hóa Wait:** Thay thế dần các đoạn chờ tĩnh hoặc ngầm định bằng `WebDriverWait` cho các nút bấm và thông báo flash.
2. **Triển khai kiến trúc POM:** Thiết kế thư mục `pages/` chứa các class tương ứng (ví dụ `LoginPage`, `SecurePage`) cho các bài kiểm thử tiếp theo.
3. **Mở rộng kịch bản kiểm thử:** Thực hiện thêm các bài kiểm thử tương tác nâng cao như Checkboxes, Dropdown, Alert, File Upload và Drag & Drop.
4. **Tích hợp báo cáo tự động:** Cấu hình thư viện `pytest-html` để xuất báo cáo kiểm thử dạng HTML trực quan nộp kèm minh chứng.