# src/simulation/simulation_engine.py

from src.analytics.kpi_engine import KPIEngine


class SimulationEngine:

    def __init__(self, event_manager):

        self.event_manager = event_manager

        self.kpi_engine = KPIEngine()

        self.current_day = 0

        self.running = False

        self.strategy = "FASTEST"

    def start(self):

        self.running = True

    def pause(self):

        self.running = False

    def stop(self):

        self.running = False

    def reset(self):

        self.current_day = 0

        self.running = False

    def step(self):

        if not self.running:
            return

        self.current_day += 1

    def set_strategy(
        self,
        strategy: str
    ):

        self.strategy = strategy

    def get_current_day(self):

        return self.current_day

    def get_active_event_count(self):

        return len(
            self.event_manager
            .get_active_events()
        )

    def get_snapshot(self):

        active_event_count = (
            self.get_active_event_count()
        )

        kpis = (
            self.kpi_engine
            .calculate(active_event_count)
        )

        kpis["day"] = (
            self.current_day
        )

        kpis["strategy"] = (
            self.strategy
        )

        return kpis