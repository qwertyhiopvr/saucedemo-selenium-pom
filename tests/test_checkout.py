import pytest

from config import PASSWORD, USERS
from pages.checkout_page import CheckoutCompletePage, CheckoutStepOnePage, CheckoutStepTwoPage
from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage


def _reach_checkout_step_one(driver, item_names=("Sauce Labs Backpack",)):
    LoginPage(driver).open().login(USERS["standard"], PASSWORD)
    inventory = InventoryPage(driver)
    for name in item_names:
        inventory.add_item_to_cart_by_name(name)
    inventory.go_to_cart()
    from pages.cart_page import CartPage

    CartPage(driver).click_checkout()
    return CheckoutStepOnePage(driver)


def test_complete_checkout_happy_path(driver):
    step_one = _reach_checkout_step_one(driver, ["Sauce Labs Backpack", "Sauce Labs Bike Light"])
    step_one.fill_info("Azim", "Hasanov", "735700")
    step_one.click_continue()

    step_two = CheckoutStepTwoPage(driver)
    step_two.wait_for_url_contains("checkout-step-two.html")

    item_total = step_two.get_item_total()
    tax = step_two.get_tax()
    total = step_two.get_total()
    assert round(item_total + tax, 2) == round(total, 2)

    step_two.click_finish()

    complete = CheckoutCompletePage(driver)
    complete.wait_for_url_contains("checkout-complete.html")
    assert complete.get_complete_header() == "Thank you for your order!"


@pytest.mark.parametrize(
    "first_name, last_name, postal_code, expected_error",
    [
        ("", "Hasanov", "735700", "Error: First Name is required"),
        ("Azim", "", "735700", "Error: Last Name is required"),
        ("Azim", "Hasanov", "", "Error: Postal Code is required"),
    ],
)
def test_checkout_step_one_requires_all_fields(
    driver, first_name, last_name, postal_code, expected_error
):
    step_one = _reach_checkout_step_one(driver)
    step_one.fill_info(first_name, last_name, postal_code)
    step_one.click_continue()

    assert step_one.get_error_message() == expected_error
