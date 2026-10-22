"""Checkout tests (TC_CHK_*)."""
import pytest


@pytest.fixture
def checkout(inventory):
    """Standard user with Backpack ($29.99) and Bike Light ($9.99) in the cart,
    on the Checkout: Your Information page."""
    inventory.add_to_cart("sauce-labs-backpack")
    inventory.add_to_cart("sauce-labs-bike-light")
    return inventory.go_to_cart().checkout()


@pytest.mark.parametrize("first,last,postal,expected", [
    ("", "", "", "First Name is required"),
    ("Vishwajeet", "", "", "Last Name is required"),
    ("Vishwajeet", "Tulse", "", "Postal Code is required"),
])
def test_missing_information_shows_error(checkout, first, last, postal, expected):
    checkout.fill_information(first, last, postal)
    assert expected in checkout.error_message()


def test_overview_totals_are_correct(checkout):
    checkout.fill_information("Vishwajeet", "Tulse", "411041")
    subtotal, tax, total = checkout.subtotal(), checkout.tax(), checkout.total()
    assert subtotal == pytest.approx(39.98)
    assert tax == pytest.approx(round(subtotal * 0.08, 2))
    assert total == pytest.approx(subtotal + tax)


def test_complete_order(checkout):
    checkout.fill_information("Vishwajeet", "Tulse", "411041")
    checkout.finish()
    assert checkout.completion_message() == "Thank you for your order!"
    assert "checkout-complete" in checkout.driver.current_url
