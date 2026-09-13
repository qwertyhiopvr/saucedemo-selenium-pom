import os

import pytest
from pytest_html import extras
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


@pytest.fixture
def driver():
    options = Options()
    if os.getenv("HEADLESS", "1") == "1":
        options.add_argument("--headless=new")
    options.add_argument("--window-size=1400,1000")

    drv = webdriver.Chrome(options=options)
    yield drv
    drv.quit()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    report.extras = getattr(report, "extras", [])

    if report.when == "call" and report.failed:
        driver = item.funcargs.get("driver")
        if driver is not None:
            screenshot = driver.get_screenshot_as_base64()
            report.extras.append(extras.image(screenshot, mime_type="image/png"))
