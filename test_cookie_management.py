import os

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


BASE_URL = "https://the-internet.herokuapp.com/login"


@pytest.fixture
def driver():
    options = Options()
    options.add_argument("--window-size=1280,900")
    if os.getenv("HEADLESS", "0") == "1":
        options.add_argument("--headless=new")

    remote_url = os.getenv("SELENIUM_REMOTE_URL")
    browser = (
        webdriver.Remote(command_executor=remote_url, options=options)
        if remote_url
        else webdriver.Chrome(options=options)
    )
    browser.get(BASE_URL)
    yield browser
    browser.quit()


def test_them_va_lay_cookie_theo_ten(driver):
    driver.add_cookie({"name": "t8_test", "value": "cookie_demo", "path": "/"})

    cookie = driver.get_cookie("t8_test")

    assert cookie is not None
    assert cookie["value"] == "cookie_demo"


def test_xoa_mot_cookie(driver):
    driver.add_cookie({"name": "t8_delete", "value": "temporary", "path": "/"})
    assert driver.get_cookie("t8_delete") is not None

    driver.delete_cookie("t8_delete")

    assert driver.get_cookie("t8_delete") is None


def test_xoa_tat_ca_cookie(driver):
    driver.add_cookie({"name": "t8_a", "value": "1", "path": "/"})
    driver.add_cookie({"name": "t8_b", "value": "2", "path": "/"})

    driver.delete_all_cookies()

    assert driver.get_cookies() == []
