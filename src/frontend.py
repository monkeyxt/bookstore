from flask import Flask
import time
import requests
import yaml
import random
import logging

# Define Flask frontend
app = Flask("frontend")

# Load Server configs from yaml
with open('config.yml', 'r') as file:
    config = yaml.load(file, Loader=yaml.FullLoader)

# Server addresses and list of replica addresses
FRONTEND_IP = config['frontend']
ORDER_IP1 = config['order1']
ORDER_IP2 = config['order2']
CATALOG_IP1 = config['catalog1']
CATALOG_IP2 = config['catalog2']
order_replica_list = [ORDER_IP1, ORDER_IP2]
catalog_replica_list = [CATALOG_IP1, CATALOG_IP2]

# Local dictionary of book titles
book_titles = {
    1: "How to get a good grade in 677 in 20 minutes a day",
    2: "RPC for Dummies",
    3: "Xen and the Art of Surviving Graduate School",
    4: "Cooking for the Impatient Graduate Student",
    5: "How to finish Project 3 on time",
    6: "Why theory classes are so hard",
    7: "Spring in the Pioneer Valley"
}

# Define local cache
cache = {}

# Initializers for performance logger
perf_logger = logging.getLogger("perf")
perf_logger.setLevel(logging.DEBUG)
perf_file_handler = logging.FileHandler('frontendperf.log')
perf_file_handler.setLevel(logging.DEBUG)
perf_logger.addHandler(perf_file_handler)


# Load balancing between replicas. Randomly choose server replica and return the location of one of the replica of the
# requested server type.
def get_server_location(replica):
    server_location = random.choice(replica)
    return server_location


# Invalidate a frontend cache. The parameters could be a topic or an item number.
@app.route("/invalidate/<key>", methods=["PUT"])
def invalidate(key):
    if key in cache:
        del cache[key]
        return "Entry " + key + " deleted."
    return "Entry" + key + "not in cache."


# Search for the requested topic
@app.route("/search/<topic>")
def search(topic: str) -> str:
    # Check cache if the topic is in cache
    if topic in cache:
        return cache[topic]

    logging.info(f"Searching for topic: {topic}")
    server_location = get_server_location(catalog_replica_list)
    topic_query = {
        "topic": topic
    }

    print(server_location)

    try:
        search_start = time.perf_counter_ns()
        books = requests.post("http://" + server_location + '/query/', json=topic_query).json()
        search_elapsed = time.perf_counter_ns() - search_start
        perf_logger.info(f"search time: {search_elapsed}")

        # Parse the json of the search result
        search_result = []
        for book in books:
            search_result.extend(["Title: ", book, " "])
            search_result.extend(["ID: ", str(books[book]['item_number']), "\n"])

        final_result = "".join(search_result)
        cache[topic] = final_result

        # Return the search result in a string
        return final_result + "\n" + "Elapsed time (search): " + str(search_elapsed)

    except requests.exceptions.ConnectionError:
        # The chosen replica did not respond. Randomly pick another one to try again
        print("Chosen catalog replica failed to respond. Trying another replica")
        return search(topic)


# Lookup the requested item number
@app.route("/lookup/<int:item_number>")
def lookup(item_number):

    # Check cache to see if item_number is in cache
    if item_number in cache:
        return cache[item_number]

    title = book_titles[int(item_number)]
    logging.info(f"Looking up item: {title}")
    server_location = get_server_location(catalog_replica_list)
    item_query = {
        "item_number": item_number
    }

    try:
        lookup_start = time.perf_counter_ns()
        books = requests.post("http://" + server_location + '/query/', json=item_query).json()
        lookup_elapsed = time.perf_counter_ns() - lookup_start
        perf_logger.info(f"lookup time: {lookup_elapsed}")

        # Parse the lookup result
        lookup_result = []
        for book in books:
            lookup_result.extend(["Title: ", book, "\n"])
            lookup_result.extend(["Price: ", str(books[book]["price"]), "\n"])
            lookup_result.extend(["Stock: ", str(books[book]["stock"]), "\n"])

        final_result = "".join(lookup_result)
        cache[item_number] = final_result

        # Return the lookup result in a string
        return final_result + "\n" + "Elapsed time (lookup): " + str(lookup_elapsed)

    except requests.exceptions.ConnectionError:
        # The chosen replica did not respond. Randomly pick another one to try again
        print("Chosen catalog replica failed to respond. Trying another replica")
        return lookup(item_number)


# Buy the requested item number
@app.route("/buy/<item_number>")
def buy(item_number):
    title = book_titles[int(item_number)]
    server_location = get_server_location(order_replica_list)

    logging.info(f"Attempting to buy item: {title}")
    frontend_buy_start = time.perf_counter_ns()

    try:
        response = requests.post("http://" + server_location + '/buy/' + item_number).json()
        frontend_buy_elapsed = time.perf_counter_ns() - frontend_buy_start

        perf_logger.info(f"frontend buy time: {frontend_buy_elapsed}")
        order_elapsed = response["elapsed_time"]
        perf_logger.info(f"order buy time: {order_elapsed}")

        # Use the 'status' boolean in json to check if the purchase was successful
        if response["status"]:
            logging.info("Success")
            return "Successfully purchased: " + str(title) + "\n" + \
                   "Elapsed time (buy, order server): " + str(response["elapsed_time"]) + \
                   "\n" + "Elapsed time (buy, frontend server): " + str(frontend_buy_elapsed)
        else:
            logging.error("Purchase Failed")
            return "Failed to purchase: " + str(title) + "\n" + \
                   "Elapsed time (buy, order server): " + str(response["elapsed_time"]) + \
                   "\n" + "Elapsed time (buy, frontend server): " + str(frontend_buy_elapsed)

    except requests.exceptions.ConnectionError:
        # The chosen replica did not respond. Randomly pick another one to try again
        print("Chosen order replica failed to respond. Trying another replica")
        return buy(item_number)


if __name__ == "__main__":
    log_path = "logs/frontend.txt"
    open(log_path, "w").close()
    logging.basicConfig(filename=log_path, level=logging.DEBUG, format="%(asctime)s %(message)s")
    FRONTEND_PORT = config['frontend'].split(":")[-1]
    logging.info(f"Frontend server starting on port {FRONTEND_PORT}")
    app.run(host='0.0.0.0', port=FRONTEND_PORT)