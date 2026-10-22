"""Navigation and session tests (TC_MENU_*)."""
from pages import BASE_URL


def test_logout_returns_to_login_page(inventory):
    login_page = inventory.logout()
    assert login_page.driver.current_url == BASE_URL
    assert login_page.driver.find_element(*login_page.LOGIN_BTN).is_displayed()


def test_inventory_page_requires_login(driver):
    driver.get(BASE_URL + "inventory.html")
    error = driver.find_element("css selector", "h3[data-test='error']").text
    assert "You can only access '/inventory.html' when you are logged in" in error
