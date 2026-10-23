import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By

URL_LOGIN = "https://the-internet.herokuapp.com/login"

@pytest.fixture
def driver():
    # Khoi tao trinh duyet Chrome mac dinh cua Selenium
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.implicitly_wait(10)
    yield driver
    # Dong trinh duyet sau khi kiem thu xong
    driver.quit()

def test_tc01_login_thanh_cong(driver):
    """TC01: Dang nhap thanh cong voi tai khoan dung"""
    driver.get(URL_LOGIN)
    driver.find_element(By.ID, "username").send_keys("tomsmith")
    driver.find_element(By.ID, "password").send_keys("SuperSecretPassword!")
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
    
    # Kiem tra chuyen huong sang trang secure va co thong bao thanh cong
    assert "/secure" in driver.current_url
    flash_text = driver.find_element(By.ID, "flash").text
    assert "You logged into a secure area!" in flash_text

def test_tc02_login_sai_username(driver):
    """TC02: Dang nhap that bai khi nhap sai Username"""
    driver.get(URL_LOGIN)
    driver.find_element(By.ID, "username").send_keys("sai_user")
    driver.find_element(By.ID, "password").send_keys("SuperSecretPassword!")
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
    
    flash_text = driver.find_element(By.ID, "flash").text
    assert "Your username is invalid!" in flash_text

def test_tc03_login_sai_password(driver):
    """TC03: Dang nhap that bai khi nhap sai Password"""
    driver.get(URL_LOGIN)
    driver.find_element(By.ID, "username").send_keys("tomsmith")
    driver.find_element(By.ID, "password").send_keys("sai_pass")
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
    
    flash_text = driver.find_element(By.ID, "flash").text
    assert "Your password is invalid!" in flash_text

def test_tc04_login_de_trong(driver):
    """TC04: Dang nhap that bai khi de trong ca 2 o"""
    driver.get(URL_LOGIN)
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
    
    flash_text = driver.find_element(By.ID, "flash").text
    assert "Your username is invalid!" in flash_text

def test_tc05_dang_xuat_thanh_cong(driver):
    """TC05: Dang xuat thanh cong sau khi da dang nhap"""
    driver.get(URL_LOGIN)
    driver.find_element(By.ID, "username").send_keys("tomsmith")
    driver.find_element(By.ID, "password").send_keys("SuperSecretPassword!")
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
    
    # Bam nut Logout tai trang /secure
    driver.find_element(By.CSS_SELECTOR, "a.button.secondary.radius").click()
    
    # Kiem tra quay lai trang /login va co thong bao dang xuat
    assert "/login" in driver.current_url
    flash_text = driver.find_element(By.ID, "flash").text
    assert "You logged out of the secure area!" in flash_text