# Kịch bản Kiểm thử Chức năng 2 - Tuần 8 (Team W4)
- **Nhóm thực hiện:** K36-N06 (Team W4)
- **Chức năng kiểm thử:** Cookie, đăng nhập và lịch sử điều hướng (`/login`, `/secure`, `/status_codes`)
- **Công cụ:** Selenium WebDriver, Pytest, Explicit Waits (`WebDriverWait`)

---

## Danh sách Test Cases (Viết bằng lời trước khi viết code)

### TC01: Kiểm tra đăng nhập thành công (Trường hợp đúng - Positive Test)
- **Trang kiểm thử:** `https://the-internet.herokuapp.com/login`
- **Mục tiêu:** Xác nhận người dùng đăng nhập bằng tài khoản demo hợp lệ và được chuyển đến khu vực bảo mật.
- **Các bước thực hiện:**
  1. Mở trang `/login`.
  2. Nhập tên đăng nhập `tomsmith` và mật khẩu `SuperSecretPassword!`.
  3. Bấm nút đăng nhập.
  4. Chờ URL chứa `/secure` bằng `WebDriverWait` và kiểm tra nội dung thông báo tại `#flash`.
- **Kết quả kỳ vọng:** URL kết thúc bằng `/secure` và trang hiển thị thông báo `You logged into a secure area!`.

---

### TC02: Kiểm tra lấy danh sách cookie sau khi đăng nhập
- **Trang kiểm thử:** `https://the-internet.herokuapp.com/login` -> `/secure`
- **Mục tiêu:** Xác nhận WebDriver lấy được danh sách cookie hiện có sau khi đăng nhập.
- **Các bước thực hiện:**
  1. Đăng nhập bằng tài khoản demo hợp lệ.
  2. Gọi `driver.get_cookies()` để lấy danh sách cookie.
  3. Kiểm tra kiểu dữ liệu trả về và in tên các cookie để quan sát.
- **Kết quả kỳ vọng:** `get_cookies()` trả về một danh sách (`list`). Không cố định tên cookie vì ứng dụng demo có thể thay đổi cách tạo cookie.

---

### TC03: Kiểm tra lấy cookie theo tên
- **Trang kiểm thử:** `https://the-internet.herokuapp.com/login`
- **Mục tiêu:** Xác nhận có thể truy xuất một cookie cụ thể bằng `get_cookie(name)`.
- **Các bước thực hiện:**
  1. Mở trang `/login` để trình duyệt ở đúng domain.
  2. Thêm cookie `t8_test` với giá trị `cookie_demo` và đường dẫn `/`.
  3. Gọi `driver.get_cookie("t8_test")`.
  4. Kiểm tra cookie được trả về và có giá trị tương ứng.
- **Kết quả kỳ vọng:** Cookie `t8_test` tồn tại và giá trị bằng `cookie_demo`.

---

### TC04: Kiểm tra thêm cookie
- **Trang kiểm thử:** `https://the-internet.herokuapp.com/login`
- **Mục tiêu:** Xác nhận WebDriver thêm được cookie vào trình duyệt khi đã mở trang thuộc domain tương ứng.
- **Các bước thực hiện:**
  1. Mở trang `/login`.
  2. Thêm cookie `t8_added` với giá trị `selenium_week8` và đường dẫn `/`.
  3. Đọc lại cookie bằng `driver.get_cookie("t8_added")`.
- **Kết quả kỳ vọng:** Cookie `t8_added` được thêm thành công và có giá trị `selenium_week8`.

---

### TC05: Kiểm tra xóa một cookie
- **Trang kiểm thử:** `https://the-internet.herokuapp.com/login`
- **Mục tiêu:** Xác nhận có thể xóa riêng một cookie mà không cần xóa tất cả cookie.
- **Các bước thực hiện:**
  1. Mở trang `/login` và thêm cookie thử nghiệm `t8_delete`.
  2. Kiểm tra cookie tồn tại bằng `get_cookie`.
  3. Gọi `driver.delete_cookie("t8_delete")`.
  4. Truy xuất lại cookie cùng tên.
