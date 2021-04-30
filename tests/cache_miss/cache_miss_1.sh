#!/bin/bash
# This test times writes without invalidation for 100 sequential requests

cd ../../src/

for i in {1..100}
  do
    python3 client.py buy 1 1 cache1.1
  done
