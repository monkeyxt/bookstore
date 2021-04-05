#!/bin/bash
## This test tests for concurrent requests. 40 clients. 100 lookup requests each

cd ../../src/

echo "100 lookup request for 40 concurrent clients"
python3 client.py lookup 1 100 40con1 &
python3 client.py lookup 1 100 40con2 &
python3 client.py lookup 1 100 40con3 &
python3 client.py lookup 1 100 40con4 &
python3 client.py lookup 1 100 40con5 &
python3 client.py lookup 1 100 40con6 &
python3 client.py lookup 1 100 40con7 &
python3 client.py lookup 1 100 40con8 &
python3 client.py lookup 1 100 40con9 &
python3 client.py lookup 1 100 40con10 &
python3 client.py lookup 1 100 40con11 &
python3 client.py lookup 1 100 40con12 &
python3 client.py lookup 1 100 40con13 &
python3 client.py lookup 1 100 40con14 &
python3 client.py lookup 1 100 40con15 &
python3 client.py lookup 1 100 40con16 &
python3 client.py lookup 1 100 40con17 &
python3 client.py lookup 1 100 40con18 &
python3 client.py lookup 1 100 40con19 &
python3 client.py lookup 1 100 40con20 &
python3 client.py lookup 1 100 40con21 &
python3 client.py lookup 1 100 40con22 &
python3 client.py lookup 1 100 40con23 &
python3 client.py lookup 1 100 40con24 &
python3 client.py lookup 1 100 40con25 &
python3 client.py lookup 1 100 40con26 &
python3 client.py lookup 1 100 40con27 &
python3 client.py lookup 1 100 40con28 &
python3 client.py lookup 1 100 40con29 &
python3 client.py lookup 1 100 40con30 &
python3 client.py lookup 1 100 40con31 &
python3 client.py lookup 1 100 40con32 &
python3 client.py lookup 1 100 40con33 &
python3 client.py lookup 1 100 40con34 &
python3 client.py lookup 1 100 40con35 &
python3 client.py lookup 1 100 40con36 &
python3 client.py lookup 1 100 40con37 &
python3 client.py lookup 1 100 40con38 &
python3 client.py lookup 1 100 40con39 &
python3 client.py lookup 1 100 40con40