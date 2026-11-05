from dataclasses import dataclass


@dataclass
class Component:
    id: int
    name: str
    supplier_id: int
    unit_cost: float
    weight_kg: float