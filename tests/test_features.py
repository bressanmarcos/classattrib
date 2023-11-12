import pytest

from classattrib import DynamicAttribute, DynamicClass, SetClassAttribute


@pytest.fixture
def dynamic_class():
    @DynamicClass
    class MyDynamicClass:
        static = "shared"
        dynamic = DynamicAttribute(None)
        dynamic_no_default = DynamicAttribute()

    return MyDynamicClass


def test_static_attribute_still_works_as_usual(dynamic_class):
    assert dynamic_class.static == "shared"


def test_access_default_value(dynamic_class):
    assert dynamic_class.dynamic == None


def test_access_no_default_value(dynamic_class):
    with pytest.raises(AttributeError):
        dynamic_class.dynamic_no_default


def test_class_attribute_patch_and_rollback(dynamic_class):
    assert dynamic_class.dynamic == None

    with SetClassAttribute(dynamic_class, dynamic=42):
        assert dynamic_class.dynamic == 42

    assert dynamic_class.dynamic == None


def test_class_attribute_nested_patching(dynamic_class):
    assert dynamic_class.dynamic == None

    with SetClassAttribute(dynamic_class, dynamic=42):
        assert dynamic_class.dynamic == 42

        with SetClassAttribute(dynamic_class, dynamic=99):
            assert dynamic_class.dynamic == 99

        assert dynamic_class.dynamic == 42

    assert dynamic_class.dynamic == None

    assert dynamic_class.local == None
