from src import event

class Emitter:
    def __init__(self):
        self._value = ''

    # Events are declared by decorating an abstract, *empty* method.
    # This declares the event signature, it is never executed!
    @event
    def on_change(self, old_value: str, new_value: str):
        """
        Emitted every time the `value` changes, passing both old and new values.
        """

    @property
    def value(self) -> str:
        return self._value
    
    @value.setter
    def value(self, new_value: str):
        old_value = self._value
        self._value = new_value
        # Broadcast every time this value changes.
        self.on_change.emit(old_value, new_value)

class Observer:
    def __init__(self, name: str):
        self.name = name

    def log_change(self, old_value: str, new_value: str):
        print(f"Observer {self.name}: Value changed from \"{old_value}\" to \"{new_value}\"")

###################

emitter = Emitter()
observer_a = Observer('A')
observer_b = Observer('B')

# Subscribe to events with +=, unsubscribe with -=
emitter.on_change += observer_a.log_change
emitter.on_change += observer_b.log_change

# Change the value, broadcasting the event to all listeners:
emitter.value = 'Hello'
# Both observers will log: Value changed from "" to "Hello"

emitter.value = 'World'
# Both observers will log: Value changed from "Hello" to "World"

# Explicitly unsubscribe observer_a
emitter.on_change -= observer_a.log_change

emitter.value = "change again, logged by B but not A"

# Garbage-collect observer_b
# Subscriptions are automatically removed
observer_b = None

emitter.value = "change again, not logged by either observer"
