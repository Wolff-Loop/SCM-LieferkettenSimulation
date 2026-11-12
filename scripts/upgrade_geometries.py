import json
from pathlib import Path

path = Path("data/routes/geometries.json")
data = json.loads(path.read_text(encoding="utf-8"))

# Suez-Korridor mit bewusst vielen Wegpunkten. Leaflet verbindet jeweils nur
# benachbarte Punkte, deshalb vermeiden diese Koordinaten eine Linie über Land.
data["port_singapore_port_rotterdam"] = {
    "source": "port_singapore", "target": "port_rotterdam",
    "transport_mode": "SHIP", "ui_mode": "SEESCHIFF",
    "geometry": [
        [1.25, 103.70], [2.10, 102.20], [3.30, 100.30], [5.60, 97.10],
        [7.20, 92.00], [7.00, 86.00], [6.20, 81.00], [8.00, 76.00],
        [10.50, 69.00], [12.10, 60.00], [12.20, 52.00], [12.60, 47.00],
        [12.55, 43.50], [15.00, 42.00], [19.00, 39.50], [23.00, 37.00],
        [27.30, 34.20], [29.90, 32.55], [31.30, 32.30], [32.40, 30.00],
        [34.20, 25.00], [35.60, 20.00], [36.50, 14.50], [37.30, 10.00],
        [37.00, 4.00], [36.00, -1.50], [35.95, -5.60], [37.30, -9.20],
        [43.50, -9.80], [48.50, -5.50], [50.10, -2.00], [51.00, 1.00],
        [51.60, 3.00], [51.9244, 4.4777]
    ]
}

# Route um das Kap für die Suez-Sperrung.
data["port_singapore_port_durban"] = {
    "source": "port_singapore", "target": "port_durban",
    "transport_mode": "SHIP", "ui_mode": "SEESCHIFF",
    "geometry": [
        [1.25, 103.70], [-2.0, 99.0], [-6.0, 94.0], [-10.0, 87.0],
        [-14.0, 78.0], [-18.0, 68.0], [-22.0, 58.0], [-25.0, 48.0],
        [-28.0, 39.0], [-29.8587, 31.0218]
    ]
}

data.update({
    "port_singapore_port_hamburg": {
        "source":"port_singapore", "target":"port_hamburg", "transport_mode":"SHIP", "ui_mode":"SEESCHIFF",
        "geometry": data["port_singapore_port_rotterdam"]["geometry"][:-3] + [[51.2, 2.0], [52.5, 5.0], [53.5511, 9.9937]]
    },
    "port_hamburg_rail_heilbronn": {
        "source":"port_hamburg", "target":"rail_heilbronn", "transport_mode":"RAIL", "ui_mode":"ZUG",
        "geometry":[[53.5511,9.9937],[52.37,9.73],[51.31,9.49],[50.11,8.68],[49.49,8.47],[49.1427,9.2109]]
    },
    "supplier_lens_airport_shanghai": {
        "source":"supplier_lens", "target":"airport_shanghai", "transport_mode":"TRUCK", "ui_mode":"LKW",
        "geometry":[[28.2282,113.002],[29.7,118.3],[30.4,120.6],[31.1443,121.8083]]
    },
    "airport_shanghai_airport_frankfurt": {
        "source":"airport_shanghai", "target":"airport_frankfurt", "transport_mode":"AIR", "ui_mode":"FLUGZEUG",
        "geometry":[[31.1443,121.8083],[42,95],[48,65],[52,35],[50.0379,8.5622]]
    },
    "airport_frankfurt_factory_heilbronn": {
        "source":"airport_frankfurt", "target":"factory_heilbronn", "transport_mode":"TRUCK", "ui_mode":"LKW",
        "geometry":[[50.0379,8.5622],[49.7,8.65],[49.4,8.9],[49.1427,9.2187]]
    }
})

path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
print("geometries.json aktualisiert: maritime Routen verlaufen über Wasser")
