#!/bin/bash
set -e

mkdir -p /logs/verifier

apt-get update -qq && apt-get install -y -qq python3-pip
pip3 install cryptography pytest --quiet

pytest /tests/test_outputs.py -v
RESULT=$?
if [ $RESULT -eq 0 ]; then
    echo "1" > /logs/verifier/reward.txt
else
    echo "0" > /logs/verifier/reward.txt
fi

exit $RESULT
