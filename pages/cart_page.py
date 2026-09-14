from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from pages.base_page import BasePage
from pages.inventory_page import _slugify


class CartPage(BasePage):
    CART_ITEM_NAME = (By.CSS_SELECTOR, ".cart_item .inventory_item_name")
    CHECKOUT_BUTTON = (By.CSS_SELECTOR, "[data-test='checkout']")
    CONTINUE_SHOPPING_BUTTON = (By.CSS_SELECTOR, "[data-test='continue-shopping']")

    def get_cart_item_names(self):
        return [el.text for el in self.find_all_or_empty(self.CART_ITEM_NAME)]

    def remove_item_by_name(self, product_name):
        locator = (By.CSS_SELECTOR, f"[data-test='remove-{_slugify(product_name)}']")
        self.click(locator)
        # The row (including this button) unmounts once React commits the
        # state update -- wait for that instead of reading the list
        # immediately, which can otherwise race the re-render.
        self.wait.until(EC.invisibility_of_element_located(locator))
        return self

    def click_checkout(self):
        self.click(self.CHECKOUT_BUTTON)
        self.wait_for_url_contains("checkout-step-one.html")
        return self

    def click_continue_shopping(self):
        self.click(self.CONTINUE_SHOPPING_BUTTON)
        self.wait_for_url_contains("inventory.html")
        return self
