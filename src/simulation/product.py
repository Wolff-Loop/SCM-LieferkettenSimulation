from dataclasses import dataclass, field
from typing import List

from .component import Component


@dataclass
class Product:
    id: int
    name: str
    components: List[Component] = field(default_factory=list)