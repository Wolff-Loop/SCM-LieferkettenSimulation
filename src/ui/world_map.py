from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLabel


class WorldMap(QLabel):
    """Weltkarte. Später Leaflet-Karte, vorerst nur ein Platzhalter."""

    def __init__(self):
        super().__init__("Karte folgt")
        self.setAlignment(Qt.AlignCenter)
        self.setMinimumSize(600, 400)
        self.setStyleSheet("background-color: #E8E3DC;")