#!/bin/bash
## This test measures the amount of time for 1000 sequential request of each operation

cd ../../src/

echo "1000 sequential request for search operation"
python3 client.py search systems 100 c1
python3 client.py search gradschool 100 c1

echo "1000 sequential request for lookup operation"
python3 client.py lookup 1 100 c1
python3 client.py lookup 2 100 c1
python3 client.py lookup 3 100 c1
python3 client.py lookup 4 100 c1
python3 client.py lookup 5 100 c1
python3 client.py lookup 6 100 c1
python3 client.py lookup 7 100 c1

echo "1000 sequential request for buy operation"
python3 client.py buy 1 100 c1
python3 client.py buy 2 100 c1
python3 client.py buy 3 100 c1
python3 client.py buy 4 100 c1
python3 client.py buy 5 100 c1
python3 client.py buy 6 100 c1
python3 client.py buy 7 100 c1
