from PySide6.QtCore import QObject, QTimer, Signal
import networkx as nx

from src.core.application import Application
from src.events.event_manager import EventManager
from src.events.war_event import WarEvent
from src.events.strike_event import StrikeEvent
from src.events.supplier_failure_event import SupplierFailureEvent
from src.events.canal_blockage_event import CanalBlockageEvent
from src.events.graph_events import NodeStatusEvent
from src.analytics.kpi_engine import KPIEngine


class Backend(QObject):
    snapshot_ready = Signal(dict)
    routes_ready = Signal(dict)
    error_occurred = Signal(str)

    def __init__(self):
        super().__init__()
        self.application = Application()
        self.event_manager = EventManager(self.application)
        self.tag = 0
        self.strategie = "FASTEST"
        self.current_routes = []
        self.baseline_routes = []
        self.sendungen = []
        self.naechste_id = 1
        self.timer = QTimer(self)
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.step)

    def initialize(self):
        self.recalculate_routes()
        self.snapshot_ready.emit(self._snapshot())

    def get_map_nodes(self):
        return self.application.get_map_nodes()

    def start(self): self.timer.start()
    def pause(self): self.timer.stop()
    def stop(self): self.timer.stop()

    def reset(self):
        self.timer.stop()
        self.tag = 0
        self.sendungen.clear()
        self.naechste_id = 1
        self.event_manager.clear()
        self.application.reload_network()
        self.event_manager = EventManager(self.application)
        self.recalculate_routes()
        self.snapshot_ready.emit(self._snapshot())

    def step(self):
        self.tag += 1
        self._move_shipments()
        if self.tag % 5 == 1:
            self._create_shipments()
        self.snapshot_ready.emit(self._snapshot())

    def set_strategy(self, name):
        if name not in {"FASTEST", "CHEAPEST", "LOWEST_CO2", "MOST_RESILIENT"}:
            self.error_occurred.emit(f"Unbekannte Routingstrategie: {name}")
            return
        self.strategie = name
        self.recalculate_routes()
        self.snapshot_ready.emit(self._snapshot())

    def set_scenario(self, name, aktiv, ziel=None):
        event = self._make_event(name, ziel)
        if aktiv:
            self.event_manager.activate(event)
        else:
            self.event_manager.deactivate(event.name, event.target)
        self.recalculate_routes()
        self.snapshot_ready.emit(self._snapshot())

    def _make_event(self, name, ziel):
        if name == "Krieg": return WarEvent(ziel)
        if name in {"Streik", "Hafenstreik"}: return StrikeEvent(ziel)
        if name == "Lieferantenausfall": return SupplierFailureEvent(ziel)
        if name in {"Suezkanal-Blockade", "Sperrung"} and ziel in {None, "Suezkanal"}:
            return CanalBlockageEvent()
        if name in {"Naturkatastrophe", "Produktionsausfall", "Lagerausfall", "Flughafensperrung"}:
            return NodeStatusEvent(name, ziel, 1.0)
        return NodeStatusEvent(name, "__GLOBAL__", 0.0)

    def recalculate_routes(self):
        available, unavailable = [], []
        for product in self.application.products:
            try:
                route = self.application.calculate_product_route(product, self.strategie)
                available.append({**product, **route})
            except (nx.NetworkXNoPath, nx.NodeNotFound) as error:
                unavailable.append({**product, "error": str(error), "segments": []})

        self.current_routes = available
        # Referenz immer auf einem ungestörten, frisch geladenen Graphen berechnen.
        reference_app = Application()
        self.baseline_routes = reference_app.calculate_all_product_routes(self.strategie)
        self.routes_ready.emit({"chains": available + unavailable})
        if unavailable:
            names = ", ".join(chain["name"] for chain in unavailable)
            self.error_occurred.emit(f"Keine Route verfügbar für: {names}")

    def ist_aktiv(self, name, ziel=None):
        event = self._make_event(name, ziel)
        return self.event_manager.is_active(event.name, event.target)

    def aktive_ziele(self):
        return {e.target for e in self.event_manager.get_active_events()
                if e.target and e.target != "__GLOBAL__"}

    def ist_irgendwo_aktiv(self, name):
        return any(e.name == name for e in self.event_manager.get_active_events())

    def _create_shipments(self):
        for chain in self.current_routes:
            first_mode = chain["segments"][0]["ui_mode"] if chain["segments"] else "LKW"
            self.sendungen.append({
                "id": self.naechste_id,
                "route": f'chain_{chain["id"]}_0',
                "fortschritt": 0.0,
                "modus": first_mode,
                "ware": chain["name"],
            })
            self.naechste_id += 1

    def _move_shipments(self):
        for shipment in self.sendungen:
            shipment["fortschritt"] = min(1.0, shipment["fortschritt"] + 0.08)
        self.sendungen = [shipment for shipment in self.sendungen if shipment["fortschritt"] < 1.0]

    def _snapshot(self):
        events = self.event_manager.get_active_events()
        current = KPIEngine.calculate(self.current_routes, len(events), self.tag)
        reference = KPIEngine.calculate(self.baseline_routes, 0, self.tag)
        return {
            "tag": self.tag, "strategy": self.strategie,
            **current, "referenz": reference,
            "sendungen": [dict(s) for s in self.sendungen],
            "active_scenarios": [{"name": e.name, "target": e.target} for e in events],
            "network_statistics": self.application.get_network_statistics(),
        }

    def get_country_economics(self):
        return self.application.get_country_economics()

    def set_country_economics(self, country, labor_cost=None, duty_rate=None, risk_rate=None):
        self.application.set_country_economics(country, labor_cost, duty_rate, risk_rate)
        self.recalculate_routes()
        self.snapshot_ready.emit(self._snapshot())
