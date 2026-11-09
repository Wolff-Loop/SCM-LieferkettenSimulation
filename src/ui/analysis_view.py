from PySide6.QtCharts import QChart, QChartView, QLineSeries, QValueAxis
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QPainter, QPen
from PySide6.QtWidgets import QGridLayout, QWidget

from src.ui.dashboard import KPI_NAMEN  


class KpiChart(QChartView):
    """Liniendiagramm einer Kennzahl: aktueller Lauf gegen Referenz ohne Szenario."""

    def __init__(self, titel):
        # Diagramm zuerst bauen, dann an die View übergeben
        referenz = QLineSeries()
        referenz.setName("ohne Szenario")
        referenz.setPen(QPen(QColor("#888888"), 2, Qt.DashLine))
        aktuell = QLineSeries()
        aktuell.setName("aktuell")
        aktuell.setPen(QPen(QColor("#0F3CDC"), 2))
        achse_x = QValueAxis()
        achse_y = QValueAxis()
        achse_x.setLabelFormat("%d")
        achse_x.setTickType(QValueAxis.TicksDynamic)
        achse_x.setTickAnchor(0)
        achse_x.setTickInterval(10)
        chart = QChart()
        for serie in (referenz, aktuell):  # Referenz zuerst, damit "aktuell" oben liegt
            chart.addSeries(serie)
        chart.addAxis(achse_x, Qt.AlignBottom)
        chart.addAxis(achse_y, Qt.AlignLeft)
        for serie in (referenz, aktuell):
            serie.attachAxis(achse_x)
            serie.attachAxis(achse_y)
        chart.setTitle(titel)
        chart.legend().setAlignment(Qt.AlignBottom)
        super().__init__(chart)
        self.setRenderHint(QPainter.Antialiasing)
        self.aktuell = aktuell
        self.referenz = referenz
        self.achse_x = achse_x
        self.achse_y = achse_y

    @staticmethod
    def _setze(serie, x, y):
        n = serie.count()
        if n > 0 and serie.at(n - 1).x() == x:
            serie.replace(n - 1, x, y)  # gleicher Tag: letzten Punkt aktualisieren
        else:
            serie.append(x, y)

    def add_point(self, x, y, y_referenz=None):
        self._setze(self.aktuell, x, y)
        if y_referenz is not None:
            self._setze(self.referenz, x, y_referenz)
        self.achse_x.setRange(0, max(x, 1))
        ys = [p.y() for s in (self.aktuell, self.referenz) for p in s.points()]
        unten, oben = min(ys), max(ys)
        rand = (oben - unten) * 0.1 or 1
        self.achse_y.setRange(unten - rand, oben + rand)

    def clear(self):
        self.aktuell.clear()
        self.referenz.clear()


class AnalysisView(QWidget):
    """Tab 'Auswertung': Verlauf aller Kennzahlen, aktuell gegen Referenz."""

    def __init__(self):
        super().__init__()
        layout = QGridLayout(self)
        self.charts = {}
        self.letzter_tag = -1
        for i, (schluessel, name) in enumerate(KPI_NAMEN.items()):
            chart = KpiChart(name)
            layout.addWidget(chart, i // 2, i % 2)  # zwei Spalten
            self.charts[schluessel] = chart

    def add_snapshot(self, kpis):
        tag = kpis.get("tag")
        if tag is None:
            return
        if tag < self.letzter_tag:  # Simulation wurde zurückgesetzt
            self.reset()
        self.letzter_tag = tag
        referenz = kpis.get("referenz", {})
        for schluessel, chart in self.charts.items():
            if schluessel not in kpis:
                continue
            try:
                ref = referenz.get(schluessel)
                chart.add_point(
                    tag,
                    float(kpis[schluessel]),
                    float(ref) if ref is not None else None,
                )
            except (TypeError, ValueError):
                pass

    def reset(self):
        self.letzter_tag = -1
        for chart in self.charts.values():
            chart.clear()