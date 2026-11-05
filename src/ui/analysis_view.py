from PySide6.QtCharts import QChart, QChartView, QLineSeries, QValueAxis
from PySide6.QtCore import Qt
from PySide6.QtGui import QPainter
from PySide6.QtWidgets import QGridLayout, QWidget

from ui.dashboard import KPI_NAMEN  # Importpfad ggf. an dein Projekt anpassen


class KpiChart(QChartView):
    """Ein Liniendiagramm für eine Kennzahl über die Zeit."""

    def __init__(self, titel):
        # Diagramm zuerst bauen, dann an die View übergeben
        serie = QLineSeries()
        achse_x = QValueAxis()
        achse_y = QValueAxis()
        chart = QChart()
        chart.addSeries(serie)
        chart.addAxis(achse_x, Qt.AlignBottom)
        chart.addAxis(achse_y, Qt.AlignLeft)
        serie.attachAxis(achse_x)
        serie.attachAxis(achse_y)
        chart.setTitle(titel)
        chart.legend().hide()
        super().__init__(chart)
        self.setRenderHint(QPainter.Antialiasing)
        self.serie = serie
        self.achse_x = achse_x
        self.achse_y = achse_y

    def add_point(self, x, y):
        n = self.serie.count()
        if n > 0 and self.serie.at(n - 1).x() == x:
            self.serie.replace(n - 1, x, y)  # gleicher Tag: letzten Punkt aktualisieren
        else:
            self.serie.append(x, y)
        self.achse_x.setRange(0, max(x, 1))
        ys = [p.y() for p in self.serie.points()]
        unten, oben = min(ys), max(ys)
        rand = (oben - unten) * 0.1 or 1
        self.achse_y.setRange(unten - rand, oben + rand)

    def clear(self):
        self.serie.clear()


class AnalysisView(QWidget):
    """Tab 'Auswertung': Verlauf aller Kennzahlen über die Simulation."""

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
        for schluessel, wert in kpis.items():
            if schluessel in self.charts:
                try:
                    self.charts[schluessel].add_point(tag, float(wert))
                except (TypeError, ValueError):
                    pass

    def reset(self):
        self.letzter_tag = -1
        for chart in self.charts.values():
            chart.clear()