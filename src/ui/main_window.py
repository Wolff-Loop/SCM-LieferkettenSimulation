from PySide6.QtGui import QCursor
from PySide6.QtWidgets import QHBoxLayout, QMainWindow, QMenu, QTabWidget, QVBoxLayout, QWidget

from src.ui.dashboard import Dashboard
from src.ui.world_map import WorldMap
from src.ui.control_panel import ControlPanel
from src.ui.scenario_panel import ScenarioPanel
from src.ui.backend import Backend
from src.ui.analysis_view import AnalysisView


class MainWindow(QMainWindow):
    SZENARIEN_JE_TYP = {
        "LIEFERANT": ["Lieferantenausfall"], "HAFEN": ["Hafenstreik"],
        "FABRIK": ["Produktionsausfall"], "LAGER": ["Lagerausfall"],
        "FLUGHAFEN": ["Flughafensperrung"], "ENGPASS": ["Sperrung"],
    }
    SZENARIEN_LAND = ["Krieg", "Naturkatastrophe", "Streik"]

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Supply Chain Digital Twin – 6 parallele Lieferketten")
        self.resize(1200, 800)
        self.world_map, self.dashboard = WorldMap(), Dashboard()
        self.controls, self.scenarios = ControlPanel(), ScenarioPanel()
        self.analysis, self.backend = AnalysisView(), Backend()
        self.knoten_typen = {}

        right = QVBoxLayout(); right.addWidget(self.dashboard, 3); right.addWidget(self.scenarios, 2)
        top = QHBoxLayout(); top.addWidget(self.world_map, 3); top.addLayout(right, 1)
        layout = QVBoxLayout(); layout.addLayout(top, 5); layout.addWidget(self.controls, 1)
        page = QWidget(); page.setLayout(layout)
        tabs = QTabWidget(); tabs.addTab(page, "Simulation"); tabs.addTab(self.analysis, "Auswertung")
        self.setCentralWidget(tabs)

        self.controls.start_clicked.connect(self.backend.start)
        self.controls.pause_clicked.connect(self.backend.pause)
        self.controls.reset_clicked.connect(self.backend.reset)
        self.controls.reset_clicked.connect(self.analysis.reset)
        self.controls.stop_clicked.connect(self.backend.stop)
        self.controls.strategy_changed.connect(self.backend.set_strategy)
        self.scenarios.scenario_toggled.connect(self.backend.set_scenario)
        self.backend.snapshot_ready.connect(self.dashboard.update_kpis)
        self.backend.snapshot_ready.connect(self.analysis.add_snapshot)
        self.backend.snapshot_ready.connect(self.aktualisiere_markierungen)
        self.backend.snapshot_ready.connect(lambda *_: self.scenarios.aktualisiere(self.backend))
        self.backend.snapshot_ready.connect(self.aktualisiere_sendungen)
        self.backend.routes_ready.connect(self.zeige_lieferketten)
        self.backend.error_occurred.connect(self.zeige_fehler)
        self.world_map.loadFinished.connect(self.zeige_netzwerk)
        self.world_map.map_clicked.connect(self.on_map_click)

    def zeige_netzwerk(self, ok=True):
        if not ok:
            self.zeige_fehler("Die lokale Leaflet-Karte konnte nicht geladen werden.")
            return
        nodes = self.backend.get_map_nodes()
        self.knoten_typen = {node["name"]: node["typ"] for node in nodes}
        self.world_map.set_nodes(nodes)
        self.backend.initialize()

    def zeige_lieferketten(self, result):
        self.world_map.clear_routes()
        for chain in result.get("chains", []):
            for index, segment in enumerate(chain.get("segments", [])):
                # Jede Teilstrecke erhält eine eindeutige ID. Dadurch wird keine
                # maritime Geometrie durch eine direkte Luftlinie überschrieben.
                route_id = f'chain_{chain["id"]}_{index}'
                self.world_map.draw_route(segment["geometry"], segment["ui_mode"], route_id)

    def on_map_click(self, art, name):
        if art == "country":
            title, scenarios = name, self.SZENARIEN_LAND
        else:
            node_type = self.knoten_typen.get(name)
            title, scenarios = f"{name} ({node_type})", self.SZENARIEN_JE_TYP.get(node_type, [])
        if not scenarios: return
        menu = QMenu(self); menu.addSection(title); actions = {}
        for scenario in scenarios:
            action = menu.addAction(scenario); action.setCheckable(True)
            action.setChecked(self.backend.ist_aktiv(scenario, name)); actions[action] = scenario
        selected = menu.exec(QCursor.pos())
        if selected in actions:
            scenario = actions[selected]
            self.backend.set_scenario(scenario, not self.backend.ist_aktiv(scenario, name), ziel=name)

    def aktualisiere_markierungen(self, *_):
        targets = self.backend.aktive_ziele()
        self.world_map.set_highlights(
            [target for target in targets if target in self.knoten_typen],
            [target for target in targets if target not in self.knoten_typen],
        )

    def aktualisiere_sendungen(self, snapshot):
        self.world_map.set_shipments(snapshot.get("sendungen", []))

    def zeige_fehler(self, message):
        self.statusBar().showMessage(message, 10000)
