import ctypes
import os
import allure
import pytest

lib_path = os.path.join(os.path.dirname(__file__), "../../build/libcalculator.so")
lib = ctypes.CDLL(lib_path)

lib.add.argtypes = [ctypes.c_int, ctypes.c_int]
lib.add.restype = ctypes.c_int
lib.subtract.argtypes = [ctypes.c_int, ctypes.c_int]
lib.subtract.restype = ctypes.c_int

@allure.feature("Calculator Integration Tests")
@allure.story("Addition Calculation")
@allure.description("Test the addition functionality with multiple input combinations.")
@allure.severity(allure.severity_level.NORMAL)
@allure.label("tester", "Ionut")
@allure.label("test_type", "integration")
@pytest.mark.parametrize("a, b, expected", [
    (3, 5, 8),
    (0, 0, 0),
    (-2, 3, 1),
    (-1, -4, -5)
])
def test_add_numbers(a, b, expected):
    with allure.step(f"Validate inputs a={a}, b={b}"):
        allure.attach(f"Inputs: a={a}, b={b}", 
                      name="Input Validation", 
                      attachment_type=allure.attachment_type.TEXT)
    with allure.step(f"Compute {a} + {b}"):
        result = lib.add(a, b)
        allure.attach(f"Inputs: a={a}, b={b}\nExpected: {expected}\nActual: {result}", 
                      name="Test Data", 
                      attachment_type=allure.attachment_type.TEXT)
    with allure.step(f"Verify result for {a} + {b}"):
        assert result == expected, f"Expected {expected}, but got {result}"

@allure.feature("Calculator Integration Tests")
@allure.story("Subtraction Calculation")
@allure.description("Test the subtraction functionality with multiple input combinations.")
@allure.severity(allure.severity_level.NORMAL)
@allure.label("tester", "Ionut")
@allure.label("test_type", "integration")
@pytest.mark.parametrize("a, b, expected", [
    (5, 3, 2),
    (10, 10, 0),
    (3, 5, -2),
    (-1, -4, 3),
    (2, -3, 5),
    (0, 0, 0),
    (5, 4, 1),
    (0, 0, 0),
    (-2, -3, 1)
])
def test_sub_numbers(a, b, expected):
    with allure.step(f"Validate inputs a={a}, b={b}"):
        allure.attach(f"Inputs: a={a}, b={b}", 
                      name="Input Validation", 
                      attachment_type=allure.attachment_type.TEXT)
    with allure.step(f"Compute {a} - {b}"):
        result = lib.subtract(a, b)
        allure.attach(f"Inputs: a={a}, b={b}\nExpected: {expected}\nActual: {result}", 
                      name="Test Data", 
                      attachment_type=allure.attachment_type.TEXT)
    with allure.step(f"Verify result for {a} - {b}"):
        assert result == expected, f"Expected {expected}, but got {result}"
