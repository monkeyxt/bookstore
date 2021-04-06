#!/bin/bash
# This script should be run after the forntendperf log is grabbed from a remote
# server. The frontend server should have the proper log data which this script
# will use.

cat frontendperflog.log | grep -oP "search time: \K[0-9]*" > searchresults.txt
cat frontendperflog.log | grep -oP "lookup time: \K[0-9]*" > lookupresults.txt
cat frontendperflog.log | grep -oP "frontend buy time: \K[0-9]*" > frontendbuyresults.txt
cat frontendperflog.log | grep -oP "order buy time: \K[0-9]*" > orderbuyresults.txt

python averages.py searchresults.txt
python averages.py lookupresults.txt
python averages.py frontendbuyresults.txt
python averages.py orderbuyresults.txt
