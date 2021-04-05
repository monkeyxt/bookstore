#!/bin/bash
## This test makes sure that the code perform lookup and search methods correctly.
orderpid=0
catalogpid=0
frontendpid=0

cd ../../src/

echo "Starting the order server..."
python3 order.py & orderpid=$!

echo "Starting the catalog server..."
python3 catalog.py & catalogpid=$!

echo "Starting the frontend server..."
python3 frontend.py & frontendpid=$!

sleep 0.5

echo "Performing client lookup..."
python3 client.py lookup 1

echo "Performing client search..."
python3 client.py search systems

echo "Performing client buy..."
python3 client.py buy 1

kill $orderpid $frontendpid $catalogpid
