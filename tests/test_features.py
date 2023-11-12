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


def test_class_attribute_nested_patching(dynamic_class):
    assert dynamic_class.local == None

    with SetClassAttribute(dynamic_class, local=42):
        assert dynamic_class.local == 42

        with SetClassAttribute(dynamic_class, local=99):
            assert dynamic_class.local == 99

        assert dynamic_class.local == 42

    assert dynamic_class.local == None
