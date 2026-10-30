import json
from pathlib import Path

from PySide6.QtCore import QUrl
from PySide6.QtWebEngineWidgets import QWebEngineView

MAP_HTML = Path(__file__).parent / "map" / "map.html"

# Farben der Verkehrsträger laut Aufgabenliste (Namen ggf. an enums.py anpassen)
ROUTEN_FARBEN = {
    "SEESCHIFF": "#1f5fbf",
    "LKW": "#c0392b",
    "ZUG": "#2e8b57",
    "FLUGZEUG": "#e0b000",
    "BINNENSCHIFF": "#2bb5b0",
}

KNOTEN_FARBEN = {
    "LIEFERANT": "#2E2C2A",
    "FABRIK": "#9C7F5B",
    "HAFEN": "#6C5B9E",
    "FLUGHAFEN": "#D77FA1",
    "TERMINAL": "#8A8178",
    "LAGER": "#7A8F3A",
}

class WorldMap(QWebEngineView):
    """Weltkarte: Leaflet in einem eingebetteten Web-Fenster."""

    def __init__(self):
        super().__init__()
        self.setMinimumSize(600, 400)
        self.load(QUrl.fromLocalFile(str(MAP_HTML)))

    def color_for(self, mode):
        return ROUTEN_FARBEN.get(mode, "#8A8178")
    
    def node_color(self, typ):
        return KNOTEN_FARBEN.get(typ, "#8A8178")

    def set_nodes(self, nodes):
        fertig = []
        for n in nodes:
            fertig.append({
                "name": f'{n["name"]} ({n["typ"]})',
                "lat": n["lat"],
                "lon": n["lon"],
                "color": self.node_color(n["typ"]),
            })
        self.page().runJavaScript(f"setNodes({json.dumps(fertig)});")

    def draw_route(self, coords, mode):
        farbe = self.color_for(mode)
        self.page().runJavaScript(
            f"drawRoute({json.dumps(coords)}, {json.dumps(farbe)});"
        )

    def clear_routes(self):
        self.page().runJavaScript("clearRoutes();")