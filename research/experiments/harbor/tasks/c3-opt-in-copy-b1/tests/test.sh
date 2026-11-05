#!/bin/bash
set -u
mkdir -p /logs/verifier
python3 /tests/check.py
code=$?
if [ "$code" -eq 0 ]; then
  echo 1 > /logs/verifier/reward.txt
else
  echo 0 > /logs/verifier/reward.txt
fi
