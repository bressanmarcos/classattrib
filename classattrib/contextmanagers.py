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
        self.old_kw_attributes = {}

    def __enter__(self):
        meta = type(self.cls)

        for attribute, value in self.kw_attributes.items():
            descriptor = getattr(meta, attribute)

            try:
                old_cls_specific_value = descriptor.get_value(self.cls)
            except KeyError:
                pass
            else:
                self.old_kw_attributes[attribute] = old_cls_specific_value

            setattr(self.cls, attribute, value)

    def __exit__(self, exc_type, exc_value, exc_traceback):
        for attribute in self.kw_attributes:
            if attribute in self.old_kw_attributes:
                old_value = self.old_kw_attributes[attribute]
                setattr(self.cls, attribute, old_value)
            else:
                delattr(self.cls, attribute)
