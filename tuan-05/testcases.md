# Kịch bản kiểm thử Tuần 5: Chức năng Đăng nhập (Login)
- **Hệ thống kiểm thử:** https://the-internet.herokuapp.com/login
- **Tài khoản hợp lệ:** tomsmith / SuperSecretPassword!

| Mã testcase | Tên kịch bản | Dữ liệu đầu vào | Kết quả mong đợi |
| :--- | :--- | :--- | :--- |
| **TC01** | Đăng nhập thành công với tài khoản đúng | User: `tomsmith`<br>Pass: `SuperSecretPassword!` | Chuyển hướng sang trang `/secure`, hiển thị thông báo flash xanh "You logged into a secure area!" |
| **TC02** | Đăng nhập thất bại do sai Username | User: `sai_user`<br>Pass: `SuperSecretPassword!` | Ở lại trang login, hiển thị thông báo flash đỏ "Your username is invalid!" |
| **TC03** | Đăng nhập thất bại do sai Password | User: `tomsmith`<br>Pass: `sai_pass` | Ở lại trang login, hiển thị thông báo flash đỏ "Your password is invalid!" |
| **TC04** | Đăng nhập thất bại khi để trống cả 2 ô | User: ` ` (rỗng)<br>Pass: ` ` (rỗng) | Ở lại trang login, hiển thị thông báo flash đỏ cảnh báo lỗi |
| **TC05** | Đăng xuất thành công sau khi đã đăng nhập | Nhấn nút "Logout" tại trang `/secure` | Quay lại trang `/login`, hiển thị thông báo flash xanh "You logged out of the secure area!" |