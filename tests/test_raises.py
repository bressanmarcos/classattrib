import pytest

from classattrib import DynamicClass, SetClassAttribute


def test_no_support_for_class_that_already_has_a_metaclass():
    class Meta(type):
        ...

    class Class(metaclass=Meta):
        ...

    with pytest.raises(ValueError):
        DynamicClass(Class)


def test_set_attribute_in_non_dynamic_class():
    class Class:
        ...

    with pytest.raises(ValueError):
        SetClassAttribute(Class, new_attribute=42)


def test_set_attribute_that_is_not_dynamic():
    @DynamicClass
    class Class:
        attribute = None

    with pytest.raises(AttributeError):
        SetClassAttribute(Class, new_attribute=42)
