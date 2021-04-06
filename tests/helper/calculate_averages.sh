#!/bin/bash
# This script should be run after the forntendperf log is grabbed from a remote
# server. The frontend server should have the proper log data which this script
# will use.

cat ./frontendperf.log | grep -oP "search time: \K[0-9]*" > searchresults.txt
cat ./frontendperf.log | grep -oP "lookup time: \K[0-9]*" > lookupresults.txt
cat ./frontendperf.log | grep -oP "frontend buy time: \K[0-9]*" > frontendbuyresults.txt
cat ./frontendperf.log | grep -oP "order buy time: \K[0-9]*" > orderbuyresults.txt

python averages.py searchresults.txt >> averageresults.txt
python averages.py lookupresults.txt >> averageresults.txt
python averages.py frontendbuyresults.txt >> averageresults.txt
python averages.py orderbuyresults.txt >> averageresults.txt
