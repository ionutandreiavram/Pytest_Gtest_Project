import ctypes
import os
import allure
import pytest

lib_path = os.path.join(os.path.dirname(__file__), "../../build/libfibonacci.so")
lib = ctypes.CDLL(lib_path)

lib.fibonacci.argtypes = [ctypes.c_uint64]
lib.fibonacci.restype = ctypes.c_uint64

@allure.feature("Fibonacci Integration Tests")
@allure.story("Fibonacci Calculation")
@allure.description("Test the Fibonacci functionality with multiple input combinations.")
@allure.severity(allure.severity_level.NORMAL)
@allure.label("tester", "Ionut")
@allure.label("test_type", "integration")
@pytest.mark.parametrize("n, expected", [
    (0, 0), # Test case 1 -  Fibonacci(0) = 0
    (1, 1), # Test case 2 -  Fibonacci(1) = 1
    (2, 1), # Test case 3 -  Fibonacci(2) = 1
    (3, 2), # Test case 4 -  Fibonacci(3) = 2
    (4, 3), # Test case 5 -  Fibonacci(4) = 3
    (5, 5), # Test case 6 -  Fibonacci(5) = 5
    (6, 8), # Test case 7 -  Fibonacci(6) = 8
    (7, 13), # Test case 8 -  Fibonacci(7) = 13
    (8, 21), # Test case 9 -  Fibonacci(8) = 21
    (9, 34), # Test case 10 -  Fibonacci(9) = 34
    (10, 55), # Test case 11 -  Fibonacci(10) = 55
    (20, 6765), # Test case 12 -  Fibonacci(20) = 6765
    (30, 832040), # Test case 13 -  Fibonacci(30) = 832040
    (50, 12586269025), # Test case 14 -  Fibonacci(50) = 12586269025
    (60, 1548008755920) # Test case 15 -  Fibonacci(60) = 1548008755920

])
def test_fibonacci(n, expected):
    with allure.step(f"Validate input n={n}"):
        allure.attach(f"Input parameter is {n}", name="Input Validation", attachment_type=allure.attachment_type.TEXT)
        assert n>=0, f"Input is {n} and should be positive"
    with allure.step(f"Compute fibonacci({n})"):
        result = lib.fibonacci(n)
        allure.attach(f"Input: n={n}\nExpected: {expected}\nActual: {result}", 
                      name="Test Data", 
                      attachment_type=allure.attachment_type.TEXT)
    with allure.step(f"Verify result for fibonacci({n})"):
        assert result == expected, f"Should be {expected}, but is {result}"

          
