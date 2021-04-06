#!/bin/bash
## This test measures the per tier response time of a request

cd ../../src/

echo "1000 sequential request for search operation"
python3 client.py search systems 1000 c2

echo "1000 sequential request for lookup operation"
python3 client.py lookup 1 1000 c2

echo "1000 sequential request for buy operation"
python3 client.py buy 1 1000 c2