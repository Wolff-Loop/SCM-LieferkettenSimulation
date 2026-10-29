# Person 3 - Deliverables

## Ziel

Bereitstellung der vollständigen Desktop-Anwendung inklusive Visualisierung.

---

# D1 - Hauptanwendung

Datei:

```text
main.py
```

Startet die gesamte Anwendung.

---

# D2 - Hauptfenster

Implementierte Klasse:

```python
MainWindow
```

Enthält:

- Karte
- Dashboard
- Steuerung
- Szenariomanager

---

# D3 - Weltkarte

Implementierte Klasse:

```python
WorldMap
```

Muss anzeigen:

```text
Lieferanten

Fabriken

Häfen

Flughäfen

Terminals

Lager
```

---

# D4 - Routendarstellung

Visualisiert:

```text
Schiff

LKW

Bahn

Flugzeug

Binnenschiff
```

Farbcodierung:

```text
Blau = Schiff

Rot = LKW

Grün = Bahn

Gelb = Flugzeug

Türkis = Binnenschiff
```

---

# D5 - Dashboard

Zeigt in Echtzeit:

```text
Gesamtkosten

Transportkosten

CO₂

Lieferzeit

Risikoscore

Service Level
```

---

# D6 - Routingsteuerung

Der Benutzer kann wählen:

```text
FASTEST

CHEAPEST

LOWEST_CO2

MOST_RESILIENT
```

---

# D7 - Szenariosteuerung

Der Benutzer kann aktivieren:

```text
Krieg

Streik

Naturkatastrophe

Lieferantenausfall

Suezkanal Blockade

Nachfrageanstieg
```

---

# D8 - Simulation Controls

Bedienelemente:

```text
Start

Pause

Reset

Stop
```

---

# D9 - EXE Build

Erzeugung einer lauffähigen Anwendung:

```text
SupplyChainDigitalTwin.exe
```

Die Anwendung muss auf einem Windows-System ohne Entwicklungsumgebung startbar sein.

---

# Erfolgsdefinition

Ein Benutzer kann:

1. Die EXE starten
2. Die Weltkarte sehen
3. Eine Routingstrategie auswählen
4. Ein Szenario aktivieren
5. KPI-Änderungen beobachten
6. Die Simulation steuern