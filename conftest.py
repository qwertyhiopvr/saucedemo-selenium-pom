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
    options.set_capability("goog:loggingPrefs", {"browser": "ALL"})

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

            # Printed straight to the CI log (no artifact download needed) to
            # debug the CI-only flakiness in cart/checkout navigation.
            print(f"\n--- FAILURE DEBUG for {item.name} ---")
            print(f"current_url: {driver.current_url}")
            print(f"title: {driver.title}")
            try:
                body_text = driver.execute_script(
                    "return document.body ? document.body.innerText.slice(0, 800) : null"
                )
                print(f"body innerText (first 800 chars): {body_text!r}")
            except Exception as exc:
                print(f"could not read body innerText: {exc}")
            try:
                for entry in driver.get_log("browser"):
                    print(f"console: {entry}")
            except Exception as exc:
                print(f"could not read browser console log: {exc}")
            print("--- END FAILURE DEBUG ---\n")
