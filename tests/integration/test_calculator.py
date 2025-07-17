import ctypes
import os
import allure
import pytest

lib_path = os.path.join(os.path.dirname(__file__), "../../build/libcalculator.so")
lib = ctypes.CDLL(lib_path)

lib.add_numbers.argtypes = [ctypes.c_double, ctypes.c_double]
lib.add_numbers.restype = ctypes.c_double
lib.sub_numbers.argtypes = [ctypes.c_double, ctypes.c_double]
lib.sub_numbers.restype = ctypes.c_double

@allure.feature("Calculator Integration Tests")
@allure.story("Addition Operation")
@allure.severity(allure.severity_level.NORMAL)
@allure.description("Test the addition functionality of the calculator library with multiple input combinations.")
@pytest.mark.parametrize("a, b, expected", [
       (3, 5, 8),    # Test case 1 - Pozitive numbers
       (0, 0, 0),    # Test case 2 - Zero inputs
       (-2, 3, 1),   # Test case 3 - Negative and positive
       (-1, -4, -5)  # Test case 4 - Negative numbers
   ])
def test_add_numbers(a, b, expected):
    with allure.step(f"Call add({a}, {b}) and verify result"):
        result = lib.add_numbers(a, b)
        assert abs(result - expected) < 1e-10, f"Should be {expected}, but is {result}"

@allure.feature("Calculator Integration Tests")
@allure.story("Subtraction Operation")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.parametrize("a, b, expected", [
       (5, 3, 2), # Test case 1 - Positive numbers
       (10, 10, 0), # Test case 2 - Zero result
       (3, 5, -2), # Test case 3 - Result is negative
       (-1, -4, 3), # Test case 4 - Negative numbers
       (2, -3, 5),  # Test case 5 - Positive and negative
       (0, 0, 0),   # Test case 6 - Both inputs are zero
       (5, 4, 1),   # Test case 7 - Positive numbers
       (0, 0, 0),   # Test case 8 - Both inputs are zero
       (-2, -3, 1)  # Test case 9 - Negative numbers    
   ])
def test_sub_numbers(a, b, expected):
    with allure.step(f"Call subtract({a}, {b}) and verify result"):
        result = lib.sub_numbers(a, b)
        assert abs(result - expected) < 1e-10, f"Should be {expected}, but is {result}"
# End of file: tests/integration/test_calculator.py
