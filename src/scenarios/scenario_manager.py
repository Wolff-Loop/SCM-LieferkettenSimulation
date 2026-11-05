class ScenarioManager:

    def __init__(self):
        self.active_events = []

    def activate_event(self, event):

        event.apply()

        self.active_events.append(event)

    def deactivate_event(self, event):

        event.revert()

        self.active_events.remove(event)