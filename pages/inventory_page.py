from selenium.webdriver.common.by import By

from pages.base_page import BasePage


def _slugify(product_name):
    return product_name.lower().replace(" ", "-").replace(".", "")


class InventoryPage(BasePage):
    INVENTORY_ITEM = (By.CSS_SELECTOR, ".inventory_item")
    ITEM_NAME = (By.CSS_SELECTOR, ".inventory_item_name")
    ITEM_PRICE = (By.CSS_SELECTOR, ".inventory_item_price")
    ITEM_IMAGE = (By.CSS_SELECTOR, ".inventory_item_img img")
    SORT_SELECT = (By.CSS_SELECTOR, "[data-test='product-sort-container']")
    CART_LINK = (By.CSS_SELECTOR, ".shopping_cart_link")
    CART_BADGE = (By.CSS_SELECTOR, ".shopping_cart_badge")

    def get_product_names(self):
        return [el.text for el in self.find_all(self.ITEM_NAME)]

    def get_product_prices(self):
        return [float(el.text.replace("$", "")) for el in self.find_all(self.ITEM_PRICE)]

    def get_product_image_srcs(self):
        return [el.get_attribute("src") for el in self.find_all(self.ITEM_IMAGE)]

    def add_item_to_cart_by_name(self, product_name):
        locator = (By.CSS_SELECTOR, f"[data-test='add-to-cart-{_slugify(product_name)}']")
        self.click(locator)
        return self

    def remove_item_by_name(self, product_name):
        locator = (By.CSS_SELECTOR, f"[data-test='remove-{_slugify(product_name)}']")
        self.click(locator)
        return self

    def get_cart_badge_count(self):
        if not self.is_visible(self.CART_BADGE):
            return 0
        return int(self.get_text(self.CART_BADGE))

    def go_to_cart(self):
        self.click(self.CART_LINK)
        self.wait_for_url_contains("cart.html")
        return self

    def sort_by(self, option_value):
        from selenium.webdriver.support.ui import Select

        select = Select(self.find(self.SORT_SELECT))
        select.select_by_value(option_value)
        return self
