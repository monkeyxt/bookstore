#!/bin/bash
# This test times reads with cache miss for 100 sequential reads

cd ../../src/

for i in {1..100}
  do
    python3 client.py buy 1 1 cache4.1
    python3 client.py lookup 1 1 cache4.2
  done
