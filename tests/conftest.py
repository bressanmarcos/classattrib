import pytest

from classattrib import DynamicAttribute, DynamicClass


@pytest.fixture
def dynamic_class():
    @DynamicClass
    class MyDynamicClass:
        static = "shared"
        dynamic = DynamicAttribute(None)
        dynamic_no_default = DynamicAttribute()
        dynamic_factory = DynamicAttribute(default_factory=list)

        def method(self):
            return 42

    return MyDynamicClass
