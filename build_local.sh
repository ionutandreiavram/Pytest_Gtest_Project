#!/bin/bash
     # Set project directory to current working directory
     PROJECT_DIR="$PWD"
     
     # Install system dependencies for build
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
     cd "$PROJECT_DIR" || { echo "Error: Failed to change to $PROJECT_DIR"; exit 1; }

     # Clean build and test results directories
     echo "Cleaning build and test results directories..."
     rm -rf build test_results

     # Create test results directories
     echo "Creating test results directories..."
     mkdir -p test_results/unit test_results/integration
     chmod -R 777 test_results/unit test_results/integration

     # Build project
     echo "Building project..."
     mkdir build
     cd build
     cmake .. || { echo "Error: CMake failed"; exit 1; }
     make || { echo "Error: Make failed"; exit 1; }
     echo "Verifying symbols in libcalculator.so..."
     nm -D libcalculator.so | grep -E " add_numbers|subtract_numbers" || echo "No add_numbers/subtract_numbers symbols found"
     echo "Verifying symbols in libfibonacci.so..."
     nm -D libfibonacci.so | grep fibonacci || echo "No fibonacci symbols found"
     cd ..

     echo "Build completed successfully"
     ls -l build
