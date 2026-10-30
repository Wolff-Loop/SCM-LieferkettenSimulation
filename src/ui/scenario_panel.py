from PySide6.QtCore import Signal
from PySide6.QtWidgets import QCheckBox, QGroupBox, QVBoxLayout

SZENARIEN = [
    "Krieg",
    "Streik",
    "Naturkatastrophe",
    "Lieferantenausfall",
    "Suezkanal-Blockade",
    "Nachfrageanstieg",
]


class ScenarioPanel(QGroupBox):
    """Schalter für die Szenarien (Störungen)."""

    scenario_toggled = Signal(str, bool)

    def __init__(self):
        super().__init__("Szenarien")
        layout = QVBoxLayout(self)
        for name in SZENARIEN:
            kaestchen = QCheckBox(name)
            kaestchen.toggled.connect(
                lambda aktiv, n=name: self.scenario_toggled.emit(n, aktiv)
            )
            layout.addWidget(kaestchen)