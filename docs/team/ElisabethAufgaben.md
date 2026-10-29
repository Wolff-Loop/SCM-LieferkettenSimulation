# Person 1 - Deliverables

## Ziel

Bereitstellung eines vollständigen globalen Transportnetzwerks inklusive Routing.

---

# D1 - Länderdaten

Datei:

countries.json

Inhalt:

- Länder
- Risikoindex
- Kriegsstatus
- Sanktionen

Beispiel:

```json
{
  "name": "China",
  "risk_score": 2.3,
  "war_status": false,
  "sanctioned": false
}
```

---

# D2 - Netzwerkobjekte

Implementierte Klassen:

```python
Country
Node
Supplier
Factory
Warehouse
Port
Airport
RailTerminal
```

Jeder Knoten besitzt mindestens:

```python
id
name
country
latitude
longitude
active
```

---

# D3 - Transportverbindungen

Datei:

edges.json

Inhalt:

```json
{
  "from": "Shanghai Port",
  "to": "Rotterdam Port",
  "transport_mode": "SHIP",
  "distance": 19200,
  "cost": 5000,
  "co2": 1200,
  "lead_time": 28
}
```

Attribute:

- Start
- Ziel
- Transportart
- Distanz
- Kosten
- CO₂
- Dauer
- Risiko
- Kapazität

---

# D4 - Supply Chain Graph

Implementierte Klasse:

```python
SupplyChainGraph
```

Verfügbare Funktionen:

```python
load_network()

add_node()

remove_node()

add_edge()

remove_edge()

disable_node()

disable_edge()

enable_node()

enable_edge()
```

---

# D5 - Routing Engine

Implementierte Klasse:

```python
RoutingEngine
```

Unterstützte Strategien:

```python
FASTEST
CHEAPEST
LOWEST_CO2
MOST_RESILIENT
```

Verfügbare Funktionen:

```python
calculate_route()

find_fastest_route()

find_cheapest_route()

find_greenest_route()

find_resilient_route()
```

---

# Erfolgsdefinition

Folgender Aufruf funktioniert:

```python
route = routing.calculate_route(
    source="Lens Technology",
    destination="Watch Factory Heilbronn",
    strategy="FASTEST"
)
```

Ergebnis:

```python
Route
```

mit:

```python
nodes
cost
distance
lead_time
co2
risk
```