class Inventory:

    def __init__(self):
        self.stock = {}

    def add_stock(self, item_name: str, quantity: int):
        self.stock[item_name] = (
            self.stock.get(item_name, 0) + quantity
        )

    def remove_stock(self, item_name: str, quantity: int):

        current = self.stock.get(item_name, 0)

        if quantity > current:
            raise ValueError(
                "Not enough stock available."
            )

        self.stock[item_name] -= quantity

    def get_stock_level(self, item_name: str):

        return self.stock.get(item_name, 0)