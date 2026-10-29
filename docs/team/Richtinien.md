# Approved Technology Stack

Diese Bibliotheken dürfen für das Projekt verwendet werden.

Ziel:

- Kompatibilität zwischen allen Modulen
- Einfache EXE-Erstellung mit PyInstaller
- Keine unnötigen Abhängigkeiten
- Wartbarkeit

---

# Python

Version:

```text
Python 3.12
```

Alle Entwickler verwenden dieselbe Version.

---

# GUI

```text
PySide6
```

Install:

```bash
pip install pyside6
```

Verwendung:

- Fenster
- Menüs
- Buttons
- Layouts
- Dialoge

Alternative Bibliotheken sind nicht erlaubt.

Nicht verwenden:

- Tkinter
- Kivy
- wxPython

---

# Kartenanzeige

```text
Leaflet
```

in einer eingebetteten HTML-Komponente.

Install:

```bash
pip install pyqtwebengine
```

oder

```bash
pip install pyside6-addons
```

Verwendung:

- Weltkarte
- Marker
- Routendarstellung

Nicht verwenden:

- ArcGIS SDK
- Cesium
- Google Maps API

---

# Routing & Netzwerk

```text
NetworkX
```

Install:

```bash
pip install networkx
```

Verwendung:

- Supply Chain Graph
- Dijkstra
- Routing

Nicht verwenden:

- graph-tool
- igraph

---

# Datenverarbeitung

```text
Pandas
```

Install:

```bash
pip install pandas
```

Verwendung:

- CSV
- KPI Auswertungen
- Reports

---

# Numerische Berechnung

```text
NumPy
```

Install:

```bash
pip install numpy
```

Verwendung:

- CO₂ Berechnungen
- KPI Berechnungen

---

# Datenhaltung

```text
SQLite
```

Verwendung:

Python Standardbibliothek:

```python
sqlite3
```

Keine zusätzliche Installation nötig.

Nicht verwenden:

- PostgreSQL
- MongoDB
- MySQL

Begründung:

EXE bleibt einfacher.

---

# Datenformate

Verwenden:

```text
JSON
CSV
SQLite
```

Nicht verwenden:

```text
Excel als Datenbank
XML
YAML
```

---

# Logging

```python
logging
```

Standard Python Bibliothek nutzen.

---

# Testing

```text
pytest
```

Install:

```bash
pip install pytest
```

---

# Build Tool

```text
PyInstaller
```

Install:

```bash
pip install pyinstaller
```

Build:

```bash
pyinstaller --onefile --windowed main.py
```

---

# Dokumentation

```text
Markdown
```

Dokumente:

- README.md
- ADRs
- Meeting Notes
- UML Dokumentation

---

# Verbotene Bibliotheken

Nicht verwenden:

```text
TensorFlow
PyTorch
OpenCV
Spark
Dask
Selenium
ArcGIS SDK
QGIS SDK
Docker Abhängigkeiten
```

Begründung:

Unnötig komplex für dieses Projekt.
Große EXE-Dateien.
Erhöhtes Fehlerrisiko.