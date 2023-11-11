_NoDefault = object()


class DynamicAttribute:
    def __init__(self, default=_NoDefault):
        self.default = default
        self.value = default

    def __set__(self, cls, value):
        self.value = value

    def __get__(self, cls, metacls):
        if cls is None:
            # When accessed from the MetaClass
            return self
        return self.value

    def __delete__(self, cls):
        self.value = self.default
