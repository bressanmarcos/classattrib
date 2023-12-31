import pytest

from dynattrib import DynamicAttribute, DynamicClass


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
        
        def __call__(self):
            return 99

    return MyDynamicClass
