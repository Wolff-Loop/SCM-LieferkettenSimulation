import json
import sys
from pathlib import Path


def project_root():
    if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
        return Path(sys._MEIPASS)
    return Path(__file__).resolve().parents[2]


class NetworkLoader:
    def __init__(self, data_path=None):
        self.data_path = Path(data_path) if data_path else project_root() / "data"

    @staticmethod
    def load_json(filepath):
        with Path(filepath).open("r", encoding="utf-8") as file:
            return json.load(file)

    def _load_optional(self, *parts, default):
        path = self.data_path.joinpath(*parts)
        return self.load_json(path) if path.exists() else default

    def load_network_data(self):
        return {
            "suppliers": self.load_json(self.data_path / "nodes" / "suppliers.json"),
            "ports": self.load_json(self.data_path / "nodes" / "ports.json"),
            "airports": self._load_optional("nodes", "airports.json", default=[]),
            "rail_terminals": self.load_json(self.data_path / "nodes" / "rail_terminals.json"),
            "factories": self.load_json(self.data_path / "nodes" / "factories.json"),
            "warehouses": self._load_optional("nodes", "warehouses.json", default=[]),
            "bottlenecks": self._load_optional("nodes", "bottlenecks.json", default=[]),
            "edges": self.load_json(self.data_path / "routes" / "edges.json"),
            "transport_modes": self.load_json(self.data_path / "routes" / "transport_modes.json"),
            "geometries": self.load_json(self.data_path / "routes" / "geometries.json"),
            "products": self.load_json(self.data_path / "products.json"),
            "country_economics": self.load_json(self.data_path / "economics" / "countries.json"),
            "economic_config": self.load_json(self.data_path / "economics" / "model_config.json"),
        }
