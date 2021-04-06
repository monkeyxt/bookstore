#!/bin/bash
## This test tests for concurrent requests. 2 clients. 100 lookup requests each

cd ../../src/

echo "100 lookup request for 2 concurrent clients"
python3 client.py lookup 1 100 2con1 &
python3 client.py lookup 1 100 2con2


