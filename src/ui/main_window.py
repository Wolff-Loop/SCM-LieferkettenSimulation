from PySide6.QtWidgets import (QHBoxLayout, QLabel, QMainWindow, QVBoxLayout, QWidget)

from ui.dashboard import Dashboard
from ui.world_map import WorldMap
from ui.control_panel import ControlPanel
from ui.scenario_panel import ScenarioPanel

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

        self.controls.start_clicked.connect(lambda: print("Start"))
        self.controls.strategy_changed.connect(lambda name: print("Strategie:", name))
        self.scenarios.scenario_toggled.connect(lambda name, aktiv: print("Szenario:", name))