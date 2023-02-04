from __future__ import annotations
from inspect import ismethod

from typing import Any, Callable, Generic, ParamSpec, TypeVar
from functools import partial
from weakref import WeakMethod

P = ParamSpec("P")
C = TypeVar("C", bound=Callable)

class Event(Generic[P]):
    """
    Stores (weak) references to zero or more subscribers, which are functions
    or methods.

    When emitted, calls each subscriber in order, passing all parameters.
    """

    __slots__ = ('_subscribers',)

    def __init__(self):
        # Note for future: we can save memory by lazily initializing this upon
        # first subscription. See:
        # https://github.com/pyglet/pyglet/blob/d89fa4466d7f5d2183eac91f4ab2bb5fb4db745e/pyglet/event.py#L140-L141
        self._subscribers: list[WeakMethod | Callable] = []

    def append_listener(self, handler: Callable[P, Any]):
        return self.__iadd__(handler)

    def __iadd__(self, handler: Callable[P, Any]):
        subscription = WeakMethod(handler, self._remove_weak_method) if ismethod(handler) else handler # type: ignore
        self._subscribers.append(subscription)
        return self

    def remove_listener(self, handler: Callable[P, Any]):
        return self.__isub__(handler)

    def __isub__(self, handler: Callable[P, Any]):
        # Iterate over a copy as we might mutate the list
        for subscription in list(self._subscribers):
            try:
                if isinstance(subscription, WeakMethod):
                    if subscription() == handler:
                        self._subscribers.remove(subscription)
                        break
                else:
                    if subscription == handler:
                        self._subscribers.remove(subscription)
                        break
            except TypeError:
                # weakref is already dead
                pass
        return self

    def _remove_weak_method(self, weak_method: WeakMethod) -> object:
        """
        Very similar to __isub__, but only used internally in WeakMethod
        finalizers.  If an instance has subscribed to us, but then is
        garbage-collected, we remove the subscriptions.
        """
        for subscription in list(self._subscribers):
            try:
                if weak_method == subscription:
                    self._subscribers.remove(weak_method)
                    return
            except TypeError:
                # weakref is already dead
                pass

    def emit(self, *args: P.args, **kwargs: P.kwargs) -> None:
        for subscription in self._subscribers:
            # Unwrap WeakMethod
            handler = subscription() if isinstance(subscription, WeakMethod) else subscription
            handler(*args, **kwargs) # type: ignore

    def __call__(self, *args: P.args, **kwargs: P.kwargs) -> None:
        self.emit(*args, **kwargs)