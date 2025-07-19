cmake_minimum_required(VERSION 3.10)
project(CalculatorProject C CXX)

enable_testing()
find_package(GTest REQUIRED)
include_directories(${GTEST_INCLUDE_DIRS} include)

# Ensure symbols are exported
set(CMAKE_C_VISIBILITY_PRESET default)
set(CMAKE_CXX_VISIBILITY_PRESET default)
set(CMAKE_VISIBILITY_INLINES_HIDDEN OFF)

# C libraries
add_library(calculator SHARED src/calculator.c)
add_library(fibonacci SHARED src/fibonacci.c)
add_library(concatenate SHARED src/concatenate.c)

# Set output directory for libraries
set_target_properties(calculator fibonacci PROPERTIES
    LIBRARY_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}")

# Debug symbols
add_custom_command(TARGET calculator POST_BUILD
    COMMAND nm -D ${CMAKE_BINARY_DIR}/libcalculator.so | grep -E " add|subtract" || echo "No add/subtract symbols in libcalculator.so"
    COMMAND nm -D ${CMAKE_BINARY_DIR}/libfibonacci.so | grep fibonacci || echo "No fibonacci symbols in libfibonacci.so"
    COMMAND nm -D ${CMAKE_BINARY_DIR}/libconcatenate.so | grep Concatenate || echo "No Concatenate symbols in libconcatenate.so"
)

# Unit test executable
add_executable(test_calculator tests/unit/test_calculator.cpp src/calculator.c)
target_link_libraries(test_calculator ${GTEST_LIBRARIES} pthread)

add_test(NAME CalculatorTest COMMAND test_calculator)
