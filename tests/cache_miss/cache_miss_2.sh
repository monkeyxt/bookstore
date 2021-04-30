#!/bin/bash
# This test times writes with invalidation for 100 sequential requests

cd ../../src/

for i in {1..100}
  do
    python3 client.py lookup 1 1 cache2.1
    python3 client.py buy 1 1 cache2.2
  done
