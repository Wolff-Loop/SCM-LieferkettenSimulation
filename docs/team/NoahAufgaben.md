# Person 2 - Deliverables

## Ziel

Bereitstellung der vollständigen Simulations- und Szenariologik.

---

# D1 - Produktmodell

Implementierte Klassen:

```python
Product

Component

Order
```

Muss ermöglichen:

```python
create_product()

create_order()
```

---

# D2 - Shipment System

Implementierte Klasse:

```python
Shipment
```

Attribute:

```python
origin

destination

route

quantity

current_location

status
```

Statuswerte:

```python
PREPARING

IN_TRANSIT

DELAYED

DELIVERED

CANCELLED
```

---

# D3 - Inventory System

Implementierte Klasse:

```python
Inventory
```

Funktionen:

```python
add_stock()

remove_stock()

reserve_stock()

release_stock()

get_stock_level()
```

---

# D4 - Simulation Engine

Implementierte Klasse:

```python
SimulationEngine
```

Funktionen:

```python
start()

pause()

resume()

step()

reset()

stop()
```

---

# D5 - Event System

Basisklasse:

```python
Event
```

Abgeleitete Klassen:

```python
WarEvent

StrikeEvent

FloodEvent

EarthquakeEvent

SupplierFailureEvent

DemandSpikeEvent

FuelPriceShockEvent

CanalBlockageEvent
```

---

# D6 - Scenario Manager

Implementierte Klasse:

```python
ScenarioManager
```

Funktionen:

```python
create_scenario()

save_scenario()

load_scenario()

activate_scenario()

deactivate_scenario()
```

---

# D7 - KPI Engine

Implementierte Klasse:

```python
KPIEngine
```

Berechnet:

```python
total_cost

transport_cost

lead_time

co2_emissions

service_level

risk_score

network_utilization
```

---

# Erfolgsdefinition

Folgender Aufruf funktioniert:

```python
scenario_manager.activate(
    "China War"
)
```

und erzeugt:

```python
updated KPIs

updated shipments

updated network status
```