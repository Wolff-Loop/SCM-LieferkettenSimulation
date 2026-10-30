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


class WorldMap(QWebEngineView):
    """Weltkarte: Leaflet in einem eingebetteten Web-Fenster."""

    def __init__(self):
        super().__init__()
        self.setMinimumSize(600, 400)
        self.load(QUrl.fromLocalFile(str(MAP_HTML)))

    def color_for(self, mode):
        return ROUTEN_FARBEN.get(mode, "#8A8178")

    def set_nodes(self, nodes):
        self.page().runJavaScript(f"setNodes({json.dumps(nodes)});")

    def draw_route(self, coords, mode):
        farbe = self.color_for(mode)
        self.page().runJavaScript(
            f"drawRoute({json.dumps(coords)}, {json.dumps(farbe)});"
        )

    def clear_routes(self):
        self.page().runJavaScript("clearRoutes();")