from PySide6.QtCore import QObject, QTimer, Signal
import random

BASISWERTE = {
    "FASTEST": {"kosten": 120.0, "zeit": 20},
    "CHEAPEST": {"kosten": 90.0, "zeit": 34},
    "LOWEST_CO2": {"kosten": 100.0, "zeit": 30},
    "MOST_RESILIENT": {"kosten": 110.0, "zeit": 27},
}


class FakeBackend(QObject):
    """Testdaten statt echter Simulation (TESTWERTE, keine Ergebnisse).

    Hat dieselben Methodennamen wie später die echte Simulation, damit
    die Oberfläche beim Austausch nicht umgebaut werden muss.
    """

    snapshot_ready = Signal(dict)

    def __init__(self):
        super().__init__()
        self.tag = 0
        self.rng = random.Random(1)  # festes Seed: Testläufe sind reproduzierbar
        self.strategie = "FASTEST"
        self.aktive_szenarien = set()
        self.timer = QTimer(self)
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.step)

    def start(self):
        self.timer.start()

    def pause(self):
        self.timer.stop()

    def reset(self):
        self.timer.stop()
        self.tag = 0
        self.rng = random.Random(1)
        self.snapshot_ready.emit(self._kpis())

    def stop(self):
        self.timer.stop()

    def step(self):
        self.tag += 1
        self.snapshot_ready.emit(self._kpis())

    def set_strategy(self, name):
        self.strategie = name
        self.snapshot_ready.emit(self._kpis())

    def set_scenario(self, name, aktiv, ziel=None):
        schluessel = (name, ziel)
        if aktiv:
            self.aktive_szenarien.add(schluessel)
        else:
            self.aktive_szenarien.discard(schluessel)
        self.snapshot_ready.emit(self._kpis())

    def ist_aktiv(self, name, ziel=None):
        return (name, ziel) in self.aktive_szenarien

    def aktive_ziele(self):
        return {ziel for (_, ziel) in self.aktive_szenarien if ziel}

    def _werte(self, n, rauschen):
        """Kennzahlen für n aktive Szenarien (n=0: Referenz ohne Störung)."""
        basis = BASISWERTE[self.strategie]
        faktor = 1 + 0.15 * n
        return {
            "total_cost": round(basis["kosten"] * faktor + self.tag + rauschen * 2, 1),
            "transport_cost": round(basis["kosten"] * 0.6 * faktor + rauschen, 1),
            "co2_emissions": round(10 + 0.2 * self.tag + rauschen * 0.3, 1),
            "lead_time": round(basis["zeit"] + 4 * n + rauschen, 1),
            "risk_score": min(100, 20 + 15 * n),
            "service_level": round(max(0, 98 - 6 * n + rauschen), 1),
        }

    def _kpis(self):
        rauschen = self.rng.uniform(-1, 1)  # dieselbe Schwankung für beide Linien
        kpis = self._werte(len(self.aktive_szenarien), rauschen)
        kpis["tag"] = self.tag
        kpis["referenz"] = self._werte(0, rauschen)
        return kpis
    