#!/bin/bash
## This test tests for concurrent requests. 10 clients. 100 lookup requests each

cd ../../src/

echo "100 lookup request for 10 concurrent clients"
python3 client.py lookup 1 100 10con1 &
python3 client.py lookup 1 100 10con2 &
python3 client.py lookup 1 100 10con3 &
python3 client.py lookup 1 100 10con4 &
python3 client.py lookup 1 100 10con5 &
python3 client.py lookup 1 100 10con6 &
python3 client.py lookup 1 100 10con7 &
python3 client.py lookup 1 100 10con8 &
python3 client.py lookup 1 100 10con9 &
python3 client.py lookup 1 100 10con10