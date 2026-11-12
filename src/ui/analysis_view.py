from collections import deque

from PySide6.QtCharts import QChart, QChartView, QLineSeries, QValueAxis
from PySide6.QtCore import Qt, QMargins
from PySide6.QtGui import QColor, QPainter, QPen
from PySide6.QtWidgets import (
    QGridLayout,
    QLabel,
    QScrollArea,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)


METRICS = {
    "total_cost": ("Gesamtkosten (€)", "€", 2),
    "purchase_cost": ("Einkauf inkl. Arbeit (€)", "€", 2),
    "material_cost": ("Materialkosten (€)", "€", 2),
    "labor_cost": ("Arbeitskosten (€)", "€", 2),
    "transport_cost": ("Transportkosten (€)", "€", 2),
    "customs_cost": ("Zollkosten (€)", "€", 2),
    "inventory_cost": ("Kapitalbindung (€)", "€", 2),
    "quality_cost": ("Qualitätskosten (€)", "€", 2),
    "carbon_cost": ("CO₂-Kosten (€)", "€", 2),
    "co2_emissions": ("CO₂-Emissionen (kg)", "kg", 2),
    "lead_time": ("Lieferzeit (Tage)", "Tage", 1),
    "risk_score": ("Risikoscore", "Punkte", 1),
    "service_level": ("Service Level / OTIF (%)", "%", 1),
}

MAX_POINTS = 120


class MetricChart(QChartView):
    """Ein einzelnes, automatisch skaliertes KPI-Zeitreihendiagramm."""

    def __init__(self, key, title, unit, decimals, parent=None):
        super().__init__(parent)
        self.key = key
        self.unit = unit
        self.decimals = decimals
        self.reference_values = deque(maxlen=MAX_POINTS)
        self.current_values = deque(maxlen=MAX_POINTS)

        self.reference_series = QLineSeries()
        self.reference_series.setName("ohne Szenario")
        reference_pen = QPen(QColor("#707070"), 2)
        reference_pen.setStyle(Qt.DashLine)
        self.reference_series.setPen(reference_pen)

        self.current_series = QLineSeries()
        self.current_series.setName("aktuell")
        self.current_series.setPen(QPen(QColor("#1f5bd8"), 2.5))

        chart = QChart()
        chart.setTitle(title)
        chart.addSeries(self.reference_series)
        chart.addSeries(self.current_series)
        chart.legend().setVisible(True)
        chart.legend().setAlignment(Qt.AlignBottom)
        chart.setMargins(QMargins(10, 8, 10, 8))
        chart.setBackgroundRoundness(7)
        chart.setAnimationOptions(QChart.NoAnimation)

        self.axis_x = QValueAxis()
        self.axis_x.setTitleText("Simulationstag")
        self.axis_x.setLabelFormat("%.0f")
        self.axis_x.setTickCount(6)
        self.axis_x.setMinorTickCount(0)

        self.axis_y = QValueAxis()
        self.axis_y.setTitleText(unit)
        self.axis_y.setLabelFormat("%.2f" if decimals == 2 else "%.1f")
        self.axis_y.setTickCount(6)
        self.axis_y.setMinorTickCount(0)

        chart.addAxis(self.axis_x, Qt.AlignBottom)
        chart.addAxis(self.axis_y, Qt.AlignLeft)
        for series in (self.reference_series, self.current_series):
            series.attachAxis(self.axis_x)
            series.attachAxis(self.axis_y)

        self.setChart(chart)
        self.setRenderHint(QPainter.Antialiasing)
        self.setMinimumSize(520, 295)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.show_empty_state()

    def show_empty_state(self):
        self.axis_x.setRange(0, 10)
        self.axis_y.setRange(0, 1)

    @staticmethod
    def _as_number(value):
        try:
            number = float(value)
            if number == number and abs(number) != float("inf"):
                return number
        except (TypeError, ValueError):
            pass
        return None

    def add_snapshot(self, day, current_value, reference_value):
        current = self._as_number(current_value)
        reference = self._as_number(reference_value)
        if current is None and reference is None:
            return

        if current is not None:
            self.current_values.append((float(day), current))
        if reference is not None:
            self.reference_values.append((float(day), reference))

        self._replace_series(self.current_series, self.current_values)
        self._replace_series(self.reference_series, self.reference_values)
        self._update_axes()

    @staticmethod
    def _replace_series(series, values):
        series.clear()
        for x, y in values:
            series.append(x, y)

    def _update_axes(self):
        points = list(self.current_values) + list(self.reference_values)
        if not points:
            self.show_empty_state()
            return

        xs = [x for x, _ in points]
        ys = [y for _, y in points]
        x_min, x_max = min(xs), max(xs)
        y_min, y_max = min(ys), max(ys)

        # Mindestens zehn Tage anzeigen, danach gleitendes Fenster.
        visible_max = max(10.0, x_max)
        visible_min = max(0.0, visible_max - MAX_POINTS + 1)
        self.axis_x.setRange(visible_min, visible_max)

        if y_min == y_max:
            # Konstante Zeitreihe trotzdem sichtbar machen.
            padding = max(abs(y_min) * 0.05, 1.0)
        else:
            padding = max((y_max - y_min) * 0.12, abs(y_max) * 0.01, 0.1)

        axis_min = y_min - padding
        axis_max = y_max + padding
        if y_min >= 0:
            axis_min = max(0.0, axis_min)
        self.axis_y.setRange(axis_min, axis_max)

        # Keine wissenschaftliche Schreibweise und keine abgeschnittenen "...".
        magnitude = max(abs(axis_min), abs(axis_max))
        if magnitude >= 1000:
            self.axis_y.setLabelFormat("%.0f")
        elif magnitude >= 100:
            self.axis_y.setLabelFormat("%.1f")
        else:
            self.axis_y.setLabelFormat("%.2f")

    def reset(self):
        self.reference_values.clear()
        self.current_values.clear()
        self.reference_series.clear()
        self.current_series.clear()
        self.show_empty_state()


class AnalysisView(QWidget):
    """Scrollbare Auswertung mit robusten, automatisch skalierten Charts."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.charts = {}

        outer_layout = QVBoxLayout(self)
        summary = QLabel(
            "Zeitreihenvergleich: gestrichelt = Baseline ohne Szenario, "
            "blau = aktueller Simulationslauf"
        )
        summary.setStyleSheet("font-weight: 600; padding: 6px;")
        outer_layout.addWidget(summary)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        container = QWidget()
        grid = QGridLayout(container)
        grid.setContentsMargins(8, 8, 8, 8)
        grid.setHorizontalSpacing(12)
        grid.setVerticalSpacing(12)

        for index, (key, (title, unit, decimals)) in enumerate(METRICS.items()):
            chart = MetricChart(key, title, unit, decimals)
            self.charts[key] = chart
            grid.addWidget(chart, index // 2, index % 2)

        scroll.setWidget(container)
        outer_layout.addWidget(scroll)

    def add_snapshot(self, snapshot):
        if not isinstance(snapshot, dict):
            return
        day = snapshot.get("tag", snapshot.get("day", 0))
        reference = snapshot.get("referenz", {}) or {}

        for key, chart in self.charts.items():
            chart.add_snapshot(
                day,
                snapshot.get(key),
                reference.get(key),
            )

    def reset(self):
        for chart in self.charts.values():
            chart.reset()
