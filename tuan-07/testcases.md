# Kịch bản Kiểm thử Chức năng 2 - Tuần 7 (Team W4)
- **Nhóm thực hiện:** K36-N06 (Team W4)
- **Chức năng kiểm thử:** Thông báo ngẫu nhiên & Chuyển hướng (`/notification_message`, `/redirector`)
- **Công cụ:** Selenium WebDriver, Pytest, Explicit Waits (`WebDriverWait`)

---

## Danh sách Test Cases (Viết bằng lời trước khi viết code)

### TC01: Kiểm tra hiển thị và làm mới thông báo ngẫu nhiên (Trường hợp đúng - Positive Test)
- **Trang kiểm thử:** `https://the-internet.herokuapp.com/notification_message_rendered`
- **Mục tiêu:** Xác nhận khi bấm vào liên kết "Click here", thông báo cũ biến mất khỏi DOM (`staleness_of`), thông báo mới hiện ra (`visibility_of_element_located`) với nội dung hợp lệ, và kiểm tra thao tác làm mới trang (`refresh`).
- **Các bước thực hiện:**
  1. Mở trang `/notification_message_rendered`.
  2. Chờ phần tử thông báo đầu tiên (`#flash`) hiển thị trên màn hình.
  3. Bấm vào nút "Click here" để yêu cầu tải thông báo mới.
  4. Chờ cho phần tử thông báo cũ không còn tồn tại trong DOM (`EC.staleness_of`) và chờ phần tử thông báo mới hiển thị (`EC.visibility_of_element_located`).
  5. Đọc nội dung văn bản của thông báo mới và thực hiện làm mới trang (`driver.refresh()`).
- **Kết quả kỳ vọng:** Nội dung thông báo thuộc một trong các thông điệp hợp lệ của hệ thống (`Action successful`, `Action unsuccesful, please try again`, hoặc `Action unsuccessful`).

---

### TC02: Kiểm tra chuyển hướng trang và điều hướng lịch sử trình duyệt (Trường hợp đúng - Positive Test)
- **Trang kiểm thử:** `https://the-internet.herokuapp.com/redirector`
- **Mục tiêu:** Xác nhận liên kết chuyển hướng đưa người dùng sang đúng trang `/status_codes` và kiểm tra tính năng quay lại trang trước (`back`).
- **Các bước thực hiện:**
  1. Mở trang `/redirector` và kiểm tra URL hiện tại (`current_url`).
  2. Chờ liên kết chuyển hướng (`#redirect`) hiển thị và bấm vào liên kết đó.
  3. Dùng `WebDriverWait` với `EC.url_contains("/status_codes")` để chờ trình duyệt chuyển hướng hoàn tất.
  4. Kiểm tra `driver.current_url` đã đổi sang trang Status Codes.
  5. Gọi lệnh `driver.back()` để quay lại trang trước đó và chờ URL quay về `/redirector`.
- **Kết quả kỳ vọng:** Trình duyệt chuyển hướng chính xác sang `/status_codes` và quay về lại `/redirector` thành công khi gọi `back()`, không dùng `time.sleep`.

---

### TC03: Kiểm tra chuyển hướng vào mã trạng thái lỗi máy chủ 500 và xác nhận không chứa thông báo thành công (Trường hợp sai - Negative Test)
- **Trang kiểm thử:** `https://the-internet.herokuapp.com/redirector` -> `/status_codes/500`
- **Mục tiêu:** Kiểm tra trường hợp điều hướng vào đường dẫn trả về mã lỗi HTTP 500 (Internal Server Error) và xác nhận hệ thống báo lỗi chứ không trả về trạng thái thành công (200 OK).
- **Các bước thực hiện:**
  1. Từ trang `/redirector`, bấm chuyển hướng sang `/status_codes`.
  2. Bấm chọn liên kết mã lỗi `500` (trường hợp lỗi máy chủ).
  3. Chờ URL chuyển sang `/status_codes/500` bằng `EC.url_contains("status_codes/500")`.
  4. Chờ đoạn văn bản thông báo kết quả hiển thị (`EC.visibility_of_element_located`).
  5. Kiểm tra nội dung trang báo mã lỗi 500 và khẳng định trang **không** hiển thị trạng thái thành công `200 status code`.
- **Kết quả kỳ vọng:** URL chứa `/status_codes/500`, nội dung xác nhận mã lỗi 500 và hoàn toàn không chứa thông báo của mã 200.