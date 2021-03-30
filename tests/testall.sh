#!/bin/bash

echo "Running all test scripts for 30 seconds each..."

echo "Running test 1..."
timeout 30s bash test1.sh

echo "Running test 2..."
timeout 30s bash test2.sh