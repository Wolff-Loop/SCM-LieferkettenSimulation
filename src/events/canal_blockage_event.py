from src.events.graph_events import NodeStatusEvent


class CanalBlockageEvent(NodeStatusEvent):
    """Deaktiviert den physischen Suez-Knoten.

    Alle Europa-Routen über Suez hängen von diesem Knoten ab. Nach Sperrung
    bleibt nur die längere Kaproute über `choke_cape_good_hope` verfügbar.
    """

    def __init__(self):
        super().__init__("Suezkanal-Blockade", "Suezkanal", 1.0)
