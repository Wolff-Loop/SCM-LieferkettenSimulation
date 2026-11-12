class EventManager:
    def __init__(self, application):
        self.application = application
        self.active_events = {}

    @staticmethod
    def key(name, target=None):
        return name, target

    def activate(self, event):
        key = self.key(event.name, event.target)
        if key not in self.active_events:
            event.apply(self.application)
            self.active_events[key] = event

    def deactivate(self, name, target=None):
        key = self.key(name, target)
        event = self.active_events.pop(key, None)
        if event:
            event.revert(self.application)

    def clear(self):
        for event in list(self.active_events.values()):
            event.revert(self.application)
        self.active_events.clear()

    def get_active_events(self):
        return list(self.active_events.values())

    def is_active(self, name, target=None):
        return self.key(name, target) in self.active_events
