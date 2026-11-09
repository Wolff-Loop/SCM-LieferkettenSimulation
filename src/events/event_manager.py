class EventManager:

    def __init__(self):

        self.active_events = []

    def activate(self, event):

        event.apply()

        self.active_events.append(
            event
        )

    def deactivate(self, event):

        event.revert()

        if event in self.active_events:

            self.active_events.remove(
                event
            )

    def get_active_events(self):

        return self.active_events