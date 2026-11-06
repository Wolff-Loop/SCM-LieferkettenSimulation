import networkx as nx


class GraphBuilder:

    def build(
        self,
        network_data
    ):

        graph = nx.DiGraph()

        all_nodes = (
            network_data["suppliers"]
            + network_data["ports"]
            + network_data["rail_terminals"]
            + network_data["factories"]
        )

        for node in all_nodes:

            graph.add_node(
                node["id"],
                **node
            )

        for edge in network_data["edges"]:

            graph.add_edge(
                edge["source"],
                edge["target"],
                transport_mode=
                edge["transport_mode"],
                distance_km=
                edge["distance_km"],
                status=
                edge["status"]
            )

        return graph