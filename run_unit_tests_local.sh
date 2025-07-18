#!/bin/bash

     # Install system dependencies for unit tests
     echo "Installing system dependencies..."
     sudo apt-get update && sudo apt-get install -y \
         cmake \
         g++ \
         libgtest-dev \
         googletest || { echo "Error: Failed to install system dependencies"; exit 1; }

     # Build Google Test
     echo "Building Google Test..."
     cd /usr/src/googletest
     sudo cmake .
     sudo make
     sudo cp lib/*.a /usr/lib/
     sudo cp -r googletest/include/gtest /usr/include/
     cd ~/calculator_project

     # Clean test results
     echo "Cleaning test results..."
     rm -rf test_results/unit

     # Create test results directory
     echo "Creating test results directory..."
     mkdir -p test_results/unit

     # Run unit tests with GTest
     echo "Running unit tests..."
     if [ -f build/test_calculator ]; then
         ./build/test_calculator --gtest_output=xml:test_results/unit/test_results_unit.xml || { echo "Error: Unit tests failed"; exit 1; }
     else
         echo "Error: Unit tests executable 'test_calculator' not found. Please run build_local.sh first."
         exit 1
     fi

     # Verify unit test results
     if [ -f test_results/unit/test_results_unit.xml ]; then
         echo "Unit tests results saved to test_results/unit/test_results_unit.xml:"
         cat test_results/unit/test_results_unit.xml
     else
         echo "Error: test_results/unit/test_results_unit.xml not generated"
         exit 1
     fi

     echo "Unit tests completed. Results displayed above in GTest default format."