from config import PASSWORD, USERS
from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage


def _login(driver, username=USERS["standard"]):
    LoginPage(driver).open().login(username, PASSWORD)
    return InventoryPage(driver)


def test_inventory_page_lists_six_products(driver):
    page = _login(driver)
    assert len(page.get_product_names()) == 6


def test_add_single_item_updates_cart_badge(driver):
    page = _login(driver)
    page.add_item_to_cart_by_name("Sauce Labs Backpack")

    assert page.get_cart_badge_count() == 1


def test_add_multiple_items_updates_cart_badge_count(driver):
    page = _login(driver)
    page.add_item_to_cart_by_name("Sauce Labs Backpack")
    page.add_item_to_cart_by_name("Sauce Labs Bike Light")

    assert page.get_cart_badge_count() == 2


def test_remove_item_from_inventory_page_clears_badge(driver):
    page = _login(driver)
    page.add_item_to_cart_by_name("Sauce Labs Backpack")
    page.remove_item_by_name("Sauce Labs Backpack")

    assert page.get_cart_badge_count() == 0


def test_cart_badge_hidden_when_cart_is_empty(driver):
    page = _login(driver)
    assert page.get_cart_badge_count() == 0


def test_sort_by_price_low_to_high(driver):
    page = _login(driver)
    page.sort_by("lohi")

    prices = page.get_product_prices()
    assert prices == sorted(prices)


def test_sort_by_price_high_to_low(driver):
    page = _login(driver)
    page.sort_by("hilo")

    prices = page.get_product_prices()
    assert prices == sorted(prices, reverse=True)


def test_sort_by_name_z_to_a(driver):
    page = _login(driver)
    page.sort_by("za")

    names = page.get_product_names()
    assert names == sorted(names, reverse=True)


def test_problem_user_shows_identical_product_images(driver):
    """Known quirk of problem_user: product images are swapped/identical.

    Written as a regression guard, not a bug report — if this ever starts
    failing, someone fixed the seed data and the test should be removed.
    """
    page = _login(driver, USERS["problem"])
    image_srcs = page.get_product_image_srcs()

    assert len(set(image_srcs)) == 1
