from flask import Flask
import time
import requests
import yaml
import logging

# Define Flask frontend
app = Flask("frontend")

# Load Server configs from yaml
with open('config.yml', 'r') as file:
    config = yaml.load(file, Loader=yaml.FullLoader)

FRONTEND_IP = config['frontend']
ORDER_IP = config['order']
CATALOG_IP = config['catalog']

perf_logger = logging.getLogger("perf")
perf_logger.setLevel(logging.DEBUG)
perf_file_handler = logging.FileHandler('frontendperf.log')
perf_file_handler.setLevel(logging.DEBUG)
perf_logger.addHandler(perf_file_handler)

# Search for the requested topic
@app.route("/search/<topic>")
def search(topic):
    logging.info(f"Searching for topic: {topic}")
    topic_query = {
        "topic": topic
    }
    search_start = time.perf_counter_ns()
    books = requests.post(CATALOG_IP + '/query/', json=topic_query).json()
    search_elapsed = time.perf_counter_ns() - search_start
    perf_logger.info(f"search time: {search_elapsed}")

    # Parse the json of the search result
    search_result = []
    for book in books:
        search_result.extend(["Title: ", book, " "])
        search_result.extend(["ID: ", str(books[book]['item_number']), "\n"])

    # Return the search result in a string
    return "".join(search_result) + "\n" + \
        "Elapsed time (search): " + str(search_elapsed)


# Lookup the requested item number
@app.route("/lookup/<int:item_number>")
def lookup(item_number):
    logging.info(f"Looking up item: {item_number}")
    item_query = {
        "item_number": item_number
    }
    lookup_start = time.perf_counter_ns()
    books = requests.post(CATALOG_IP + '/query/', json=item_query).json()
    lookup_elapsed = time.perf_counter_ns() - lookup_start
    perf_logger.info(f"lookup time: {lookup_elapsed}")

    # Parse the lookup result
    lookup_result = []
    for book in books:
        lookup_result.extend(["Title: ", book, "\n"])
        lookup_result.extend(["Price: ", str(books[book]["price"]), "\n"])
        lookup_result.extend(["Stock: ", str(books[book]["stock"]), "\n"])

    # Return the lookup result in a string
    return "".join(lookup_result) + "\n" + \
        "Elapsed time (lookup): " + str(lookup_elapsed)


# Buy the requested item number
@app.route("/buy/<item_number>")
def buy(item_number):
    logging.info(f"Attempting to buy item: {item_number}")
    frontend_buy_start = time.perf_counter_ns()
    response = requests.post(ORDER_IP + '/buy/' + item_number).json()
    frontend_buy_elapsed = time.perf_counter_ns() - frontend_buy_start
    perf_logger.info(f"frontend buy time: {frontend_buy_elapsed}")
    order_elapsed = response["elapsed_time"]
    perf_logger.info(f"order buy time: {order_elapsed}")

    # Use the 'status' boolean in json to check if the purchase was successful
    if response["status"]:
        logging.info("Success")
        return "Successfully purchased: " + str(item_number) + "\n" + \
            "Elapsed time (buy, order server): " + str(response["elapsed_time"]) + \
            "\n" + "Elapsed time (buy, frontend server): " + str(frontend_buy_elapsed)
    else:
        logging.error("Purchase Failed")
        return "Failed to purchase: " + str(item_number) + "\n" + \
            "Elapsed time (buy, order server): " + str(response["elapsed_time"]) + \
            "\n" + "Elapsed time (buy, frontend server): " + str(frontend_buy_elapsed)

if __name__ == "__main__":
    log_path = "logs/frontend.txt"
    open(log_path, "w").close()
    logging.basicConfig(filename=log_path, level=logging.DEBUG, format="%(asctime)s %(message)s")
    logging.info("Frontend server started")
    FRONTEND_PORT = config['frontend'].split(":")[2]
    app.run(host='0.0.0.0', port=FRONTEND_PORT)
