#!/bin/bash
# This test times reads without cache miss for 100 sequential reads

cd ../../src/

for i in {1..100}
  do
    python3 client.py read 1 1 cache3.1
  done
