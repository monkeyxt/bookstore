#!/bin/bash
# This tests test for fault tolerance capabilities of the system. This script crashes the primary replica.

# Start the servers and record their pids
cd ../../src/
echo "Starting servers..."
echo "Starting order1..."
python3 order.py order1 & order1_pid=$!
sleep 5s

echo "Starting order2..."
python3 order.py order2 & order2_pid=$!
sleep 5s

echo "Starting catalog1..."
python3 catalog.py catalog1 & catalog1_pid=$!
sleep 5s

echo "Starting catalog2..."
python3 catalog.py catalog2 & catalog2_pid=$!
sleep 5s

# Start frontend with caching disabled to ensure always go to catalog servers
echo "Starting frontent..."
python3 frontend.py False & frontend_pid=$!
sleep 5s


# Crash the primary replica
# sleep 5
echo "Killing catalog1..."
kill $catalog1_pid

# Perform buy and lookup requests to ensure replica is functioning properly
python3 client.py lookup 1
python3 client.py buy 1
python3 client.py buy 1
python3 client.py buy 1
python3 client.py lookup 1

# Wait a few seconds to make sure all requests finish
sleep 5s

# Restart catalog replica
echo "Restarting catalog1..."
python3 catalog.py catalog1 & catalog1_pid=$!

# Wait to allow server to start and synchronize
sleep 10s

# Kill secondary replica
echo "Killing catalog2..."
kill $catalog2_pid

echo "Restarting catalog2..."
python3 catalog.py catalog2 & catalog2_pid=$!

# Perform buy and lookup requests again to ensure replica is functioning properly
python3 client.py lookup 1
python3 client.py buy 1
python3 client.py buy 1
python3 client.py buy 1
python3 client.py lookup 1


sleep 5s

function kill_servers() {
    echo "Killing all servers..."
    kill $order1_pid
    kill $order2_pid
    kill $catalog1_pid
    kill $catalog2_pid
    kill $frontend_pid
}
trap kill_servers INT TERM EXIT