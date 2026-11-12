# Chart-Fix

Ersetzt `src/ui/analysis_view.py`.

Der Fix behebt:

- abgeschnittene Achsenbeschriftungen (`...`),
- verschwundene Linien bei konstanten Werten,
- fehlende automatische Y-Skalierung,
- unlesbare wissenschaftliche beziehungsweise zu lange Zahlenformate,
- unbegrenztes Wachstum der Zeitreihen,
- zu kleine Diagrammflächen,
- fehlende Scrollbarkeit bei vielen KPIs.

Die Klasse behält die vorhandene Schnittstelle bei:

```python
analysis.add_snapshot(snapshot)
analysis.reset()
```
