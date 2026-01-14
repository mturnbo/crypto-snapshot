from app.utils.utils import show_object_values


class ExampleObject:
    def __init__(self):
        self.name = "TestName"
        self.value = "TestValue"


def test_show_object_values_with_standard_object(capsys):
    obj = ExampleObject()
    show_object_values(obj)
    captured = capsys.readouterr()
    assert "ExampleObject Object Attributes" in captured.out
    assert "name" in captured.out
    assert "TestName" in captured.out
    assert "value" in captured.out
    assert "TestValue" in captured.out


def test_show_object_values_with_empty_object(capsys):
    class EmptyObject:
        pass

    obj = EmptyObject()
    show_object_values(obj)
    captured = capsys.readouterr()
    assert "EmptyObject Object Attributes" in captured.out
    assert "Key" in captured.out
    assert "Value" in captured.out
    assert "No data" in captured.out or obj.__dict__ == {}


def test_show_object_values_with_nested_object(capsys):
    class NestedObject:
        def __init__(self):
            self.sub_object = ExampleObject()

    obj = NestedObject()
    show_object_values(obj)
    captured = capsys.readouterr()
    assert "NestedObject Object Attributes" in captured.out
    assert "sub_object" in captured.out
    assert "ExampleObject" in captured.out
