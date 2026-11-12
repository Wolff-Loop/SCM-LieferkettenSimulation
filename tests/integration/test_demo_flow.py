from src.core.application import Application
from src.events.canal_blockage_event import CanalBlockageEvent


def test_all_six_supply_chains_are_calculated():
    app = Application()
    routes = app.calculate_all_product_routes("LOWEST_CO2")
    assert len(routes) == 6
    assert {route["id"] for route in routes} == {
        "movement", "battery", "glass", "case", "strap", "packaging"
    }


def test_fastest_glass_route_uses_air():
    app = Application()
    route = app.calculate_route("supplier_lens", "factory_heilbronn", "FASTEST")
    assert "airport_shanghai" in route["node_ids"]


def test_lowest_co2_glass_route_uses_sea():
    app = Application()
    route = app.calculate_route("supplier_lens", "factory_heilbronn", "LOWEST_CO2")
    assert "port_singapore" in route["node_ids"]
    assert all(segment["geometry"] for segment in route["segments"])


def test_suez_blockage_reroutes_supply_chains():
    app = Application()
    CanalBlockageEvent().apply(app)
    route = app.calculate_route("supplier_lens", "factory_heilbronn", "LOWEST_CO2")
    assert "port_durban" in route["node_ids"] or "port_hamburg" in route["node_ids"]
