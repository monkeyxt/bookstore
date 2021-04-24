# bookstore
Book store lab 2 for CS 677

## Requirements
 - Python 3
 - Flask
 - Docker

## How to run (docker)
**NOTE:** these all run, however without proper container networking the services may not be able to talk to each other.
In order to properly run containers like this, one needs to first get distinct IPs, edit `config.yml`, rebuild docker images, and deploy the containers to each of those IPs.
Alternatively, if you are on linux, use the host networking option.
In this case, you would run all the following docker commands with the `--network=host` option.

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

## How to run (python)
First make sure you have python and all dependencies installed.
Then, navigate to the `src` directory and run the following:
```sh
python catalog.py catalog1
python catalog.py catalog2
python order.py order1
python order.py order2
python frontend.py
```
