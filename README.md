# py_typed_events

Type-hinted events for python, inspired by C# events and delegates.

## Features

- Describe events as decorated methods, similar to `@property`
- Add and remove subscriptions with `+=` and `-=`, like C# events.
  - `emitter.on_event += self.respond_to_event`
- Subscribed methods are weakly held.
  - Subscribed instances will garbage collect automatically without needing to remove all their subscriptions.
- Type hinting, typechecking, and docstring support.
  - F2 to rename an event will rename it everywhere.
  - Typechecker will verify that you pass the correct args to `.emit()`.
  - Typechecker will verify that subscribers accept the correct args.
<!--
  - Hovering over an event will show the docstring.
  - Typechecker can remind you when your event subscription is incompatible.
  with the event.
-->

## Usage

For a complete example, see [`examples/example.py`](examples/example.py)

```python
class Emitter:
    # Events are declared by decorating an abstract, *empty* method.
    # This method declares the event signature.
    @event
    def on_change(self, old_value: str, new_value: str): ...

class Observer:
    def __init__(self, emitter: Emitter):
        emitter.on_change += self.log_change

    def log_change(self, old_value: str, new_value: str):
        print(f"Value changed from \"{old_value}\" to \"{new_value}\"")

emitter = Emitter()
observer = Observer(emitter)
# Emit with `.emit` or as bare call
emitter.on_change.emit('old', 'new')
emitter.on_change('old', 'new')
```

## Installation

Not (yet) published to PyPi, so install directly from git using your preferred
package manager.  For example, with `pip`:

```python
pip install git+https://github.com/cspotcode/py_typed_events.git
```

## Development

Build script uses `just`: https://github.com/casey/just

Read `justfile` for details.
