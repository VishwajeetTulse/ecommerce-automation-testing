"""Cart tests (TC_CART_*)."""


def test_add_two_items_updates_badge(inventory):
    inventory.add_to_cart("sauce-labs-backpack")
    inventory.add_to_cart("sauce-labs-bike-light")
    assert inventory.cart_count() == 2


def test_cart_page_lists_added_items(inventory):
    inventory.add_to_cart("sauce-labs-backpack")
    inventory.add_to_cart("sauce-labs-bike-light")
    cart = inventory.go_to_cart()
    assert cart.item_names() == ["Sauce Labs Backpack", "Sauce Labs Bike Light"]


def test_remove_item_from_cart_page(inventory):
    inventory.add_to_cart("sauce-labs-backpack")
    inventory.add_to_cart("sauce-labs-bike-light")
    cart = inventory.go_to_cart()
    cart.remove("sauce-labs-bike-light")
    assert cart.item_names() == ["Sauce Labs Backpack"]
    assert inventory.cart_count() == 1


def test_remove_from_products_page(inventory):
    inventory.add_to_cart("sauce-labs-onesie")
    inventory.remove_from_cart("sauce-labs-onesie")
    assert inventory.cart_count() == 0
