import threading
import weakref

_NoDefault = object()


class DynamicAttribute(threading.local):
    __slots__ = "default", "default_factory"

    def __init__(self, default=_NoDefault, default_factory=None):
        self.default = default
        self.default_factory = default_factory
        if self.default is not _NoDefault and default_factory is not None:
            raise ValueError("Must set only one from `default` and `default_factory`")
        self.values = weakref.WeakKeyDictionary()

    def __set__(self, cls, value):
        self.values[cls] = value

    def __get__(self, cls, metacls):
        if cls is None:
            # When accessed from the MetaClass
            return self

        for s_cls in cls.mro():
            if s_cls in self.values:
                return self.values[s_cls]

        if self.default is not _NoDefault:
            return self.default
        if self.default_factory is not None:
            return self.default_factory()

        raise AttributeError("Attribute value is not set")

    def get_value(self, cls, default=_NoDefault):
        try:
            return self.values[cls]
        except KeyError:
            if default is _NoDefault:
                raise
            return default

    def __delete__(self, cls):
        del self.values[cls]
