from PySide6.QtCore import QObject, QTimer, Signal

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
        # DEINE AUFGABE: siehe unten
        pass

    def stop(self):
        self.timer.stop()

    def step(self):
        self.tag += 1
        self.snapshot_ready.emit(self._kpis())

    def set_strategy(self, name):
        self.strategie = name
        self.snapshot_ready.emit(self._kpis())

    def set_scenario(self, name, aktiv):
        # DEINE AUFGABE: siehe unten
        pass

    def _kpis(self):
        basis = BASISWERTE[self.strategie]
        n = len(self.aktive_szenarien)
        faktor = 1 + 0.15 * n
        return {
            "total_cost": round(basis["kosten"] * faktor + self.tag, 1),
            "transport_cost": round(basis["kosten"] * 0.6 * faktor, 1),
            "co2_emissions": round(10 + 0.2 * self.tag, 1),
            "lead_time": basis["zeit"] + 4 * n,
            "risk_score": min(100, 20 + 15 * n),
            "service_level": max(0, 98 - 6 * n),
        }