#!/bin/bash
## This test makes sure that the code perform lookup and search methods correctly.

echo "Starting the order server..."
(cd ../src && python3 order.py)

echo "Starting the catalog server..."
(cd ../src && python3 catalog.py)

echo "Starting the frontend server..."
(cd ../src && python3 catalog.py)

echo "Performing client lookup..."
(cd ../src && python3 client.py lookup 1)

echo "Performing client search..."
(cd ../src && python3 client.py search systems)
