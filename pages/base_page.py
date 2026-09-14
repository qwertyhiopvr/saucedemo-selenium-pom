from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from config import DEFAULT_TIMEOUT

STALE_RETRY_ATTEMPTS = 3


class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, DEFAULT_TIMEOUT)

    def open(self, url):
        self.driver.get(url)

    def find(self, locator):
        return self.wait.until(EC.presence_of_element_located(locator))

    def find_all(self, locator):
        return self.wait.until(EC.presence_of_all_elements_located(locator))

    def find_all_or_empty(self, locator):
        """Like find_all, but a legitimately empty result isn't a timeout."""
        return self.driver.find_elements(*locator)

    def click(self, locator):
        """Waits for clickability, then clicks via JS rather than native
        mouse-coordinate hit-testing. Native .click() proved unreliable in
        headless CI against this React app -- element_to_be_clickable would
        pass, .click() wouldn't raise, yet the app's onClick handler
        sometimes never fired (no navigation, no state change). Dispatching
        the click via the DOM sidesteps coordinate/viewport hit-testing
        entirely. Retries on staleness for the same reason as before: the
        element can go stale between being located and being clicked."""
        for attempt in range(STALE_RETRY_ATTEMPTS):
            try:
                element = self.wait.until(EC.element_to_be_clickable(locator))
                self.driver.execute_script("arguments[0].click();", element)
                return
            except StaleElementReferenceException:
                if attempt == STALE_RETRY_ATTEMPTS - 1:
                    raise

    def type(self, locator, text):
        el = self.find(locator)
        el.clear()
        el.send_keys(text)

    def get_text(self, locator):
        return self.find(locator).text

    def is_visible(self, locator):
        try:
            return self.wait.until(EC.visibility_of_element_located(locator)).is_displayed()
        except Exception:
            return False

    def wait_for_url_contains(self, fragment):
        self.wait.until(EC.url_contains(fragment))
