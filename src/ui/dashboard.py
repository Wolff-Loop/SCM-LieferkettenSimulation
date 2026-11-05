from PySide6.QtWidgets import QGridLayout, QLabel, QWidget

KPI_NAMEN = {
    "total_cost": "Gesamtkosten",
    "transport_cost": "Transportkosten",
    "co2_emissions": "CO₂",
    "lead_time": "Lieferzeit",
    "risk_score": "Risikoscore",
    "service_level": "Service Level",
}


class Dashboard(QWidget):
    """Zeigt die sechs Kennzahlen an."""

    def __init__(self):
        super().__init__()
        layout = QGridLayout(self)
        self.werte = {}
        for zeile, (schluessel, name) in enumerate(KPI_NAMEN.items()):
            layout.addWidget(QLabel(name), zeile, 0)
            wert = QLabel("–")
            layout.addWidget(wert, zeile, 1)
            self.werte[schluessel] = wert

    def update_kpis(self, kpis):
        for schluessel, wert in kpis.items():
            if schluessel in self.werte:
                self.werte[schluessel].setText(str(wert))

