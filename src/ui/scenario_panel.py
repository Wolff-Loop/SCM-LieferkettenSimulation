from PySide6.QtCore import Signal
from PySide6.QtWidgets import QCheckBox, QGroupBox, QVBoxLayout

SZENARIEN = [
    "Krieg", "Streik", "Naturkatastrophe", "Lieferantenausfall",
    "Suezkanal-Blockade", "Nachfrageanstieg",
]
GLOBALE_SZENARIEN = {"Nachfrageanstieg", "Suezkanal-Blockade"}


class ScenarioPanel(QGroupBox):
    scenario_toggled = Signal(str, bool)

    def __init__(self):
        super().__init__("Szenarien")
        layout = QVBoxLayout(self)
        self.kaestchen = {}
        for name in SZENARIEN:
            box = QCheckBox(name)
            if name in GLOBALE_SZENARIEN:
                box.toggled.connect(lambda aktiv, n=name: self.scenario_toggled.emit(n, aktiv))
            else:
                box.setEnabled(False)
                box.setToolTip("Auf der Karte einen Knoten oder ein Land anklicken")
            layout.addWidget(box)
            self.kaestchen[name] = box

    def aktualisiere(self, backend, *_):
        for name, box in self.kaestchen.items():
            aktiv = backend.ist_irgendwo_aktiv(name)
            if box.isChecked() != aktiv:
                box.blockSignals(True)
                box.setChecked(aktiv)
                box.blockSignals(False)
