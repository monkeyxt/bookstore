#!/bin/bash
# This tests test for fault tolerance capabilities of the system. This script crashes the primary replica.

# Get config file path
config=$1

# Get hosts for each server as well as ip addresses without ports
frontend_host=$(grep -A0 'frontend:' $config | awk '{ print $2}' | tr -d '"')
frontend_ip=$(echo $frontend_host | cut -f1 -d":")

order_host=$(grep -A0 'order:' $config | awk '{ print $2}' | tr -d '"')
order_ip=$(echo $order_host | cut -f1 -d":")

catalog_host=$(grep -A0 'catalog:' $config | awk '{ print $2}' | tr -d '"')
catalog_ip=$(echo $catalog_host | cut -f1 -d":")

# Send random buy and lookup requests
cd ../../src/

python3 client.py buy 1 &
python3 client.py buy 1 &
python3 client.py buy 1 &
python3 client.py buy 1 &
python3 client.py buy 1 &
python3 client.py buy 1 &
python3 client.py buy 1 &
python3 client.py buy 2 &
python3 client.py buy 2 &
python3 client.py buy 2

# Crash the primary replica
sleep 5
echo Killing the primary replica and query through other server


# Send a second round of buy and lookup requests
sleep 5
python3 client.py buy 2 &
python3 client.py buy 3 &
python3 client.py buy 5 &
python3 client.py buy 7 &
python3 client.py buy 1 &
python3 client.py buy 6 &
python3 client.py buy 4

# Check database consistency by sending a download request to both servers
