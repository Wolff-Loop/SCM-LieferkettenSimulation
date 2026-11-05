from dataclasses import dataclass


@dataclass
class Order:
    id: int
    supplier: str
    destination: str
    quantity: int