"""Products page tests (TC_PROD_*)."""
import pytest


def test_six_products_listed(inventory):
    assert len(inventory.product_names()) == 6


def test_sort_price_low_to_high(inventory):
    inventory.sort_by("lohi")
    prices = inventory.product_prices()
    assert prices == sorted(prices)


def test_sort_price_high_to_low(inventory):
    inventory.sort_by("hilo")
    prices = inventory.product_prices()
    assert prices == sorted(prices, reverse=True)


def test_sort_name_z_to_a(inventory):
    inventory.sort_by("za")
    names = inventory.product_names()
    assert names == sorted(names, reverse=True)


@pytest.mark.xfail(reason="Known defect DEF-02: sorting is broken for problem_user", strict=True)
def test_sort_price_problem_user(login_page):
    inventory = login_page.login("problem_user")
    inventory.sort_by("lohi")
    prices = inventory.product_prices()
    assert prices == sorted(prices)
