import re

from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class CheckoutStepOnePage(BasePage):
    FIRST_NAME_INPUT = (By.CSS_SELECTOR, "[data-test='firstName']")
    LAST_NAME_INPUT = (By.CSS_SELECTOR, "[data-test='lastName']")
    POSTAL_CODE_INPUT = (By.CSS_SELECTOR, "[data-test='postalCode']")
    CONTINUE_BUTTON = (By.CSS_SELECTOR, "[data-test='continue']")
    CANCEL_BUTTON = (By.CSS_SELECTOR, "[data-test='cancel']")
    ERROR_MESSAGE = (By.CSS_SELECTOR, "[data-test='error']")

    def fill_info(self, first_name="", last_name="", postal_code=""):
        self.type(self.FIRST_NAME_INPUT, first_name)
        self.type(self.LAST_NAME_INPUT, last_name)
        self.type(self.POSTAL_CODE_INPUT, postal_code)
        return self

    def click_continue(self):
        self.click(self.CONTINUE_BUTTON)
        return self

    def click_cancel(self):
        self.click(self.CANCEL_BUTTON)
        return self

    def get_error_message(self):
        return self.get_text(self.ERROR_MESSAGE)


class CheckoutStepTwoPage(BasePage):
    ITEM_TOTAL = (By.CSS_SELECTOR, "[data-test='subtotal-label']")
    TAX = (By.CSS_SELECTOR, "[data-test='tax-label']")
    TOTAL = (By.CSS_SELECTOR, "[data-test='total-label']")
    FINISH_BUTTON = (By.CSS_SELECTOR, "[data-test='finish']")
    CANCEL_BUTTON = (By.CSS_SELECTOR, "[data-test='cancel']")

    @staticmethod
    def _extract_amount(text):
        return float(re.search(r"[\d.]+", text).group())

    def get_item_total(self):
        return self._extract_amount(self.get_text(self.ITEM_TOTAL))

    def get_tax(self):
        return self._extract_amount(self.get_text(self.TAX))

    def get_total(self):
        return self._extract_amount(self.get_text(self.TOTAL))

    def click_finish(self):
        self.click(self.FINISH_BUTTON)
        return self


class CheckoutCompletePage(BasePage):
    COMPLETE_HEADER = (By.CSS_SELECTOR, "[data-test='complete-header']")
    BACK_HOME_BUTTON = (By.CSS_SELECTOR, "[data-test='back-to-products']")

    def get_complete_header(self):
        return self.get_text(self.COMPLETE_HEADER)
