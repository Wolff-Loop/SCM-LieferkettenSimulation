from src.events.war_event import (
    WarEvent
)

from src.scenarios.scenario_manager import (
    ScenarioManager
)


manager = ScenarioManager()

war = WarEvent(
    "China",
    0.8
)

manager.activate_event(
    war
)