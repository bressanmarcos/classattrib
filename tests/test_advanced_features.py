import threading

from classattrib import SetClassAttribute, DynamicAttribute, DynamicClass


def test_saved_value_for_class_attribute_is_garbage_collected_with_class(dynamic_class):
    """If for some reason the class ceases to exist while it has
    defined attributes, we need to make sure their values are also
    gc'ed."""

    class SubClass(dynamic_class):
        ...

    SetClassAttribute(SubClass, dynamic=42).__enter__()
    del SubClass
    import gc

    gc.collect()

    meta = type(dynamic_class)
    descriptor = meta.dynamic
    assert len(descriptor.values) == 0


def launch_in_thread(func):
    class ThreadWithException(threading.Thread):
        def __init__(self):
            super().__init__(name=func.__name__)
            self.raised_exception = None

        def run(self):
            try:
                func()
            except BaseException as e:
                self.raised_exception = e
                raise

    thread = ThreadWithException()
    thread.start()
    thread.join()

    if thread.raised_exception:
        raise thread.raised_exception


def test_dynamic_attribute_values_are_not_shared_among_threads(dynamic_class):
    assert dynamic_class.dynamic is None

    with SetClassAttribute(dynamic_class, dynamic=42):
        assert dynamic_class.dynamic == 42

        def thread_function():
            assert dynamic_class.dynamic is None

            with SetClassAttribute(dynamic_class, dynamic=99):
                assert dynamic_class.dynamic == 99

            assert dynamic_class.dynamic is None

        launch_in_thread(thread_function)

        assert dynamic_class.dynamic == 42

    assert dynamic_class.dynamic is None
