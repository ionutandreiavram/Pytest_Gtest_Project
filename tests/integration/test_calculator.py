import ctypes
import os
# Folose?te calea absoluta pentru container sau local
lib_path = os.path.join(os.path.dirname(__file__), "../../build/libcalculator.so")
lib = ctypes.CDLL(lib_path)

lib.add_numbers.argtypes = [ctypes.c_double, ctypes.c_double]
lib.add_numbers.restype = ctypes.c_double
lib.sub_numbers.argtypes = [ctypes.c_double, ctypes.c_double]
lib.sub_numbers.restype = ctypes.c_double

def test_add_numbers():
    result = lib.add_numbers(2,3)
    assert abs(result - 5.0) < 1e-10,  f"Should be 5, but is {result}"

def test_sub_numbers():
    result1 = lib.sub_numbers(5,3)
    result2 = lib.sub_numbers(5,4)
    assert abs(result1 - 2.0) < 1e-10, f"Should be 2, but is {result1}"
    assert abs(result2 - 1.0) < 1e-10, f"Should be 1, but is {result2}"
