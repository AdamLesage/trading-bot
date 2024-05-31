#!/bin/bash

# Install the coverage tool if not already installed
pip3 install --user coverage

# Find the coverage tool
COVERAGE=$(python3 -m site --user-base)/bin/coverage

$COVERAGE erase

cd ./tests

# Run the tests and measure coverage
# Discover allows us to run all tests in the directory
$COVERAGE run -m unittest discover

$COVERAGE report -m

# Check for test failures
FAILURES=$($COVERAGE report -m | grep "FAILED")
echo "Failures: $FAILURES"

if [ -n "$FAILURES" ]; then
    exit 1
else
    exit 0
fi
