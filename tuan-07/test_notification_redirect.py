import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@pytest.fixture
def driver():
    """Khởi tạo trình duyệt Chrome cho mỗi bài kiểm thử và đóng lại sau khi chạy xong."""
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(options=options)
    yield driver
    driver.quit()


def test_tc01_notification_message_and_refresh(driver):
    """
    TC01 (Positive): Kiểm tra thông báo ngẫu nhiên tại /notification_message_rendered.
    Sử dụng: WebDriverWait, EC.visibility_of_element_located, EC.staleness_of, refresh.
    """
    driver.get("https://the-internet.herokuapp.com/notification_message_rendered")
    wait = WebDriverWait(driver, 15)

    # 1. Chờ và bấm nút 'Click here' lần đầu để sinh thông báo
    click_here_link = wait.until(
        EC.visibility_of_element_located((By.LINK_TEXT, "Click here"))
    )
    click_here_link.click()

    # 2. Chờ phần tử thông báo (#flash) hiển thị trên giao diện
    flash_element = wait.until(
        EC.visibility_of_element_located((By.ID, "flash"))
    )
    first_message = flash_element.text.strip()

    # 3. Thực hiện làm mới trang (refresh) -> phần tử flash_element cũ sẽ bị gỡ khỏi DOM
    driver.refresh()
    wait.until(EC.staleness_of(flash_element))

    # 4. Sau khi refresh, chờ nút 'Click here' xuất hiện lại và bấm để lấy thông báo mới
    new_click_here = wait.until(
        EC.visibility_of_element_located((By.LINK_TEXT, "Click here"))
    )
    new_click_here.click()

    # 5. Chờ thông báo mới (#flash) hiển thị và kiểm tra nội dung
    new_flash_element = wait.until(
        EC.visibility_of_element_located((By.ID, "flash"))
    )
    second_message = new_flash_element.text.strip()

    # Danh sách các thông báo hợp lệ mà trang web trả về ngẫu nhiên
    valid_messages = [
        "Action successful",
        "Action unsuccesful, please try again",
        "Action unsuccessful"
    ]
    assert any(msg in first_message for msg in valid_messages), "Thông báo lần 1 không hợp lệ!"
    assert any(msg in second_message for msg in valid_messages), "Thông báo lần 2 không hợp lệ!"
    assert new_flash_element.is_displayed()


def test_tc02_redirector_and_browser_history_back(driver):
    """
    TC02 (Positive): Kiểm tra chuyển hướng từ /redirector sang /status_codes và quay lại.
    Sử dụng: WebDriverWait, EC.visibility_of_element_located, EC.url_contains, current_url, back.
    """
    driver.get("https://the-internet.herokuapp.com/redirector")
    wait = WebDriverWait(driver, 15)

    # Kiểm tra URL ban đầu
    assert "/redirector" in driver.current_url

    # 1. Chờ nút chuyển hướng (#redirect) hiển thị và bấm vào
    redirect_link = wait.until(
        EC.visibility_of_element_located((By.ID, "redirect"))
    )
    redirect_link.click()

    # 2. Chờ URL chuyển hướng thành công sang '/status_codes'
    wait.until(EC.url_contains("/status_codes"))
    assert "https://the-internet.herokuapp.com/status_codes" in driver.current_url

    # 3. Sử dụng hàm back() để quay trở lại trang trước đó
    driver.back()
    wait.until(EC.url_contains("/redirector"))
    assert driver.current_url.endswith("/redirector")


def test_tc03_negative_redirect_to_500_server_error(driver):
    """
    TC03 (Negative - Trường hợp sai): Kiểm tra điều hướng vào trang mã lỗi máy chủ 500
    và xác nhận hệ thống báo lỗi 500 chứ KHÔNG trả về trạng thái thành công 200.
    """
    driver.get("https://the-internet.herokuapp.com/redirector")
    wait = WebDriverWait(driver, 15)

    # 1. Bấm link chuyển hướng sang trang danh sách Status Codes
    wait.until(EC.visibility_of_element_located((By.ID, "redirect"))).click()
    wait.until(EC.url_contains("/status_codes"))

    # 2. Bấm vào mã lỗi 500 (Internal Server Error)
    link_500 = wait.until(
        EC.visibility_of_element_located((By.LINK_TEXT, "500"))
    )
    link_500.click()

    # 3. Chờ URL cập nhật sang '/status_codes/500'
    wait.until(EC.url_contains("/status_codes/500"))
    assert "/status_codes/500" in driver.current_url

    # 4. Chờ nội dung thông báo lỗi hiển thị và kiểm tra trường hợp phủ định (Negative check)
    content_element = wait.until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "div.example p"))
    )
    page_text = content_element.text

    assert "This page returned a 500 status code" in page_text
    assert "200 status code" not in page_text, "Lỗi: Trang lỗi 500 nhưng lại báo mã thành công 200!"