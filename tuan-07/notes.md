# Ghi chú Học tập & Báo cáo Thí nghiệm - Tuần 7 (Team W4)
- **Nhóm thực hiện:** K36-N06 (Team W4)
- **Chủ đề Tuần 7:** Chờ đúng lúc (Explicit Waits) & Chức năng 2: Thông báo ngẫu nhiên (`/notification_message`) và Chuyển hướng (`/redirector`)

---

## 1. Trả lời câu hỏi phần Đọc tài liệu trước buổi học

### Câu 1: Vì sao không nên dùng lệnh `time.sleep()` để chờ trong kiểm thử tự động?
- **Trả lời:**
  1. **Gây lãng phí thời gian (Làm chậm bộ test):** Nếu đặt `time.sleep(5)` nhưng phần tử chỉ mất `0.5s` để xuất hiện, bài test vẫn bị ép chờ đủ 5 giây vô ích. Khi dự án có nhiều test case, tổng thời gian chạy sẽ bị kéo dài rất lâu.
  2. **Thiếu ổn định (Flaky Test):** Nếu mạng chậm hoặc server phản hồi mất `5.5s` (lâu hơn mức `time.sleep(5)` cố định), bài kiểm thử sẽ lập tức văng lỗi `NoSuchElementException` dù ứng dụng vẫn hoạt động đúng.
  3. **Giải pháp thay thế:** Dùng `WebDriverWait` (Explicit Wait) giúp kiểm tra điều kiện liên tục (mặc định mỗi 0.5s) — phần tử vừa xuất hiện là chạy tiếp ngay, chỉ báo lỗi `TimeoutException` khi vượt quá ngưỡng thời gian tối đa.

### Câu 2: Chờ "phần tử hiển thị" (`visibility_of_element_located`) khác chờ "phần tử bấm được" (`element_to_be_clickable`) thế nào?
- **Trả lời:**
  - **`EC.visibility_of_element_located`:** Kiểm tra phần tử đã có mặt trong cây DOM và hiển thị trên giao diện (không bị `display: none` hay `visibility: hidden`, kích thước lớn hơn 0). Dùng khi cần đọc nội dung văn bản (`.text`) hoặc xác nhận thông báo xuất hiện.
  - **`EC.element_to_be_clickable`:** Ngoài việc phần tử phải hiển thị (`visible`), nó còn kiểm tra thêm điều kiện phần tử đó **đang ở trạng thái kích hoạt (`enabled` / không bị `disabled`)** và sẵn sàng nhận thao tác click chuột. Dùng trước khi thực hiện lệnh `.click()`.

---

## 2. Nhận xét về Thí nghiệm có và không có lệnh chờ (Trang `/dynamic_loading/1`)

Nhóm đã thực hiện thí nghiệm trên trang `https://the-internet.herokuapp.com/dynamic_loading/1` (nơi phần tử `#finish` chứa dòng chữ `"Hello World!"` bị ẩn và chỉ hiện ra sau khoảng 5 giây kể từ khi bấm nút `Start`):

| Trường hợp thí nghiệm | Cách viết code | Kết quả chạy thực tế | Giải thích nguyên nhân |
| :--- | :--- | :--- | :--- |
| **TH1: Không có lệnh chờ** | Bấm nút `Start` xong gọi ngay `driver.find_element(By.ID, "finish").text` | **FAILED** (Chuỗi trả về rỗng `""` khi assert `"Hello World!"`) | Khi vừa bấm `Start`, thanh loading đang chạy, thẻ `#finish` tuy có trong DOM nhưng vẫn đang ở trạng thái ẩn (`style="display: none"`), nên `.text` trả về chuỗi rỗng. |
| **TH2: Thêm lệnh chờ tường minh (`WebDriverWait`)** | Dùng `WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "finish")))` | **PASSED 100%** (Lấy đúng chữ `"Hello World!"` ngay khi loading xong) | Selenium tự động chờ cho đến khi thanh tiến trình biến mất và thẻ `#finish` chuyển sang trạng thái hiển thị mới đọc `.text`, giúp bài test ổn định tuyệt đối. |

---

## 3. Ghi chú cá nhân của từng thành viên trong nhóm (Đầy đủ 5 thành viên)

- **Phạm Khang (Trưởng nhóm):**
  - *Điều đã học:* Hiểu rõ cách kết hợp `EC.url_contains` và `driver.current_url` để kiểm tra luồng chuyển hướng trang (`/redirector` -> `/status_codes`) mà không bị lỗi kiểm tra quá sớm khi trình duyệt chưa kịp đổi URL.
- **Nguyễn Đức Duy:**
  - *Điều đã học:* Nắm vững cơ chế hoạt động của `EC.staleness_of(element)`. Khi làm mới trang (`driver.refresh()`) ở `/notification_message_rendered`, việc chờ phần tử `#flash` cũ bị gỡ khỏi DOM bằng `staleness_of` trước khi thao tác tiếp giúp tránh hoàn toàn lỗi `StaleElementReferenceException`.
- **Tùng Anh:**
  - *Điều đã học:* Biết cách sử dụng các hàm điều hướng lịch sử trình duyệt như `driver.back()` và `driver.refresh()` kết hợp với `WebDriverWait` để đồng bộ hóa trạng thái trang sau mỗi lần điều hướng.
- **Duy Anh Nguyễn:**
  - *Điều đã học:* Phân biệt được rõ ràng sự khác nhau giữa Implicit Wait (`implicitly_wait`) và Explicit Wait (`WebDriverWait`). Hiểu lý do tại sao không nên dùng `time.sleep` và không nên trộn lẫn hai cơ chế chờ trong cùng một bài test.
- **Phương Huy:**
  - *Điều đã học:* Học được cách thiết kế test case trường hợp sai (Negative Test) cho trang điều hướng mã trạng thái lỗi HTTP (`500`), đảm bảo bài kiểm thử kiểm chứng được cả kịch bản tích cực lẫn tiêu cực.

---

## 4. Nhật ký sử dụng AI trong Tuần 7

- **Đã hỏi AI điều gì:**
  1. Nguyên nhân gây lỗi `TimeoutException` khi gọi `driver.refresh()` trên trang `/notification_message_rendered` và cách kết hợp `EC.staleness_of`.
  2. Cách kiểm tra danh sách thông báo ngẫu nhiên trên trang `/notification_message_rendered` vì có lúc trang trả về `"Action successful"`, lúc lại trả về `"Action unsuccesful, please try again"`.
- **Câu trả lời của AI có đúng không:**
  - Đúng và rất sát thực tế. AI giải thích rõ sau khi `refresh()`, thanh `#flash` không tự sinh ra mà cần bấm lại `"Click here"`, đồng thời chỉ ra từ `"unsuccesful"` trên trang web mẫu bị thiếu một chữ `s`, giúp nhóm đưa vào danh sách kiểm tra hợp lệ.
- **Mình hiểu thêm được gì:**
  - Hiểu rằng `EC.staleness_of` nhận đối số là một đối tượng **WebElement** đã tìm thấy trước đó (khác với `visibility_of_element_located` nhận một tuple locator `(By.ID, ...)`). Khi phần tử cũ bị gỡ khỏi cây DOM sau lệnh `refresh()`, `staleness_of` trả về `True` ngay lập tức.