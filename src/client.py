import requests
import sys
import yaml
import time
import os

# Load Server configs from yaml
with open('config.yml', 'r') as file:
    config = yaml.load(file, Loader=yaml.FullLoader)

FRONTEND_IP = config['frontend']


# Search the requested topic
def search(topic):
    print(topic)
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

    total_runtime = 0

    if len(sys.argv) > 3:
        iterations = int(sys.argv[3])

        for i in range(iterations):
            start = time.time()
            getattr(sys.modules[__name__], method_name)(parameter_name)
            end = time.time()
            total_runtime += (end - start)

        if len(sys.argv) > 4:
            client_id = str(sys.argv[4])
            filename = client_id + '_' + method_name + '_' + parameter_name + '_' + str(iterations)
            with open('../tests/output/' + filename + '.txt', 'w') as w_file:
                w_file.write(str(1.0 * total_runtime / iterations))
        else:
            print("Average Runtime: " + str(1.0 * total_runtime / iterations))

    else:
        getattr(sys.modules[__name__], method_name)(parameter_name)


if __name__ == '__main__':
    main()
