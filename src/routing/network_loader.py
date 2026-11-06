import json
from pathlib import Path


class NetworkLoader:

    def __init__(self):

        self.data_path = (
            Path(__file__)
            .resolve()
            .parents[2]
            / "data"
        )

    def load_json(self, filepath):

        with open(
            filepath,
            "r",
            encoding="utf-8"
        ) as file:

            return json.load(file)

    def load_network_data(self):

        return {

            "suppliers":
                self.load_json(
                    self.data_path /
                    "nodes" /
                    "suppliers.json"
                ),

            "ports":
                self.load_json(
                    self.data_path /
                    "nodes" /
                    "ports.json"
                ),

            "rail_terminals":
                self.load_json(
                    self.data_path /
                    "nodes" /
                    "rail_terminals.json"
                ),

            "factories":
                self.load_json(
                    self.data_path /
                    "nodes" /
                    "factories.json"
                ),

            "edges":
                self.load_json(
                    self.data_path /
                    "routes" /
                    "edges.json"
                ),

            "transport_modes":
                self.load_json(
                    self.data_path /
                    "routes" /
                    "transport_modes.json"
                )
        }