#!/bin/bash
## This test tests for concurrent requests. 20 clients. 100 lookup requests each

cd ../../src/

echo "100 lookup request for 20 concurrent clients"
python3 client.py lookup 1 100 20con1 &
python3 client.py lookup 1 100 20con2 &
python3 client.py lookup 1 100 20con3 &
python3 client.py lookup 1 100 20con4 &
python3 client.py lookup 1 100 20con5 &
python3 client.py lookup 1 100 20con6 &
python3 client.py lookup 1 100 20con7 &
python3 client.py lookup 1 100 20con8 &
python3 client.py lookup 1 100 20con9 &
python3 client.py lookup 1 100 20con10 &
python3 client.py lookup 1 100 20con11 &
python3 client.py lookup 1 100 20con12 &
python3 client.py lookup 1 100 20con13 &
python3 client.py lookup 1 100 20con14 &
python3 client.py lookup 1 100 20con15 &
python3 client.py lookup 1 100 20con16 &
python3 client.py lookup 1 100 20con17 &
python3 client.py lookup 1 100 20con18 &
python3 client.py lookup 1 100 20con19 &
python3 client.py lookup 1 100 20con20
