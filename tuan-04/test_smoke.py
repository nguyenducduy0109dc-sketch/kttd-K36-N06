from selenium import webdriver

def test_smoke_the_internet_title():
    # Bước 1: Khởi tạo trình duyệt Google Chrome
    driver = webdriver.Chrome()
    
    # Bước 2: Mở trang web thực hành the-internet
    driver.get("https://the-internet.herokuapp.com/")
    
    # Bước 3: Kiểm tra tiêu đề trang web có đúng là 'The Internet' hay không
    assert driver.title == "The Internet"
    
    # Bước 4: Giải phóng tài nguyên và đóng trình duyệt
    driver.quit()