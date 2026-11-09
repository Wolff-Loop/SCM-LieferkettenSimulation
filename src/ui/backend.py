from PySide6.QtCore import QObject, QTimer, Signal

from src.core.application import Application


class Backend(QObject):
    """
    Schnittstelle zwischen UI und Fachlogik.

    Diese Klasse behält das Interface des bisherigen FakeBackend bei,
    verwendet aber das echte Netzwerk aus den JSON-Dateien.
    """

    snapshot_ready = Signal(dict)
    network_ready = Signal(dict)
    route_ready = Signal(dict)
    error_occurred = Signal(str)

    def __init__(self):
        super().__init__()

        self.application = Application()

        self.tag = 0
        self.running = False
        self.strategie = "FASTEST"
        self.aktive_szenarien = set()
        self.sendungen = []

        self.timer = QTimer(self)
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.step)

    def initialize(self):
        """
        Übergibt Knoten und Kanten an die UI.
        """
        network = {
            "nodes": self.application.get_nodes(),
            "edges": self.application.get_edges(),
            "statistics": (
                self.application.get_network_statistics()
            ),
        }

        self.network_ready.emit(network)
        self.snapshot_ready.emit(self._snapshot())

    def get_map_nodes(self):

        return (
            self.application
            .get_map_nodes()
        )
    
    def start(self):
        self.running = True
        self.timer.start()

    def pause(self):
        self.running = False
        self.timer.stop()

    def stop(self):
        self.running = False
        self.timer.stop()

    def reset(self):
        self.timer.stop()

        self.running = False
        self.tag = 0
        self.sendungen.clear()
        self.aktive_szenarien.clear()

        self.snapshot_ready.emit(self._snapshot())

    def step(self):
        self.tag += 1
        self.snapshot_ready.emit(self._snapshot())

    def set_strategy(self, name: str):
        allowed_strategies = {
            "FASTEST",
            "CHEAPEST",
            "LOWEST_CO2",
            "MOST_RESILIENT",
        }

        if name not in allowed_strategies:
            self.error_occurred.emit(
                f"Unbekannte Routingstrategie: {name}"
            )
            return

        self.strategie = name
        self.snapshot_ready.emit(self._snapshot())

    def calculate_route(
        self,
        source: str,
        target: str,
    ):
        try:
            route = self.application.calculate_route(
                source,
                target,
            )

            result = {
                "source": source,
                "target": target,
                "strategy": self.strategie,
                "nodes": route,
            }

            self.route_ready.emit(result)

        except Exception as error:
            self.error_occurred.emit(str(error))

    def set_scenario(
        self,
        name: str,
        aktiv: bool,
        ziel: str | None = None,
    ):
        key = (name, ziel)

        if aktiv:
            self.aktive_szenarien.add(key)
        else:
            self.aktive_szenarien.discard(key)

        self.snapshot_ready.emit(self._snapshot())

    def ist_aktiv(
        self,
        name: str,
        ziel: str | None = None,
    ) -> bool:
        return (name, ziel) in self.aktive_szenarien

    def aktive_ziele(self) -> set:
        return {
            ziel
            for _, ziel in self.aktive_szenarien
            if ziel
        }

    def ist_irgendwo_aktiv(self, name: str) -> bool:
        return any(
            event_name == name
            for event_name, _ in self.aktive_szenarien
        )

    def _snapshot(self) -> dict:
        """
        Einheitliches Datenformat für das Dashboard.

        Die KPI-Logik ist zunächst einfach gehalten. Entscheidend ist,
        dass die UI bereits mit dem echten Backend verbunden ist.
        """
        event_count = len(self.aktive_szenarien)

        strategy_values = {
            "FASTEST": {
                "cost": 120.0,
                "lead_time": 20.0,
                "co2": 18.0,
            },
            "CHEAPEST": {
                "cost": 90.0,
                "lead_time": 34.0,
                "co2": 14.0,
            },
            "LOWEST_CO2": {
                "cost": 105.0,
                "lead_time": 30.0,
                "co2": 8.0,
            },
            "MOST_RESILIENT": {
                "cost": 115.0,
                "lead_time": 27.0,
                "co2": 13.0,
            },
        }

        values = strategy_values[self.strategie]
        disruption_factor = 1 + (0.15 * event_count)

        return {
            "tag": self.tag,
            "strategy": self.strategie,
            "total_cost": round(
                values["cost"] * disruption_factor,
                1,
            ),
            "transport_cost": round(
                values["cost"] * 0.6 * disruption_factor,
                1,
            ),
            "co2_emissions": round(
                values["co2"] * disruption_factor,
                1,
            ),
            "lead_time": round(
                values["lead_time"] + (4 * event_count),
                1,
            ),
            "risk_score": min(
                100,
                20 + (15 * event_count),
            ),
            "service_level": max(
                0,
                98 - (6 * event_count),
            ),
            "sendungen": list(self.sendungen),
            "active_scenarios": [
                {
                    "name": name,
                    "target": target,
                }
                for name, target in self.aktive_szenarien
            ],
            "network_statistics": (
                self.application.get_network_statistics()
            ),
        }