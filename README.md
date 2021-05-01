# bookstore
Book store lab 3 for CS 677

## Requirements
 - Python 3
 - Flask
 - Docker

## How to run (docker)
**Make sure to put in the server names and the location of ssh key file in the script.**
To run the services remotely with docker, navigate to the `tests` directory and run `run_remote.sh` which will automatically take care of deployment. Then, you can run `python client.py buy 1` to buy the book with ID 1, or you can get creative and use other numbers, like 2!

To run all the tests, navigate to the `tests` directory and run `run_tests.sh` which will deploy the source codes and run our curated tests.

For more information, see the design and performance documentation in the `docs` directory.

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
If you are lazy like me and wants to have an automated process, navigate to the `tests` directory and run `run.sh`. Make sure to put in the server names in the script. Happy online shopping!
