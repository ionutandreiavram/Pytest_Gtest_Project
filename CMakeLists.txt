cmake_minimum_required(VERSION 3.10)
project(CalculatorProject)

enable_testing()
find_package(GTest REQUIRED)
include_directories(${GTEST_INCLUDE_DIRS} include)

# Calulator and Fibonacci libraries
add_library(calculator SHARED src/calculator.c)
add_library(fibonacci SHARED src/fibonacci.c)

add_executable(test_calculator tests/unit/test_calculator.cpp src/calculator.c)
target_link_libraries(test_calculator ${GTEST_LIBRARIES} pthread)

add_test(NAME CalculatorTest COMMAND test_calculator)
