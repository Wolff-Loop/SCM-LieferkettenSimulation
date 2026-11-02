from PySide6.QtWidgets import (QHBoxLayout, QLabel, QMainWindow, QVBoxLayout, QWidget)

from ui.dashboard import Dashboard
from ui.world_map import WorldMap
from ui.control_panel import ControlPanel
from ui.scenario_panel import ScenarioPanel
from ui.backend import FakeBackend
from PySide6.QtGui import QCursor
from PySide6.QtWidgets import QMenu

import json

class MainWindow(QMainWindow):
    """Hauptfenster der Anwendung (Karte, Dashboard, Steuerung)."""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Supply Chain Digital Twin")
        self.resize(1200, 800)

        self.world_map = WorldMap()
        self.dashboard = Dashboard()
        self.controls = ControlPanel()
        self.scenarios = ScenarioPanel()
        self.backend = FakeBackend()

        rechts = QVBoxLayout()
        rechts.addWidget(self.dashboard, 3)
        rechts.addWidget(self.scenarios, 2)

        oben = QHBoxLayout()
        oben.addWidget(self.world_map, 3)
        oben.addLayout(rechts, 1)

        haupt = QVBoxLayout()
        haupt.addLayout(oben, 5)
        haupt.addWidget(self.controls, 1)

        zentrum = QWidget()
        zentrum.setLayout(haupt)
        self.setCentralWidget(zentrum)

        self.knoten_typen = {}

        self.controls.start_clicked.connect(self.backend.start)
        self.controls.pause_clicked.connect(self.backend.pause)
        self.controls.reset_clicked.connect(self.backend.reset)
        self.controls.stop_clicked.connect(self.backend.stop)
        self.controls.strategy_changed.connect(self.backend.set_strategy)
        self.scenarios.scenario_toggled.connect(self.backend.set_scenario)
        self.backend.snapshot_ready.connect(self.dashboard.update_kpis)
        self.world_map.loadFinished.connect(self.zeige_testdaten)
        self.world_map.map_clicked.connect(self.on_map_click)
        self.backend.snapshot_ready.connect(self.aktualisiere_markierungen)

    SZENARIEN_JE_TYP = {
        "LIEFERANT": ["Lieferantenausfall"],
        "HAFEN": ["Hafenstreik"],
        "FABRIK": ["Produktionsausfall"],
        "LAGER": ["Lagerausfall"],
        "FLUGHAFEN": ["Flughafensperrung"],
    }

    SZENARIEN_LAND = ["Krieg", "Naturkatastrophe", "Streik"]

    def on_map_click(self, art, name):
        if art == "country":
            titel = name
            szenarien = self.SZENARIEN_LAND
        else:
            typ = self.knoten_typen.get(name)
            titel = f"{name} ({typ})"
            szenarien = self.SZENARIEN_JE_TYP.get(typ, [])
        if not szenarien:
            return
        menu = QMenu(self)
        menu.addSection(titel)
        aktionen = {}
        for s in szenarien:
            a = menu.addAction(s)
            a.setCheckable(True)
            a.setChecked(self.backend.ist_aktiv(s, name))
            aktionen[a] = s
        gewaehlt = menu.exec(QCursor.pos())
        if gewaehlt in aktionen:
            s = aktionen[gewaehlt]
            self.backend.set_scenario(s, not self.backend.ist_aktiv(s, name), ziel=name)

    def aktualisiere_markierungen(self, *_):
        ziele = self.backend.aktive_ziele()
        knoten = [z for z in ziele if z in self.knoten_typen]
        laender = [z for z in ziele if z not in self.knoten_typen]
        self.world_map.set_highlights(knoten, laender)

    def zeige_testdaten(self):
        knoten = [
            {"name": "Heilbronn", "lat": 49.14, "lon": 9.22, "typ": "FABRIK"},
            {"name": "Lager Heilbronn", "lat": 49.17, "lon": 9.25, "typ": "LAGER"},
            {"name": "Rotterdam", "lat": 51.92, "lon": 4.48, "typ": "HAFEN"},
            {"name": "Fremantle", "lat": -32.0, "lon": 115.8, "typ": "LIEFERANT"},
            {"name": "Frankfurt", "lat": 50.04, "lon": 8.56, "typ": "FLUGHAFEN"},
        ]
        self.knoten_typen = {k["name"]: k["typ"] for k in knoten}
        self.world_map.set_nodes(knoten)

        # Seeroute Fremantle -> Rotterdam
        self.world_map.draw_route(
            [[-32.0, 115.8], [-10, 95], [5, 78], [12.5, 54], [12.2, 47], [12.5, 43.5],
            [20, 38], [27.5, 34], [29.9, 32.5], [31.3, 32.3], [34, 27], [35, 20],
            [37.8, 9], [38, 0], [36.3, -2], [35.95, -5.5], [36.5, -9.5], [43.5, -9.8],
            [48.5, -5.5], [49.9, -3], [50.5, 0.5], [51.4, 1.8], [52, 3.0], [51.92, 4.48]],
            "SEESCHIFF",
        )
        # Binnenschiff Rotterdam -> Heilbronn
        self.world_map.draw_route([[51.92, 4.48], [49.14, 9.22]], "BINNENSCHIFF")
        # Flugzeug Fremantle -> Frankfurt
        self.world_map.draw_route([[-32.0, 115.8], [50.04, 8.56]], "FLUGZEUG")
        # LKW Frankfurt -> Heilbronn
        self.world_map.draw_route([[50.04, 8.56], [49.14, 9.22]], "LKW")