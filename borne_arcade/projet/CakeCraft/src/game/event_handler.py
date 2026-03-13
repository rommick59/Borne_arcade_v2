import pygame

class eventHandler:
    def __init__(self):
        self._thingToHandle = []

    def add_thing(self, thing):
        if hasattr(thing, "handle_events") and callable(getattr(thing, "handle_events")):
            self._thingToHandle.append(thing)

    def remove_thing(self, thing):
        if thing in self._thingToHandle:
            self._thingToHandle.remove(thing)

    def add_things(self, things):
        for thing in things:
            self.add_thing(thing)

    def remove_things(self, things):
        for thing in things:
            self.remove_thing(thing)

    def handle_events(self):
        for thing in self._thingToHandle:
            thing.handle_events()

    def handle_keydown(self, key):
        for thing in self._thingToHandle:
            if hasattr(thing, "handle_keydown"):
                thing.handle_keydown(key)

    def handle_movement(self, keys, dt: float = 1 / 60):
        for thing in self._thingToHandle:
            if hasattr(thing, "handle_movement"):
                thing.handle_movement(keys, dt)
