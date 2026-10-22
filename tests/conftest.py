"""
pytest configuration: creates the Selenium WebDriver for every test and
saves a screenshot when a test fails.
"""
import os

import pytest
from selenium import webdriver

from pages import LoginPage

SCREENSHOT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "reports", "screenshots")


def pytest_addoption(parser):
    parser.addoption("--browser", default="edge", help="edge or chrome")
    parser.addoption("--headed", action="store_true", help="show the browser window")


@pytest.fixture
def driver(request):
    """One fresh browser per test, closed afterwards."""
    name = request.config.getoption("--browser").lower()
    if name == "chrome":
        options = webdriver.ChromeOptions()
    else:
        options = webdriver.EdgeOptions()
    if not request.config.getoption("--headed"):
        options.add_argument("--headless=new")
    options.add_argument("--window-size=1280,900")
    drv = webdriver.Chrome(options=options) if name == "chrome" else webdriver.Edge(options=options)
    drv.implicitly_wait(5)
    yield drv
    drv.quit()


@pytest.fixture
def login_page(driver):
    return LoginPage(driver).open()


@pytest.fixture
def inventory(login_page):
    """Logged-in standard user on the Products page."""
    return login_page.login("standard_user")


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """After each test phase, save a screenshot if the test failed."""
    outcome = yield
    report = outcome.get_result()
    if report.when == "call" and report.failed:
        drv = item.funcargs.get("driver")
        if drv is not None:
            os.makedirs(SCREENSHOT_DIR, exist_ok=True)
            path = os.path.join(SCREENSHOT_DIR, f"{item.name}.png")
            drv.save_screenshot(path)
            # show the image inside the pytest-html report
            extras = getattr(report, "extras", [])
            try:
                from pytest_html import extras as html_extras
                extras.append(html_extras.image(path))
            except ImportError:
                pass
            report.extras = extras
