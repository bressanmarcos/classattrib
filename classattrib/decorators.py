from .descriptors import DynamicAttribute


def DynamicClass(cls):
    if type(cls) is not type:
        raise ValueError(f"Class type is not `type`")

    class DynamicClassMeta(type):
        __dynamicclass__ = True

    class NewClass(metaclass=DynamicClassMeta):
        ...

    attributes_to_skip = ["__dict__", "__weakref__"]

    for attribute, value in vars(cls).items():
        if attribute in attributes_to_skip:
            continue
        if isinstance(value, DynamicAttribute):
            setattr(DynamicClassMeta, attribute, value)
        else:
            setattr(NewClass, attribute, value)

    return NewClass
