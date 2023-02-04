# py_typed_events

Type-hinted events for python, inspired by C# events and delegates.

```python
class Foo:
    def __init__(self):
        self._value = ''

    # Events are declared by decorating an abstract, *empty* method.
    # This method declares the event signature.
    @event
    def on_change(self, old_value: str, new_value: str): ...

    @property
    def value(self):
        return self._value
    
    @value.setter
    def set_value(self, new_value: str):
        old_value = self._value
        self._value = new_value
        self.on_change.emit(old_value, new_value)

class Bar:
    def __init__(self, listen_to: Foo):
        # Subscribe to events with +=, unsubscribe with -=
        listen_to.on_change += self.log_change

    def log_change(self, old_value: str, new_value: str):
        print(f"Value changed from \"{old_value}\" to \"{new_value}\"")

foo = Foo()
bar = Bar(foo)
foo.value = 'Hello'
# logs 
foo.value = 'World'
```

## Development

Build script uses `just`: https://github.com/casey/just

Read `justfile` for details.
