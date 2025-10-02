#!/bin/bash
# test.sh

# Ensure root dir is in PYTHONPATH so "app" can be imported
export PYTHONPATH=$(pwd)

# Run all tests in the tests/ folder
python3 -m unittest discover -s tests -p "test*.py"
