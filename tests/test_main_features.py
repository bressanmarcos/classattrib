import pytest

from dynattrib import SetClassAttribute


def test_wrapper_class_still_behaves_like_the_original(dynamic_class):
    assert dynamic_class.__name__ == "MyDynamicClass"
    assert "MyDynamicClass" in dynamic_class.__qualname__

    obj = dynamic_class()
    assert obj.method() == 42
    assert obj() == 99


def test_static_attribute_still_works_as_usual(dynamic_class):
    assert dynamic_class.static == "shared"


def test_access_default_value(dynamic_class):
    assert dynamic_class.dynamic is None


def test_access_default_factory_value(dynamic_class):
    assert dynamic_class.dynamic_factory == []


def test_access_no_default_value(dynamic_class):
    with pytest.raises(AttributeError):
        dynamic_class.dynamic_no_default


def test_class_attribute_patch_and_rollback(dynamic_class):
    assert dynamic_class.dynamic is None

    with SetClassAttribute(dynamic_class, dynamic=42):
        assert dynamic_class.dynamic == 42

    assert dynamic_class.dynamic is None


def test_class_attribute_nested_patching(dynamic_class):
    assert dynamic_class.dynamic is None

    with SetClassAttribute(dynamic_class, dynamic=42):
        assert dynamic_class.dynamic == 42

        with SetClassAttribute(dynamic_class, dynamic=99):
            assert dynamic_class.dynamic == 99

        assert dynamic_class.dynamic == 42

    assert dynamic_class.dynamic is None


def test_subclass_attribute_takes_precedence_over_parents(dynamic_class):
    class SubClass(dynamic_class):
        ...

    assert dynamic_class.dynamic is None
    assert SubClass.dynamic is None

    with SetClassAttribute(dynamic_class, dynamic=42):
        assert dynamic_class.dynamic == 42
        assert SubClass.dynamic == 42

        with SetClassAttribute(SubClass, dynamic=99):
            assert dynamic_class.dynamic == 42
            assert SubClass.dynamic == 99

        assert dynamic_class.dynamic == 42
        assert SubClass.dynamic == 42

    assert dynamic_class.dynamic is None
    assert SubClass.dynamic is None
