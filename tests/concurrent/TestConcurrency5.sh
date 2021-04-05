#!/bin/bash
## This test tests for concurrent requests. 5 clients. 100 lookup requests each

cd ../../src/

echo "100 lookup request for 5 concurrent clients"
python3 client.py lookup 1 100 5con1 &
python3 client.py lookup 1 100 5con2 &
python3 client.py lookup 1 100 5con3 &
python3 client.py lookup 1 100 5con4 &
python3 client.py lookup 1 100 5con5