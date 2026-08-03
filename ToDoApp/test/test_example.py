import pytest

def test_equal_or_not_eqaul():
    assert 1 == 1

def test_is_instance():
    assert isinstance(1, int)
    assert isinstance("hello", str)
    assert isinstance([1, 2, 3], list)
    assert isinstance(1, float) is False
    assert isinstance(1.0, float)

def test_boolean():
    assert True is True
    assert False is False
    assert True is not False
    assert False is not True

def test_in():
    assert 1 in [1, 2, 3]
    assert "hello" in ["hello", "world"]
    assert 4 not in [1, 2, 3]
    assert "goodbye" not in ["hello", "world"]

def test_list():
    my_list = [1, 2, 3]
    any_list = [False, False]
    assert len(my_list) == 3
    assert my_list[0] == 1
    assert my_list[-1] == 3
    assert my_list[1:3] == [2, 3]
    assert not any(any_list)  # all elements are False
    assert all(my_list)  # all elements are True (non-zero

def test_type():
    assert type(1) == int
    assert type("hello") == str
    assert type([1, 2, 3]) == list
    assert type(1.0) == float
    assert type(True) == bool

def test_is():
    a = [1, 2, 3]
    b = a
    c = [1, 2, 3]
    assert a is b  # a and b refer to the same object
    assert a is not c  # a and c refer to different objects

def test_not_in():
    assert 1 not in [2, 3, 4]
    assert "hello" not in ["world", "python"]
    assert 5 not in [1, 2, 3, 4]
    assert "goodbye" not in ["hello", "world"]

def test_greater_and_less_than():
    assert 5 > 3
    assert 2 < 4
    assert 10 >= 10
    assert 7 <= 8
    assert not (5 < 3)
    assert not (2 > 4)


class Student:
    def __init__(self, first_name: str, last_name: str, major: str, years: int):
        self.first_name = first_name
        self.last_name = last_name
        self.major = major
        self.years = years

def test_person_init():
    student = Student("John", "Doe", "Computer Science", 3)
    assert student.first_name == "John"
    assert student.last_name == "Doe"
    assert student.major == "Computer Science"
    assert student.years == 3

@pytest.fixture
def student():
    return Student("Jane", "Smith", "Mathematics", 2)

def test_student_fixture(student):
    assert student.first_name == "Jane"
    assert student.last_name == "Smith"
    assert student.major == "Mathematics"
    assert student.years == 2