from src.core.application import Application
from src.events.canal_blockage_event import CanalBlockageEvent


def test_asia_europe_sea_route_uses_suez_before_blockage():
    app = Application()
    route = app.calculate_route("port_singapore", "port_rotterdam", "LOWEST_CO2")
    assert "choke_suez" in route["node_ids"]
    assert "choke_cape_good_hope" not in route["node_ids"]


def test_suez_blockage_forces_cape_route_and_increases_distance():
    app = Application()
    baseline = app.calculate_route("port_singapore", "port_rotterdam", "LOWEST_CO2")
    CanalBlockageEvent().apply(app)
    diverted = app.calculate_route("port_singapore", "port_rotterdam", "LOWEST_CO2")
    assert "choke_suez" not in diverted["node_ids"]
    assert "choke_cape_good_hope" in diverted["node_ids"]
    assert diverted["total_distance_km"] > baseline["total_distance_km"]
    assert diverted["total_time_h"] > baseline["total_time_h"]
    assert diverted["total_cost"] > baseline["total_cost"]
