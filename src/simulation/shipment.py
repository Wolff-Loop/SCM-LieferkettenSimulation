from dataclasses import dataclass
from enum import Enum


class ShipmentStatus(Enum):
    PREPARING = "PREPARING"
    IN_TRANSIT = "IN_TRANSIT"
    DELAYED = "DELAYED"
    DELIVERED = "DELIVERED"
    CANCELLED = "CANCELLED"


@dataclass
class Shipment:
    id: int
    origin: str
    destination: str
    quantity: int
    route_id: str | None = None
    current_location: str | None = None
    progress_percent: float = 0
    status: ShipmentStatus = (
        ShipmentStatus.PREPARING
    )