from src.simulation.inventory import Inventory


def test_add_stock():

    inventory = Inventory()

    inventory.add_stock(
        "Battery",
        100
    )

    assert inventory.get_stock_level(
        "Battery"
    ) == 100


def test_remove_stock():

    inventory = Inventory()

    inventory.add_stock(
        "Battery",
        100
    )

    inventory.remove_stock(
        "Battery",
        50
    )

    assert inventory.get_stock_level(
        "Battery"
    ) == 50