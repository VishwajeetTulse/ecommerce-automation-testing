# Automated Testing of an E-Commerce Website Using Selenium WebDriver

Mini project for **Software Testing and Quality Assurance (Automation Testing)**,
Laboratory Practice IV, BE Computer Engineering, Savitribai Phule Pune University.

**Application under test:** Swag Labs demo store, https://www.saucedemo.com

The stable, passing test cases from the companion manual-testing project were
converted into an automated regression suite using **Python, Selenium WebDriver
and pytest**, with a simple **Page Object Model** and an HTML report.

## Test suite

| File | Tests | What is checked |
|---|---|---|
| `tests/test_login.py` | 6 | valid login, 4 invalid logins (empty, no password, wrong password, locked-out user), password masking |
| `tests/test_products.py` | 5 | six products listed, sort by price low/high, sort by name Z-A, known sorting defect of problem_user (expected failure) |
| `tests/test_cart.py` | 4 | cart badge, cart contents, remove from cart page, remove from products page |
| `tests/test_checkout.py` | 5 | 3 missing-field validations, overview totals (8 % tax), complete order |
| `tests/test_navigation.py` | 2 | logout, protected page requires login |

Total: 22 test functions (parametrised), one marked `xfail` for a known defect.

## How to run

```bash
pip install -r requirements.txt
python -m pytest                      # headless Microsoft Edge (default)
python -m pytest --browser chrome     # headless Chrome
python -m pytest --headed             # watch the browser
python -m pytest tests/test_login.py  # one module only
```

The HTML report is written to `reports/report.html`; a screenshot of every
failed test is saved in `reports/screenshots/` and embedded in the report.

## Project structure

```
tests/pages.py            Page Objects: LoginPage, InventoryPage, CartPage, CheckoutPage
tests/conftest.py         WebDriver fixture, login fixtures, screenshot-on-failure hook
tests/test_*.py           the test cases
pytest.ini                default options (verbose, HTML report)
reports/                  report.html, console_output.txt, screenshots of failures
report/                   LaTeX project report (SPPU BE format)
```

## How it works (in one paragraph)

`conftest.py` starts a fresh headless Edge browser for every test and closes it
afterwards. Each test asks a Page Object to perform user actions (type, click,
select) and then asserts on what the page shows (URL, text, prices, badge
count). pytest collects the results and pytest-html writes a single
self-contained HTML report. If an assertion fails, a hook captures a
screenshot so the failure can be analysed without re-running the test.
