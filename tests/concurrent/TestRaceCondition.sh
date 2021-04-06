#!/bin/bash
## This test tests for concurrent requests. 3 clients. 100 buy requests each

cd ../../src/

echo "100 buy request for 3 concurrent clients"
python3 client.py buy 4 100 &
python3 client.py buy 4 100 &
python3 client.py buy 4 100

sleep 5

python3 client.py lookup 4
