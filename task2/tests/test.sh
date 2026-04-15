#!/bin/bash

mkdir -p /logs/verifier
echo "0" > /logs/verifier/reward.txt

trap 'echo "0" > /logs/verifier/reward.txt' ERR

pytest /tests/test_outputs.py -v
RESULT=$?

if [ $RESULT -eq 0 ]; then
    echo "1" > /logs/verifier/reward.txt
else
    echo "0" > /logs/verifier/reward.txt
fi

exit $RESULT
