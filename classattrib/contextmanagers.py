from .descriptors import DynamicAttribute


class SetClassAttribute:
    def __init__(self, cls, **kw_attributes):
        meta = type(cls)

        if not hasattr(meta, "__dynamicclass__"):
            raise ValueError("Only works for dynamic classes")

        for attribute in kw_attributes:
            descriptor = getattr(meta, attribute, None)
            if descriptor is None:
                raise AttributeError(
                    f"`{attribute}` must be a {DynamicAttribute.__name__} descriptor"
                )

        self.cls = cls
        self.kw_attributes = kw_attributes

    def __enter__(self):
        for attribute, value in self.kw_attributes.items():
            setattr(self.cls, attribute, value)

    def __exit__(self, exc_type, exc_value, exc_traceback):
        for attribute in self.kw_attributes:
            delattr(self.cls, attribute)
