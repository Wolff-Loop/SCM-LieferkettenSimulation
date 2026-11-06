import json
from pathlib import Path

from PySide6.QtCore import QUrl
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtCore import QObject, Signal, Slot
from PySide6.QtWebChannel import QWebChannel

class MapBridge(QObject):
    clicked = Signal(str, str)          # Art ("node") und Id

    @Slot(str, str)
    def on_map_click(self, art, id_):
        self.clicked.emit(art, id_)

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
    "ENGPASS": "#3D5A80",
}

class WorldMap(QWebEngineView):
    """Weltkarte: Leaflet in einem eingebetteten Web-Fenster."""

    map_clicked = Signal(str, str)

    def __init__(self):
        super().__init__()
        self.setMinimumSize(600, 400)
        self.load(QUrl.fromLocalFile(str(MAP_HTML)))

        self.bridge = MapBridge()
        self.channel = QWebChannel(self)
        self.channel.registerObject("bridge", self.bridge)
        self.page().setWebChannel(self.channel)
        self.bridge.clicked.connect(self.map_clicked)

    def color_for(self, mode):
        return ROUTEN_FARBEN.get(mode, "#8A8178")
    
    def node_color(self, typ):
        return KNOTEN_FARBEN.get(typ, "#8A8178")

    def set_nodes(self, nodes):
        fertig = []
        for n in nodes:
            fertig.append({
                "id": n["name"],
                "name": f'{n["name"]} ({n["typ"]})',
                "lat": n["lat"],
                "lon": n["lon"],
                "color": self.node_color(n["typ"]),
            })
        self.page().runJavaScript(f"setNodes({json.dumps(fertig)});")

    def draw_route(self, coords, mode, route_id=None):
        farbe = self.color_for(mode)
        self.page().runJavaScript(
            f"drawRoute({json.dumps(coords)}, {json.dumps(farbe)}, {json.dumps(route_id)});"
        )

    def clear_routes(self):
        self.page().runJavaScript("clearRoutes();")

    def set_highlights(self, knoten, laender):
        self.page().runJavaScript(
            f"setHighlights({json.dumps(knoten)}, {json.dumps(laender)});"
        )

    def set_shipments(self, sendungen):
        daten = [dict(s, color=self.color_for(s["modus"])) for s in sendungen]
        self.page().runJavaScript(f"setShipments({json.dumps(daten)});")
        