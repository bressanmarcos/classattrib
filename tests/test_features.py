import pytest

from classattrib import DynamicAttribute, DynamicClass, SetClassAttribute


@pytest.fixture
def dynamic_class():
    @DynamicClass
    class MyDynamicClass:
        common = "shared"
        local = DynamicAttribute(None)

    return MyDynamicClass


def test_access_default_value(dynamic_class):
    assert dynamic_class.local == None


def test_class_attribute_patch_and_rollback(dynamic_class):
    assert dynamic_class.local == None

    with SetClassAttribute(dynamic_class, local=42):
        assert dynamic_class.local == 42

    assert dynamic_class.local == None


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
