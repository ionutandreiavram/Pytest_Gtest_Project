import ctypes
import os
import allure
import pytest

# Define constants for clarity and maintainability
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
LIB_CONCATENATE_PATH = os.path.join(BASE_DIR, "build", "libconcatenate.so")



@allure.feature("Concatenate Arrays Integration Tests")
@allure.label("tester", "Ionut")
@allure.label("test_type", "integration")
@allure.severity(allure.severity_level.NORMAL)
class TestConcatenateFunctionality:
    """
    A collection of integration tests for the Concatenate_arrays C function,
    using setup_class/teardown_class methods.
    """
    # Class attribute to hold the loaded library
    lib = None

    @classmethod
    def setup_class(self):
        """
        Runs once before any test methods in this class.
        Used to load the shared library.
        """
        print("\n--- Setup (Class): Loading libconcatenate.so ---")
        try:
            self.lib = ctypes.CDLL(LIB_CONCATENATE_PATH)
            self.lib.Concatenate_arrays.argtypes = [ctypes.POINTER(ctypes.c_uint8), 
            ctypes.POINTER(ctypes.c_uint8),
            ctypes.POINTER(ctypes.c_uint16),
            ctypes.c_int]
            self.lib.Concatenate_arrays.restype = None
        except OSError as e:
            pytest.exit(f"Failed to load shared library at {LIB_CONCATENATE_PATH}: {e}. "
                        "Ensure 'libconcatenate.so' is built and in the correct path.")

    @classmethod
    def teardown_class(self):
        """
        Runs once after all test methods in this class have completed.
        Used for any necessary cleanup.
        """
        print("\n --- Teardown (Class): Cleanup for libconcatenate.so ---")
        # For ctypes, explicit unloading is rarely necessary or directly supported.
        # For other resources like files or database connections, close them here.
        self.lib = None # Optionally clear the reference
        
        
    @allure.story("Concatenation Checks")
    @allure.title("Test Concatenation with Various Inputs")
    @allure.description("Verifies the Concatenate_arrays C function correctly combines 8-bit inputs into 16-bit outputs.")
    @pytest.mark.parametrize("input1, input2, ExpectedOutput", [
    ([0x12, 0x13, 0x14, 0x15, 0x16], 
     [0x17, 0x18, 0x19, 0x20, 0xBB], 
     [0x1217, 0x1318, 0x1419, 0x1520, 0x16BB]),
    ([0x17, 0x18, 0x19, 0x20, 0xBB], 
     [0x12, 0x13, 0x14, 0x15, 0x16], 
     [0x1712, 0x1813, 0x1914, 0x2015, 0xBB16]),
    ([],[],[]),
    ([0x00],[0x01],[0x0001])
    ])
    def test_Concatenate_arrays_function(self, input1, input2, ExpectedOutput):
        with allure.step(f"Input1: {input1}, Input2: {input2}, ExpectedOutput: {ExpectedOutput} \n"):
            size = len(input1)
        if size == 0:
            c_input1 = (ctypes.c_uint8 * 0)()
            c_input2 = (ctypes.c_uint8 * 0)()
            c_output = (ctypes.c_uint16 * 0)()
        else:
            c_input1 = (ctypes.c_uint8 * size)(*input1)
            c_input2 = (ctypes.c_uint8 * size)(*input2)
            c_output = (ctypes.c_uint16 * size)()

        self.lib.Concatenate_arrays(c_input1, c_input2, c_output, size)
        actual_output_py = [c_output[i] for i in range(size)]
        with allure.step(f"Asserting Actual Output: {actual_output_py} == Expected Output: {ExpectedOutput}"):
            assert actual_output_py == ExpectedOutput, \
            f"Test failed for basic concatenation. Expected: {ExpectedOutput}, Got: {actual_output_py}"
	
