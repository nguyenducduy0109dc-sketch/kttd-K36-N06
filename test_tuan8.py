"""Tuần 8 – Kiểm thử Cookies, đăng nhập và lịch sử trình duyệt.
Chạy: python -m pytest -v -s test_tuan8.py
Tuỳ chọn Selenium Grid: đặt biến SELENIUM_REMOTE_URL.
"""
import os
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

BASE = "https://the-internet.herokuapp.com"
USERNAME = "tomsmith"
PASSWORD = "SuperSecretPassword!"
TIMEOUT = 15


@pytest.fixture
def driver():
    options = Options()
    options.add_argument("--window-size=1280,900")
    if os.getenv("HEADLESS", "0") == "1":
        options.add_argument("--headless=new")
    remote_url = os.getenv("SELENIUM_REMOTE_URL")
    browser = (webdriver.Remote(command_executor=remote_url, options=options)
               if remote_url else webdriver.Chrome(options=options))
    browser.implicitly_wait(2)
    yield browser
    browser.quit()


def login(driver):
    driver.get(f"{BASE}/login")
    driver.find_element(By.ID, "username").send_keys(USERNAME)
    driver.find_element(By.ID, "password").send_keys(PASSWORD)
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
    WebDriverWait(driver, TIMEOUT).until(EC.url_contains("/secure"))
    assert "You logged into a secure area!" in driver.find_element(By.ID, "flash").text


def test_tc01_login_thanh_cong(driver):
    login(driver)
    assert driver.current_url.endswith("/secure")


def test_tc02_lay_danh_sach_cookie(driver):
    login(driver)
    cookies = driver.get_cookies()
    print("Danh sách tên cookie sau login:", [c["name"] for c in cookies])
    assert isinstance(cookies, list)
    # Ứng dụng demo có thể thay đổi tên hoặc cách tạo cookie.
    # Không kiểm tra cố định tên cookie phiên.


def test_tc03_get_cookie_theo_ten(driver):
    driver.get(f"{BASE}/login")
    driver.add_cookie({"name": "t8_test", "value": "cookie_demo", "path": "/"})
    cookie = driver.get_cookie("t8_test")
    assert cookie is not None
    assert cookie["value"] == "cookie_demo"


def test_tc04_them_cookie(driver):
    driver.get(f"{BASE}/login")  # Phải vào domain trước khi thêm cookie
    driver.add_cookie({"name": "t8_added", "value": "selenium_week8", "path": "/"})
    assert driver.get_cookie("t8_added")["value"] == "selenium_week8"


def test_tc05_xoa_mot_cookie(driver):
    driver.get(f"{BASE}/login")
    driver.add_cookie({"name": "t8_delete", "value": "temp", "path": "/"})
    assert driver.get_cookie("t8_delete") is not None
    driver.delete_cookie("t8_delete")
    assert driver.get_cookie("t8_delete") is None


def test_tc06_xoa_tat_ca_cookie(driver):
    driver.get(f"{BASE}/login")
    driver.add_cookie({"name": "t8_a", "value": "1", "path": "/"})
    driver.add_cookie({"name": "t8_b", "value": "2", "path": "/"})
    driver.delete_all_cookies()
    assert driver.get_cookies() == []


def test_tc07_refresh_giu_phien_dang_nhap(driver):
    login(driver)
    driver.refresh()
    WebDriverWait(driver, TIMEOUT).until(EC.url_contains("/secure"))
    assert driver.find_element(By.CSS_SELECTOR, "a.button.secondary.radius").text.strip() == "Logout"


def test_tc08_back_forward_va_current_url(driver):
    driver.get(f"{BASE}/login")
    assert driver.current_url.endswith("/login")
    driver.get(f"{BASE}/status_codes")
    assert driver.current_url.endswith("/status_codes")
    driver.back()
    WebDriverWait(driver, TIMEOUT).until(EC.url_contains("/login"))
    assert driver.current_url.endswith("/login")
    driver.forward()
    WebDriverWait(driver, TIMEOUT).until(EC.url_contains("/status_codes"))
    assert driver.current_url.endswith("/status_codes")


def test_tc09_by_link_text(driver):
    driver.get(f"{BASE}/status_codes")
    driver.find_element(By.LINK_TEXT, "200").click()
    WebDriverWait(driver, TIMEOUT).until(EC.url_contains("/status_codes/200"))
    assert driver.current_url.endswith("/status_codes/200")
    assert "200" in driver.find_element(By.TAG_NAME, "body").text


def test_tc10_remote_webdriver_tuong_thich(driver):
    # Chạy cùng một bộ test ở local hoặc Selenium Grid qua SELENIUM_REMOTE_URL.
    driver.get(f"{BASE}/login")
    assert driver.title == "The Internet"
    assert driver.session_id
    print("WebDriver session:", driver.session_id)
    print("Chế độ:", "Remote" if os.getenv("SELENIUM_REMOTE_URL") else "Local")
