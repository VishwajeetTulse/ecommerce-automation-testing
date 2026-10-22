"""
Small Page Object classes for the Swag Labs demo store.

Each class wraps one page: it knows the locators of that page and offers a
few actions. Tests use these methods instead of raw locators, so if the
site changes only this file has to be updated.
"""
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait

BASE_URL = "https://www.saucedemo.com/"
DEFAULT_PASSWORD = "secret_sauce"


class LoginPage:
    USERNAME_INPUT = (By.ID, "user-name")
    PASSWORD_INPUT = (By.ID, "password")
    LOGIN_BTN = (By.ID, "login-button")
    ERROR = (By.CSS_SELECTOR, "h3[data-test='error']")

    def __init__(self, driver):
        self.driver = driver

    def open(self):
        self.driver.get(BASE_URL)
        return self

    def login(self, username, password=DEFAULT_PASSWORD):
        self.driver.find_element(*self.USERNAME_INPUT).clear()
        self.driver.find_element(*self.USERNAME_INPUT).send_keys(username)
        self.driver.find_element(*self.PASSWORD_INPUT).clear()
        self.driver.find_element(*self.PASSWORD_INPUT).send_keys(password)
        self.driver.find_element(*self.LOGIN_BTN).click()
        # wait until either the Products page opens or an error is shown
        WebDriverWait(self.driver, 10).until(
            lambda d: "inventory.html" in d.current_url or d.find_elements(*self.ERROR))
        return InventoryPage(self.driver)

    def error_message(self):
        return self.driver.find_element(*self.ERROR).text


class InventoryPage:
    ITEMS = (By.CLASS_NAME, "inventory_item")
    NAMES = (By.CLASS_NAME, "inventory_item_name")
    PRICES = (By.CLASS_NAME, "inventory_item_price")
    SORT = (By.CLASS_NAME, "product_sort_container")
    BADGE = (By.CLASS_NAME, "shopping_cart_badge")
    CART_LINK = (By.CLASS_NAME, "shopping_cart_link")
    MENU_BTN = (By.ID, "react-burger-menu-btn")
    LOGOUT = (By.ID, "logout_sidebar_link")

    def __init__(self, driver):
        self.driver = driver

    def is_loaded(self):
        return "inventory.html" in self.driver.current_url

    def product_names(self):
        return [e.text for e in self.driver.find_elements(*self.NAMES)]

    def product_prices(self):
        return [float(e.text.strip("$")) for e in self.driver.find_elements(*self.PRICES)]

    def sort_by(self, value):  # az, za, lohi, hilo
        Select(self.driver.find_element(*self.SORT)).select_by_value(value)

    def add_to_cart(self, slug):
        self.driver.find_element(By.ID, f"add-to-cart-{slug}").click()

    def remove_from_cart(self, slug):
        self.driver.find_element(By.ID, f"remove-{slug}").click()

    def cart_count(self):
        badge = self.driver.find_elements(*self.BADGE)
        return int(badge[0].text) if badge else 0

    def go_to_cart(self):
        self.driver.find_element(*self.CART_LINK).click()
        return CartPage(self.driver)

    def logout(self):
        self.driver.find_element(*self.MENU_BTN).click()
        self.driver.find_element(*self.LOGOUT).click()
        return LoginPage(self.driver)


class CartPage:
    ITEM_NAMES = (By.CLASS_NAME, "inventory_item_name")
    CHECKOUT = (By.ID, "checkout")

    def __init__(self, driver):
        self.driver = driver

    def item_names(self):
        return [e.text for e in self.driver.find_elements(*self.ITEM_NAMES)]

    def remove(self, slug):
        self.driver.find_element(By.ID, f"remove-{slug}").click()

    def checkout(self):
        self.driver.find_element(*self.CHECKOUT).click()
        return CheckoutPage(self.driver)


class CheckoutPage:
    FIRST = (By.ID, "first-name")
    LAST = (By.ID, "last-name")
    POSTAL = (By.ID, "postal-code")
    CONTINUE = (By.ID, "continue")
    FINISH = (By.ID, "finish")
    ERROR = (By.CSS_SELECTOR, "h3[data-test='error']")
    SUBTOTAL = (By.CLASS_NAME, "summary_subtotal_label")
    TAX = (By.CLASS_NAME, "summary_tax_label")
    TOTAL = (By.CLASS_NAME, "summary_total_label")
    COMPLETE = (By.CLASS_NAME, "complete-header")

    def __init__(self, driver):
        self.driver = driver

    def fill_information(self, first, last, postal):
        self.driver.find_element(*self.FIRST).send_keys(first)
        self.driver.find_element(*self.LAST).send_keys(last)
        self.driver.find_element(*self.POSTAL).send_keys(postal)
        self.driver.find_element(*self.CONTINUE).click()

    def error_message(self):
        return self.driver.find_element(*self.ERROR).text

    def _amount(self, locator):
        return float(self.driver.find_element(*locator).text.split("$")[1])

    def subtotal(self):
        return self._amount(self.SUBTOTAL)

    def tax(self):
        return self._amount(self.TAX)

    def total(self):
        return self._amount(self.TOTAL)

    def finish(self):
        self.driver.find_element(*self.FINISH).click()

    def completion_message(self):
        return self.driver.find_element(*self.COMPLETE).text
