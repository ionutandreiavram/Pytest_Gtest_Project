#!/bin/bash

     # Install system dependencies for integration tests
     echo "Installing system dependencies..."
     sudo apt-get update && sudo apt-get install -y \
         python3 \
         python3-pip \
         python3-venv \
         python3-dev \
         libc6-dev \
         libffi-dev \
         default-jre \
         openjdk-17-jre-headless \
         wget || { echo "Error: Failed to install system dependencies"; exit 1; }

     # Find and set JAVA_HOME dynamically
     echo "Setting JAVA_HOME..."
     JAVA_HOME=$(find /usr/lib/jvm -name 'java-17-openjdk-*' -type d | head -n 1)
     if [ -z "$JAVA_HOME" ]; then
         echo "Error: JAVA_HOME could not be set. Java installation not found."
         exit 1
     fi
     export JAVA_HOME
     export PATH=$JAVA_HOME/bin:$PATH
     java -version || { echo "Error: Java not installed correctly"; exit 1; }

     # Install Allure
     echo "Installing Allure..."
     wget https://github.com/allure-framework/allure2/releases/download/2.30.0/allure_2.30.0-1_all.deb
     sudo dpkg -i allure_2.30.0-1_all.deb || sudo apt-get install -f -y
     allure --version || { echo "Error: Allure not installed correctly"; exit 1; }
     rm allure_2.30.0-1_all.deb

     # Clean venv and test results
     echo "Cleaning venv and test results..."
     rm -rf venv test_results/integration allure-report-integration

     # Create test results directory
     echo "Creating test results directory..."
     mkdir -p test_results/integration

     # Verify Python and venv installation
     echo "Verifying Python and venv..."
     python3 --version || { echo "Error: Python3 not installed"; exit 1; }
     python3 -m ensurepip || sudo apt-get install -y python3-venv
     python3 -m venv --help || { echo "Error: python3-venv not installed properly"; exit 1; }

     # Create virtual environment
     echo "Creating virtual environment..."
     python3 -m venv venv
     if [ -d venv ]; then
         echo "Virtual environment created successfully"
     else
         echo "Error: Failed to create virtual environment"
         exit 1
     fi
     source venv/bin/activate
     echo "Virtual environment activated"

     # Install Python dependencies
     echo "Installing Python dependencies..."
     pip install --upgrade pip
     pip install -r requirements.txt --no-cache-dir || { echo "Error: Failed to install Python dependencies"; exit 1; }

     # Verify pytest installation
     echo "Verifying pytest installation..."
     pip show pytest || { echo "Error: pytest not installed"; exit 1; }
     pytest --version || { echo "Error: pytest not found in virtual environment"; exit 1; }

     # Run integration tests
     echo "Running integration tests..."
     if [ -d build ]; then
         export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$PWD/build
         pytest tests/integration/ --alluredir=test_results/integration/allure-results --junitxml=test_results/integration/test_results_pytest.xml --verbose || { echo "Error: Integration tests failed"; exit 1; }
     else
         echo "Error: Build directory not found. Please run build_local.sh first."
         exit 1
     fi

     # Generate Allure report for integration tests
     echo "Generating Allure report for integration tests..."
     chmod -R 755 test_results/integration/allure-results || echo "No allure-results directory, skipping chmod"
     rm -rf allure-report-integration
     allure generate test_results/integration/allure-results -o allure-report-integration --clean
     chmod -R 755 allure-report-integration
     echo "Integration tests Allure report generated:"
     ls -l allure-report-integration

     # Deactivate virtual environment
     deactivate