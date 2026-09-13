import pytest

from config import PASSWORD, USERS
from pages.login_page import LoginPage


@pytest.mark.parametrize("username", [USERS["standard"], USERS["problem"], USERS["performance_glitch"]])
def test_successful_login(driver, username):
    page = LoginPage(driver).open()
    page.login(username, PASSWORD)

    page.wait_for_url_contains("inventory.html")
    assert "inventory.html" in driver.current_url


def test_locked_out_user_cannot_login(driver):
    page = LoginPage(driver).open()
    page.login(USERS["locked_out"], PASSWORD)

    assert page.get_error_message() == "Epic sadface: Sorry, this user has been locked out."
    assert "inventory.html" not in driver.current_url


def test_login_with_wrong_password_shows_error(driver):
    page = LoginPage(driver).open()
    page.login(USERS["standard"], "wrong_password")

    assert page.get_error_message() == (
        "Epic sadface: Username and password do not match any user in this service"
    )


def test_login_with_empty_username_shows_error(driver):
    page = LoginPage(driver).open()
    page.login("", PASSWORD)

    assert page.get_error_message() == "Epic sadface: Username is required"


def test_login_with_empty_password_shows_error(driver):
    page = LoginPage(driver).open()
    page.login(USERS["standard"], "")

    assert page.get_error_message() == "Epic sadface: Password is required"