- **Kết quả kỳ vọng:** Cookie tồn tại trước khi xóa và không còn tồn tại sau khi xóa (`get_cookie` trả về `None`).

---

### TC06: Kiểm tra xóa tất cả cookie
- **Trang kiểm thử:** `https://the-internet.herokuapp.com/login`
- **Mục tiêu:** Xác nhận lệnh `delete_all_cookies()` xóa toàn bộ cookie của domain hiện tại.
- **Các bước thực hiện:**
  1. Mở trang `/login`.
  2. Thêm hai cookie thử nghiệm `t8_a` và `t8_b`.
  3. Gọi `driver.delete_all_cookies()`.
  4. Lấy lại danh sách cookie bằng `driver.get_cookies()`.
- **Kết quả kỳ vọng:** Danh sách cookie sau khi xóa là rỗng (`[]`).

---

### TC07: Kiểm tra phiên đăng nhập sau khi làm mới trang
- **Trang kiểm thử:** `https://the-internet.herokuapp.com/login` -> `/secure`
- **Mục tiêu:** Xác nhận phiên đăng nhập vẫn được duy trì sau thao tác làm mới trang.
- **Các bước thực hiện:**
  1. Đăng nhập bằng tài khoản demo hợp lệ.
  2. Gọi `driver.refresh()`.
  3. Chờ URL chứa `/secure`.
  4. Kiểm tra nút đăng xuất có nội dung `Logout`.
- **Kết quả kỳ vọng:** Trình duyệt vẫn ở trang `/secure` và nút `Logout` hiển thị sau khi tải lại.

---

### TC08: Kiểm tra điều hướng back, forward và URL hiện tại
- **Trang kiểm thử:** `https://the-internet.herokuapp.com/login` và `/status_codes`
- **Mục tiêu:** Xác nhận lịch sử điều hướng của trình duyệt hoạt động đúng.
- **Các bước thực hiện:**
  1. Mở trang `/login` và kiểm tra URL.
  2. Mở trang `/status_codes` và kiểm tra URL.
  3. Gọi `driver.back()` rồi chờ URL chứa `/login`.
  4. Gọi `driver.forward()` rồi chờ URL chứa `/status_codes`.
- **Kết quả kỳ vọng:** URL lần lượt khớp với trang đăng nhập, trang Status Codes, quay lại trang đăng nhập và tiến tới trang Status Codes; không dùng `time.sleep`.

---

### TC09: Kiểm tra tìm liên kết bằng link text và mở mã trạng thái 200
- **Trang kiểm thử:** `https://the-internet.herokuapp.com/status_codes` -> `/status_codes/200`
- **Mục tiêu:** Xác nhận có thể tìm liên kết `200` bằng `By.LINK_TEXT` và mở đúng trang đích.
- **Các bước thực hiện:**
  1. Mở trang `/status_codes`.
  2. Tìm và bấm liên kết có nội dung `200` bằng `By.LINK_TEXT`.
  3. Chờ URL chứa `/status_codes/200`.
  4. Kiểm tra URL và nội dung trang.
- **Kết quả kỳ vọng:** URL kết thúc bằng `/status_codes/200` và nội dung trang có mã `200`.

---

### TC10: Kiểm tra WebDriver tương thích với chế độ local hoặc remote
- **Trang kiểm thử:** `https://the-internet.herokuapp.com/login`
- **Mục tiêu:** Xác nhận test có thể chạy với Chrome local hoặc Selenium Grid được cấu hình qua biến môi trường `SELENIUM_REMOTE_URL`.
- **Các bước thực hiện:**
  1. Khởi tạo WebDriver: dùng Chrome local nếu không có `SELENIUM_REMOTE_URL`, hoặc Remote WebDriver nếu biến này được cấu hình.
  2. Mở trang `/login`.
  3. Kiểm tra tiêu đề trang và `session_id` của WebDriver.
- **Kết quả kỳ vọng:** Tiêu đề là `The Internet` và WebDriver có `session_id`. Khi chạy chế độ remote, Selenium Grid/Remote server phải đang hoạt động.
