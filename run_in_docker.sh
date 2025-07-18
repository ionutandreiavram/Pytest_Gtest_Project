#!/bin/bash

     # Create Docker container and run build/tests
     docker run --rm -v $(pwd):/calculator_project -w /calculator_project ubuntu:22.04 /bin/bash -c "
         # Install system dependencies
         echo 'Installing system dependencies...'
         apt-get update && apt-get install -y \
             cmake \
             g++ \
             libgtest-dev \
             googletest \
             python3 \
             python3-pip \
             python3-venv \
             python3-dev \
             libc6-dev \
             libffi-dev \
             default-jre \
             openjdk-17-jre-headless \
             wget || { echo 'Error: Failed to install system dependencies'; exit 1; }

         # Find and set JAVA_HOME dynamically
         echo 'Setting JAVA_HOME...'
         JAVA_HOME=\$(find /usr/lib/jvm -name 'java-17-openjdk-*' -type d | head -n 1)
         if [ -z \"\$JAVA_HOME\" ]; then
             echo 'Error: JAVA_HOME could not be set. Java installation not found.'
             exit 1
         fi
         export JAVA_HOME
         export PATH=\$JAVA_HOME/bin:\$PATH
         java -version || { echo 'Error: Java not installed correctly'; exit 1; }

         # Install Allure
         echo 'Installing Allure...'
         wget https://github.com/allure-framework/allure2/releases/download/2.30.0/allure_2.30.0-1_all.deb
         dpkg -i allure_2.30.0-1_all.deb || apt-get install -f -y
         allure --version || { echo 'Error: Allure not installed correctly'; exit 1; }
         rm allure_2.30.0-1_all.deb

         # Build Google Test
         echo 'Building Google Test...'
         cd /usr/src/googletest
         cmake .
         make
         cp lib/*.a /usr/lib/
         cp -r googletest/include/gtest /usr/include/
         cd /calculator_project

         # Clean build and test results directories
         echo 'Cleaning build and test results directories...'
         rm -rf build test_results allure-report-integration

         # Create test results directories
         echo 'Creating test results directories...'
         mkdir -p test_results/unit test_results/integration

         # Build project
         echo 'Building project...'
         mkdir build
         cd build
         cmake .. || { echo 'Error: CMake failed'; exit 1; }
         make || { echo 'Error: Make failed'; exit 1; }
         cd ..

         # Run unit tests with GTest
         echo 'Running unit tests...'
         if [ -f build/test_calculator ]; then
             ./build/test_calculator --gtest_output=xml:test_results/unit/test_results_unit.xml || { echo 'Error: Unit tests failed'; exit 1; }
         else
             echo 'Error: Unit tests executable test_calculator not found'
             exit 1
         fi
         if [ -f test_results/unit/test_results_unit.xml ]; then
             echo 'Unit tests results saved to test_results/unit/test_results_unit.xml:'
             cat test_results/unit/test_results_unit.xml
         else
             echo 'Error: test_results/unit/test_results_unit.xml not generated'
             exit 1
         fi

         # Verify Python and venv installation
         echo 'Verifying Python and venv...'
         python3 --version || { echo 'Error: Python3 not installed'; exit 1; }
         python3 -m ensurepip || apt-get install -y python3-venv
         python3 -m venv --help || { echo 'Error: python3-venv not installed properly'; exit 1; }

         # Create virtual environment
         echo 'Creating virtual environment...'
         python3 -m venv venv
         if [ -d venv ]; then
             echo 'Virtual environment created successfully'
         else
             echo 'Error: Failed to create virtual environment'
             exit 1
         fi
         source venv/bin/activate
         echo 'Virtual environment activated'

         # Install Python dependencies
         echo 'Installing Python dependencies...'
         pip install --upgrade pip
         pip install -r requirements.txt --no-cache-dir || { echo 'Error: Failed to install Python dependencies'; exit 1; }

         # Verify pytest installation
         echo 'Verifying pytest installation...'
         pip show pytest || { echo 'Error: pytest not installed'; exit 1; }
         pytest --version || { echo 'Error: pytest not found in virtual environment'; exit 1; }

         # Run integration tests
         echo 'Running integration tests...'
         export LD_LIBRARY_PATH=\$LD_LIBRARY_PATH:/calculator_project/build
         pytest tests/integration/ --alluredir=test_results/integration/allure-results --junitxml=test_results/integration/test_results_pytest.xml --verbose || { echo 'Error: Integration tests failed'; exit 1; }

         # Generate Allure report for integration tests
         echo 'Generating Allure report for integration tests...'
         chmod -R 755 test_results/integration/allure-results || echo 'No allure-results directory, skipping chmod'
         rm -rf allure-report-integration
         allure generate test_results/integration/allure-results -o allure-report-integration --clean
         chmod -R 755 allure-report-integration
         echo 'Integration tests Allure report generated:'
         ls -l allure-report-integration

         # Deactivate virtual environment
         deactivate
     "