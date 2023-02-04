from typing import Any, Callable, Concatenate, Generic, ParamSpec, TypeVar, cast
from .event import Event

P = ParamSpec("P")

def event(signature: Callable[Concatenate[Any, P], None]):
    # Lie to the typechecker.
    # In reality, we are returning an `EventDescriptor`.
    # But as soon as anyone tries to access it, it triggers `__get__` and
    # replaces itself with an `Event`.
    # So as far as the consumer is aware, they are *always* dealing with an `Event`.
    return cast(Event[P], EventDescriptor(signature))

class EventDescriptor(Generic[P]):
    """
    This class exists to deal with a pesky problem:
    Python @decorators create a singleton descriptor stored on the class, but we
    need to create a new event emitter per instance.
    This descriptor will do the latter as soon as it's accessed.

    If you want to understand how events work, better to skip this class and look at `Event`.
    """
    __slots__ = ('_attr_name')

    def __init__(self, signature: Callable[Concatenate[Any, P], None]):
        self._attr_name = signature.__name__

    def __get__(self, obj, objtype=None):
        # Create `Event` instance on-demand and attach to the instance.
        event = Event[P]()
        setattr(obj, self._attr_name, event)
        return event
