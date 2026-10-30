from PySide6.QtWidgets import (QHBoxLayout, QLabel, QMainWindow, QVBoxLayout, QWidget)

from ui.dashboard import Dashboard
from ui.world_map import WorldMap

class MainWindow(QMainWindow):
    """Hauptfenster der Anwendung (Karte, Dashboard, Steuerung)."""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Supply Chain Digital Twin")
        self.resize(1200, 800)

        self.world_map = WorldMap()
        self.dashboard = Dashboard()
        self.controls = QLabel("Steuerung folgt")

        oben = QHBoxLayout()
        oben.addWidget(self.world_map, 3)
        oben.addWidget(self.dashboard, 1)

        haupt = QVBoxLayout()
        haupt.addLayout(oben, 5)
        haupt.addWidget(self.controls, 1)

        zentrum = QWidget()
        zentrum.setLayout(haupt)
        self.setCentralWidget(zentrum)