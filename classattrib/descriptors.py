_NoDefault = object()


class DynamicAttribute:
    def __init__(self, default=_NoDefault):
        self.default = default
        self.value = {}

    def __set__(self, cls, value):
        self.value[cls] = value

    def __get__(self, cls, metacls):
        if cls is None:
            # When accessed from the MetaClass
            return self

        for s_cls in cls.mro():
            if s_cls in self.value:
                return self.value[s_cls]

        if self.default is not _NoDefault:
            return self.default

        raise AttributeError("Attribute value is not set")

    def get_value(self, cls, default=_NoDefault):
        try:
            return self.value[cls]
        except KeyError:
            if default is _NoDefault:
                raise
            return default

    def __delete__(self, cls):
        del self.value[cls]
