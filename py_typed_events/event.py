from __future__ import annotations

from inspect import ismethod
from typing import Any, Callable, Generic, ParamSpec, TypeVar
from weakref import WeakMethod

P = ParamSpec("P")
C = TypeVar("C", bound=Callable)


class Event(Generic[P]):
    """
    Stores (weak) references to zero or more listeners, which are functions
    or methods.

    When emitted, calls each listener in order, passing all parameters.
    """

    __slots__ = ("_listeners",)

    def __init__(self):
        # Note for future: we can save memory by lazily initializing this upon
        # first subscription. See:
        # https://github.com/pyglet/pyglet/blob/d89fa4466d7f5d2183eac91f4ab2bb5fb4db745e/pyglet/event.py#L140-L141

        # Stored as a tuple to optimize for emitting often, rarely changing listeners
        self._listeners: tuple[WeakMethod | Callable, ...] = ()

    def append_listener(self, listener: Callable[P, Any]):
        """
        Subscribe to an event. The listener will be called every time the event is emitted.
        """
        l = WeakMethod(listener, self._remove_weak_method) if ismethod(listener) else listener  # type: ignore
        self._listeners += (l,)
        return self

    __iadd__ = append_listener

    def remove_listener(self, listener: Callable[P, Any]):
        """
        Remove a previously-subscribed event listener.
        """
        # Find the last -- most recently subscribed -- listener and remove it.
        # for i in range(len(self._listeners) - 1, -1, -1):
        for index_reversed, l in enumerate(reversed(self._listeners)):
            l_unwrapped = l() if isinstance(l, WeakMethod) else l
            if l_unwrapped == listener:
                # Found it
                i = len(self._listeners) - index_reversed - 1
                self._listeners = self._listeners[:i] + self._listeners[i + 1 :]
                break
        return self

    __isub__ = remove_listener

    def _remove_weak_method(self, weak_method: WeakMethod) -> object:
        # Very similar to remove_listener, but only used internally in WeakMethod
        # finalizers.  If an instance has subscribed to us, but then is
        # garbage-collected, we remove the subscriptions.
        self._listeners = tuple(l for l in self._listeners if l is not weak_method)

    def emit(self, *args: P.args, **kwargs: P.kwargs) -> None:
        # No docstring so that consumer's declared docstring surfaces.
        for l in self._listeners:
            l_unwrapped = l() if isinstance(l, WeakMethod) else l
            l_unwrapped(*args, **kwargs)  # type: ignore

    __call__ = emit
