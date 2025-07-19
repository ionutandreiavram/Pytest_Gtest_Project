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
@allure.description("Tests the C Fibonacci function with various valid inputs.\n \
                     Args: \n \
                     n (uint64): The input number for the Fibonacci calculation.\n \
                     expected (uint64): The expected Fibonacci result for 'n'.")
@allure.severity(allure.severity_level.NORMAL)
@allure.label("tester", "Ionut")
@allure.label("test_type", "integration")
@pytest.mark.parametrize("n, expected", [
    (0, 0), # Test case 1 -  Fibonacci(0) = 0
    (1, 0), # Test case 2 -  Fibonacci(1) = 0
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
    (60, 1548008755920), # Test case 15 -  Fibonacci(60) = 1548008755920
    (93, 12200160415121876738), # Test case 16 - Fibonacci(93) = 12200160415121876738 
    (-1, -1) # Test case 17 - Fibonacci(17) = -1
])
def test_fibonacci(n, expected):
    """
    Tests the C Fibonacci function with various valid inputs.

    Args:
        n (uint64): The input number for the Fibonacci calculation.
        expected (uint64): The expected Fibonacci result for 'n'.
    """
    with allure.step(f"Validate input n={n}"):
         allure.attach(f"Input parameter is {n}", name="Input Validation", attachment_type=allure.attachment_type.TEXT)
         if n < 0:
            fibonacci_lib.fibonacci.argtypes = [ctypes.c_int64]
            fibonacci_lib.fibonacci.restype = ctypes.c_int64
         
    with allure.step(f"Compute fibonacci({n})"):
        result = lib.fibonacci(n)
        allure.attach(f"Input: n={n}\nExpected: {expected}\nActual: {result}", 
                      name="Test Data", 
                      attachment_type=allure.attachment_type.TEXT)
                      
    with allure.step(f"Verify result for fibonacci({n})"):
        assert result == expected, f"Result should be {expected}, but is {result}"
        if n<0:
            lib.fibonacci.argtypes = [ctypes.c_uint64]
            lib.fibonacci.restype = ctypes.c_uint64
