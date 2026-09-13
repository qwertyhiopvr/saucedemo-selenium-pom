from config import PASSWORD, USERS
from pages.cart_page import CartPage
from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage


def _login(driver):
    LoginPage(driver).open().login(USERS["standard"], PASSWORD)
    return InventoryPage(driver)


def test_cart_reflects_items_added_on_inventory_page(driver):
    inventory = _login(driver)
    inventory.add_item_to_cart_by_name("Sauce Labs Backpack")
    inventory.add_item_to_cart_by_name("Sauce Labs Bike Light")
    inventory.go_to_cart()

    cart = CartPage(driver)
    assert set(cart.get_cart_item_names()) == {"Sauce Labs Backpack", "Sauce Labs Bike Light"}


def test_remove_item_from_cart_page(driver):
    inventory = _login(driver)
    inventory.add_item_to_cart_by_name("Sauce Labs Backpack")
    inventory.add_item_to_cart_by_name("Sauce Labs Bike Light")
    inventory.go_to_cart()

    cart = CartPage(driver)
    cart.remove_item_by_name("Sauce Labs Backpack")

    assert cart.get_cart_item_names() == ["Sauce Labs Bike Light"]


def test_continue_shopping_returns_to_inventory_page(driver):
    inventory = _login(driver)
    inventory.add_item_to_cart_by_name("Sauce Labs Backpack")
    inventory.go_to_cart()

    CartPage(driver).click_continue_shopping()

    inventory.wait_for_url_contains("inventory.html")
    assert "inventory.html" in driver.current_url


def test_checkout_button_navigates_even_with_empty_cart(driver):
    inventory = _login(driver)
    inventory.go_to_cart()

    cart = CartPage(driver)
    assert cart.get_cart_item_names() == []

    cart.click_checkout()
    cart.wait_for_url_contains("checkout-step-one.html")
    assert "checkout-step-one.html" in driver.current_url
