# Demo-Integrationspatch

## Ziel

Dieser Patch verbindet das echte JSON-Netzwerk, strategieabhängiges NetworkX-Routing, Ereignisse, KPI-Berechnung und die PySide6/Leaflet-UI.

## Einspielen

1. Alle Dateien aus diesem Patch in die Repository-Wurzel kopieren und vorhandene Dateien ersetzen.
2. Routengeometrien ergänzen:

```bash
python scripts/upgrade_geometries.py
```

3. Python 3.12 verwenden und Abhängigkeiten installieren:

```powershell
py -3.12 -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

4. Tests:

```powershell
pytest -q
```

5. Anwendung:

```powershell
python -m src.main
```

## Demoablauf

1. Start: `FASTEST` zeigt die Luftfrachtroute Lens Technology → Shanghai Airport → Frankfurt → Heilbronn.
2. `LOWEST_CO2` auswählen: Route wechselt auf LKW → Shanghai Port → Singapur → Rotterdam → Duisburg → Heilbronn.
3. Im Szenario-Panel `Suezkanal-Blockade` aktivieren: Route wird über Durban oder Hamburg neu berechnet.
4. Auf der Karte Rotterdam anklicken und `Hafenstreik` aktivieren: Route nutzt Hamburg.
5. Start drücken: Simulationstag und Sendung bewegen sich; Dashboard und Auswertung werden aktualisiert.
6. Reset drücken: Baseline wird wiederhergestellt.

## Wichtige Modellgrenze

Die Routengeometrien sind kuratierte Visualisierungskorridore. Dijkstra rechnet auf den Gewichten in `edges.json` und den aus `transport_modes.json` abgeleiteten Werten.

## Sechs parallele Lieferketten

Die Demo berechnet und visualisiert gleichzeitig:

1. Uhrwerk – Citizen Miyota, Japan
2. Batterie – Panasonic Energy, Japan
3. Saphirglas / Display – Lens Technology, China
4. Gehäuse – Jabil Mexico
5. Lederarmband – HLP Leather, Südafrika
6. Verpackung – Klabin, Brasilien

Die KPI-Gesamtkosten und Emissionen werden summiert. Die Lieferzeit entspricht dem kritischen Pfad, also der langsamsten der sechs Komponentenketten. Eine Uhr kann erst montiert werden, wenn alle sechs Komponenten verfügbar sind.

## Großer Benchmarkgraph mit 500+ Knoten

Für die erweiterte Demo:

```bash
python scripts/generate_large_network.py
pytest -q
python -m src.main
```

Der Generator nutzt einen festen Seed und erzeugt mindestens 500 Knoten sowie mehrere tausend gerichtete Kanten. Jeder Lieferant erhält mehrere Straßenverbindungen zu Häfen, Flughäfen und Bahnterminals. Die Zusatzknoten sind synthetische Benchmarkdaten und müssen in der Dokumentation ausdrücklich als solche bezeichnet werden.

Die UI zeichnet weiterhin nur die sechs aktuell berechneten Lieferketten. Alle Kanten gleichzeitig darzustellen wäre bei mehreren tausend Kanten unlesbar.
