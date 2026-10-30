from PySide6.QtWidgets import (QHBoxLayout, QLabel, QMainWindow, QVBoxLayout, QWidget)

from ui.dashboard import Dashboard
from ui.world_map import WorldMap
from ui.control_panel import ControlPanel
from ui.scenario_panel import ScenarioPanel
from ui.backend import FakeBackend

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

        self.controls.start_clicked.connect(self.backend.start)
        self.controls.pause_clicked.connect(self.backend.pause)
        self.controls.reset_clicked.connect(self.backend.reset)
        self.controls.stop_clicked.connect(self.backend.stop)
        self.controls.strategy_changed.connect(self.backend.set_strategy)
        self.scenarios.scenario_toggled.connect(self.backend.set_scenario)
        self.backend.snapshot_ready.connect(self.dashboard.update_kpis)
        self.world_map.loadFinished.connect(self.zeige_testdaten)

    def zeige_testdaten(self):
        self.world_map.set_nodes([
            {"name": "Heilbronn", "lat": 49.14, "lon": 9.22, "color": "#9C7F5B"},
            {"name": "Rotterdam", "lat": 51.92, "lon": 4.48, "color": "#8A8178"},
            {"name": "Fremantle", "lat": -32.0, "lon": 115.8, "color": "#2E2C2A"},
        ])
        self.world_map.draw_route(
            [[-32.0, 115.8], [-10, 95], [5, 78], [12.5, 54], [12.2, 47], [12.5, 43.5],
            [20, 38], [27.5, 34], [29.9, 32.5], [31.3, 32.3], [34, 27], [35, 20],
            [37.8, 9], [38, 0], [36.3, -2], [35.95, -5.5], [36.5, -9.5], [43.5, -9.8],
            [48.5, -5.5], [49.9, -3], [50.5, 0.5], [51.4, 1.8], [52, 3.0], [51.92, 4.48]],
            "SEESCHIFF",
        )
        self.world_map.draw_route([[51.92, 4.48], [49.14, 9.22]], "BINNENSCHIFF")