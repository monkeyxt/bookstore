import requests
import sys
import time
import yaml

# Load Server configs from yaml
with open('config.yml', 'r') as file:
    config = yaml.load(file, Loader=yaml.FullLoader)

FRONTEND_IP = config['frontend']


# Search the requested topic
def search(topic):
    search_output = requests.get(FRONTEND_IP + '/search/' + topic).text
    print(search_output)
    return search_output


# Lookup the requested book item
def lookup(item_number):
    item_number_str = str(item_number)
    lookup_output = requests.get(FRONTEND_IP + '/lookup/' + item_number_str).text
    print(lookup_output)
    return lookup_output


# Buy the requested book item
def buy(item_number):
    item_number_str = str(item_number)
    buy_output = requests.get(FRONTEND_IP + '/buy/' + item_number_str).text
    print(buy_output)
    return buy_output


def main():
    method_name = sys.argv[1]
    parameter_name = sys.argv[2]
    getattr(sys.modules[__name__], method_name)(parameter_name)


if __name__ == '__main__':
    main()
