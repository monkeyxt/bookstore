# bookstore
Book store lab 2 for CS 677

## Requirements
- Python 3
- Flask

## How to run
Run the `run_all.sh` script in the `tests` directory to build and deploy.
More detailed information is available in the design documents in the `docs` directory.
Make sure to specify the desired server addresses in `src/config.yml`.

## How to test
Unit tests can be run individually using tests in `tests/unit`.
More detailed information is available in the test documents in the `docs` directory.

## Things to do

- change update to also update cost, and increment / decrement rather than accept and write a value
- frontend caching
- catalog / order primary replication
- communication with caching server from order / catalog
- dockerize everything
- health check / heartbeat on replicas, frontend communicates and checks if up/down, forward requests to nonfaulty nodes(edited)
- frontend remote restart / resync with nonfaulty nodes(edited)
- (extra credit) raft
- make sure its very easy to enable / disable caching, test request perf with/without
- invalidate cache test, check for consistency and performance of subsequent requests
- add new books
- fault tolerance needs to be able to bring up primary in recovery(edited)
