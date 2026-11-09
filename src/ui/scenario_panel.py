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

# Szenarien ohne Ort: nur diese lassen sich in der Liste schalten
GLOBALE_SZENARIEN = {"Nachfrageanstieg"}


class ScenarioPanel(QGroupBox):
    """Zeigt die Szenarien; globale lassen sich schalten, ortsgebundene nur anzeigen."""

    scenario_toggled = Signal(str, bool)

    def __init__(self):
        super().__init__("Szenarien")
        layout = QVBoxLayout(self)
        self.kaestchen = {}
        for name in SZENARIEN:
            box = QCheckBox(name)
            if name in GLOBALE_SZENARIEN:
                box.toggled.connect(
                    lambda aktiv, n=name: self.scenario_toggled.emit(n, aktiv)
                )
            else:
                box.setEnabled(False)
                box.setToolTip(
                    "Auf der Karte auf einen Knoten, ein Land oder einen Engpass klicken"
                )
            layout.addWidget(box)
            self.kaestchen[name] = box

    def aktualisiere(self, backend, *_):
        """Setzt die Häkchen passend zum Zustand im Backend."""
        for name, box in self.kaestchen.items():
            aktiv = backend.ist_irgendwo_aktiv(name)
            if box.isChecked() != aktiv:
                box.blockSignals(True)   # sonst würde setChecked wieder ein Signal auslösen
                box.setChecked(aktiv)
                box.blockSignals(False)