#!/bin/bash
## This test measures the amount of time for 1000 sequential request of each operation

cd ../../src/

echo "1000 sequential request for search operation"
python3 client.py search systems 1000 c1
python3 client.py search gradschool 1000 c1

echo "1000 sequential request for lookup operation"
python ../../src/client.py lookup 1 1000 c1
python ../../src/client.py lookup 2 1000 c1
python ../../src/client.py lookup 3 1000 c1
python ../../src/client.py lookup 4 1000 c1

echo "1000 sequential request for buy operation"
python ../../src/client.py buy 1 1000 c1
python ../../src/client.py buy 2 1000 c1
python ../../src/client.py buy 3 1000 c1
python ../../src/client.py buy 4 1000 c1

