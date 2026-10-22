"""Login module tests (TC_LOGIN_*)."""
import pytest


def test_valid_login(login_page):
    inventory = login_page.login("standard_user")
    assert inventory.is_loaded()


@pytest.mark.parametrize("username,password,expected", [
    ("", "", "Username is required"),
    ("standard_user", "", "Password is required"),
    ("standard_user", "wrong", "do not match any user"),
    ("locked_out_user", "secret_sauce", "locked out"),
])
def test_invalid_login_shows_error(login_page, username, password, expected):
    login_page.login(username, password)
    assert expected in login_page.error_message()


def test_password_is_masked(login_page):
    field = login_page.driver.find_element(*login_page.PASSWORD_INPUT)
    assert field.get_attribute("type") == "password"
