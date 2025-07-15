import ctypes
import os
import allure

lib_path = os.path.join(os.path.dirname(__file__), "../../build/libcalculator.so")
lib = ctypes.CDLL(lib_path)

lib.add_numbers.argtypes = [ctypes.c_double, ctypes.c_double]
lib.add_numbers.restype = ctypes.c_double
lib.sub_numbers.argtypes = [ctypes.c_double, ctypes.c_double]
lib.sub_numbers.restype = ctypes.c_double

@allure.feature("Calculator Integration Tests")
@allure.story("Addition Operation")
@allure.severity(allure.severity_level.NORMAL)
def test_add_numbers():
    with allure.step("Call add(2, 3) and verify result"):
        result = lib.add_numbers(2,3)
        assert abs(result - 5.0) < 1e-10,  f"Should be 5, but is {result}"

@allure.feature("Calculator Integration Tests")
@allure.story("Subtraction Operation")
@allure.severity(allure.severity_level.NORMAL)
def test_sub_numbers():
    with allure.step("Call subtract(5, 3) and verify result"):
        result1 = lib.sub_numbers(5,3)
        assert abs(result1 - 2.0) < 1e-10, f"Should be 2, but is {result1}"
    with allure.step("Call subtract(5, 4) and verify result"):
        result2 = lib.sub_numbers(5,4)
        assert abs(result2 - 1.0) < 1e-10, f"Should be 1, but is {result2}"
