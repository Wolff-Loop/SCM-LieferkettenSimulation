from src.routing.network_loader import (
    NetworkLoader
)

from src.routing.graph_builder import (
    GraphBuilder
)

from src.routing.routing_engine import (
    RoutingEngine
)


network_data = (
    NetworkLoader()
    .load_network_data()
)

graph = (
    GraphBuilder()
    .build(network_data)
)

print(
    f"Nodes: "
    f"{graph.number_of_nodes()}"
)

print(
    f"Edges: "
    f"{graph.number_of_edges()}"
)

route = (
    RoutingEngine(graph)
    .find_route(
        "supplier_lens",
        "factory_heilbronn"
    )
)

print(route)