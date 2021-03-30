#!/bin/bash
# This test makes sure that the code perform buy method correctly

echo "Starting the order server..."
(cd ../src && python3 order.py)

echo "Starting the catalog server..."
(cd ../src && python3 catalog.py)

echo "Starting the frontend server..."
(cd ../src && python3 catalog.py)

echo "Performing client buy..."
(cd ../src && python3 client.py buy 1)