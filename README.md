# bookstore
Book store lab 2 for CS 677

## Requirements
 - Python 3
 - Flask
 - Docker

## How to run (docker)
First make sure you have docker installed. Then, navigate to the `src` directory.
To build the docker images, run `bash docker/docker_builds.sh`.
Finally to run the containers, do the following:
```sh
docker run -p 9006:9006 frontend
docker run -p 9002:9002 order order1
docker run -p 9003:9003 order order2
docker run -p 9004:9004 catalog catalog1
docker run -p 9005:9005 catalog catalog2
```

Then, you can run `python client.py buy 1` to buy the book with ID 1, or you can get creative and use other numbers, like 2!

## How to run
Run the `run_all.sh` script in the `tests` directory to build and deploy.
More detailed information is available in the design documents in the `docs` directory.
Make sure to specify the desired server addresses in `src/config.yml`.

## How to test
Unit tests can be run individually using tests in `tests/unit`.
More detailed information is available in the test documents in the `docs` directory.

