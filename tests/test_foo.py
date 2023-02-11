from __future__ import annotations

from py_typed_events import event


class Foo:
    @event
    def on_foo(self, a, b):
        ...


# Should not try to overwrite Foo.on_foo
Foo.on_foo

# When adding multiple listeners, then removing one, it should be the only one removed
# When adding multiple listeners, then one is GCed, it should be the only one removed
# When GC removes a listener, subsequent emit should succeed

# Can be declared and emitted on slotted class using metaclass
