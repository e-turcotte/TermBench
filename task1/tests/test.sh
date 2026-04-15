#!/bin/bash
set -e

mkdir -p /logs/verifier

# Make sure pip is available
apt-get update -qq && apt-get install -y -qq python3-pip

# Install dependencies explicitly
pip3 install cryptography pytest --quiet

# Run tests
pytest /tests/test_outputs.py -v
RESULT=$?

if [ $RESULT -eq 0 ]; then
    echo "1" > /logs/verifier/reward.txt
else
    echo "0" > /logs/verifier/reward.txt
fi

exit $RESULT
