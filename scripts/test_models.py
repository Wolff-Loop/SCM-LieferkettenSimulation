from src.simulation.inventory import Inventory
from src.events.war_event import WarEvent
from src.scenarios.scenario_manager import ScenarioManager

inventory = Inventory()

inventory.add_stock("Battery", 100)

print(
    inventory.get_stock_level("Battery")
)

war = WarEvent("China")

manager = ScenarioManager()

manager.activate_event(war)

print("Finished.")