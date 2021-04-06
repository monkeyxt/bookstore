from flask import Flask, request
import requests
import yaml
import json
import threading
import logging

## Define Flask frontend
app = Flask("catalog")

## Load Server configs from yaml
with open('config.yml', 'r') as file:
    config = yaml.load(file, Loader=yaml.FullLoader)

FRONTEND_IP = config['frontend']
ORDER_IP = config['order']
CATALOG_IP = config['catalog']

# Initial setting for the books catalog
books = {
    "How to get a good grade in 677 in 20 minutes a day": {
        "item_number": 1,
        "topic": "systems",
        "stock": 11,
        "price": 3
    },
    "RPC for Dummies": {
        "item_number": 2,
        "topic": "systems",
        "stock": 7,
        "price": 4
    },
    "Xen and the Art of Surviving Graduate School": {
        "item_number": 3,
        "topic": "gradschool",
        "stock": 2,
        "price": 15
    },
    "Cooking for the Impatient Graduate Student": {
        "item_number": 4,
        "topic": "gradschool",
        "stock": 10,
        "price": 5
    }
}

books_lock = threading.Lock()

## Query endpoint
# Include a data payload with the request (ex: {"item_number": 100})
@app.route("/query/", methods = ["POST"])
def query():
    output = {}
    # If the request payload specifies a topic, grab all entires that match that topic
    query_data = json.loads(request.data)
    if "topic" in query_data.keys():
        topic = query_data["topic"]
        logging.info(f"Querying for topic: {topic}")
        for key, value in books.items():
            if value["topic"] == topic:
                output[key] = value

    # If the request payload specifies an item number, grab all entries with that item number
    elif "item_number" in query_data.keys():
        item_number = query_data["item_number"]
        logging.info(f"Querying for item number: {item_number}")
        for key, value in books.items():
            if value["item_number"] == item_number:
                output[key] = value

    # If no matches are found in the search, print a message
    if len(output) == 0:
            print("No matches found")

    return output


## Update endpoint
# Include a data payload, the keys of which will be set in the databse
# ex: update_data = {"New Book": {"item_number": 111, "topic": "knowledge"}}
@app.route("/update/", methods = ["POST"])
def update():
    update_data = json.loads(request.data)
    logging.info(f"Updating items: {list(update_data.keys())}")
    # Acquire the lock and update the book entries as specified
    with books_lock:
        for key, value in update_data.items():
            books[key] = value

    return {"Success": True}

if __name__ == "__main__":
    log_path = "../logs/catalog.txt"
    open(log_path, "w").close()
    logging.basicConfig(filename=log_path, level=logging.DEBUG, format="%(asctime)s %(message)s")
    logging.info("Catalog server started")
    CATALOG_PORT = config['catalog'].split(":")[2]
    app.run(host='0.0.0.0',port = CATALOG_PORT, threaded=True)

# The code below can be pasted into the python shell as set up
# before interacting with the API
"""
import json
import yaml
import requests
test_data = {"test_key": "test_value"}
item_query = {"item_number": 359}
topic_query = {"topic": "gradschool"}
update_data = {
    "New Book": {
        "item_number": 100,
        "topic": "test_topic",
        "stock": 1000,
        "price": 1
    }
}
with open('config.yml', 'r') as file:
    config = yaml.load(file, Loader=yaml.FullLoader)

query_path = f"{config['catalog']}/query"
update_path = f"{config['catalog']}/update"
"""
# Sample request bodies
"""
r = requests.post(query_path, data=json.dumps(query_data))
response_contents = json.loads(r.content)
"""