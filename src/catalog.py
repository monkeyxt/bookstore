import codecs
import csv
from flask import Flask, request, make_response, abort
import requests
import yaml
import json
import threading
import sys
import time

# Define Flask frontend
app = Flask("catalog")

################################################################################
# Macros
################################################################################

# Load Server configs from yaml
with open('config.yml', 'r') as file:
    config = yaml.load(file, Loader=yaml.FullLoader)

# Server addresses and list of replica addresses
FRONTEND_IP = config['frontend']
ORDER_IP1 = config['order1']
ORDER_IP2 = config['order2']
CATALOG_IP1 = config['catalog1']
CATALOG_IP2 = config['catalog2']

# Initial setting for the books catalog
books = {
    "How to get a good grade in 677 in 20 minutes a day": {
        "item_number": 1,
        "topic": "systems",
        "stock": 1011,
        "price": 3
    },
    "RPC for Dummies": {
        "item_number": 2,
        "topic": "systems",
        "stock": 1007,
        "price": 4
    },
    "Xen and the Art of Surviving Graduate School": {
        "item_number": 3,
        "topic": "gradschool",
        "stock": 1002,
        "price": 15
    },
    "Cooking for the Impatient Graduate Student": {
        "item_number": 4,
        "topic": "gradschool",
        "stock": 100,
        "price": 5
    },
    "How to finish Project 3 on time": {
        "item_number": 5,
        "topic": "gradschool",
        "stock": 100,
        "price": 1
    },
    "Why theory classes are so hard": {
        "item_number": 6,
        "topic": "systems",
        "stock": 20,
        "price": 2
    },
    "Spring in the Pioneer Valley": {
        "item_number": 7,
        "topic": "gradschool",
        "stock": 50,
        "price": 3
    }
}

books_lock = threading.Lock()
database_lock = threading.Lock()


################################################################################
# Helper functions for managing catalog replicas
################################################################################

# Hold election and name the current server the primary. This is a watered down version of election algorithm since
# there are only two servers
def hold_election():
    return


# Notify other catalog nodes who is now the primary replica for catalog servers
def broadcast_coordinator():
    catalog_replica_list = app.config.get("catalog_replica_list")
    local_catalog_server = app.config.get("local_ip")
    for catalog_replica in catalog_replica_list:
        if catalog_replica != local_catalog_server:
            try:
                requests.get("http://" + str(catalog_replica) + "/notify/" + app.config.get("primary_catalog"))
            except requests.exceptions.ConnectionError:
                print("The other catalog replica is down. Failed to notify")


# Get notified who is the primary catalog replica.
@app.route("/notify/<primary>", methods=["GET"])
def notify(primary):
    app.config["primary_catalog"] = primary
    return {
        "status": True,
    }


# Forwarding the query to the primary catalog replica
def forward_query(item_number, attribute, operation, number, primary):
    try:
        response = requests.post("http://" + str(primary) + "/update/" + str(item_number) + "/" + str(attribute) + "/" + str(operation) + "/" + str(number)).json()
        return response
    except requests.exceptions.ConnectionError:
        # Primary catalog server is down, make self primary and try again
        app.config["primary_catalog"] = app.config.get("local_ip")
        return forward_query(item_number, attribute, operation, number, app.config.get("primary_catalog"))


# Sync an order to another other replica by calling the same function as update on the other replica
def sync_order(order):
    item_number = str(order["item_number"])
    attribute = str(order["attribute"])
    operation = str(order["operation"])
    number = str(order["number"])

    catalog_replica_list = app.config.get("catalog_replica_list")
    local_catalog_server = app.config.get("local_ip")
    for catalog_replica in catalog_replica_list:
        if catalog_replica != local_catalog_server:
            try:
                response = requests.post("http://" + str(catalog_replica) + "/replicate/" + str(item_number) + "/" + str(attribute) + "/" + str(operation) + "/" + str(number)).json()
            except requests.exceptions.ConnectionError:
                print("The other replica is down. Failed to sync order")
                return
    return


# Sync entire database from another replica
def sync_entire():
    catalog_replica_list = app.config.get("catalog_replica_list")
    local_catalog_server = app.config.get("local_ip")
    for catalog_replica in catalog_replica_list:
        if catalog_replica != local_catalog_server:
            try:
                response = requests.get("http://" + str(catalog_replica) + "/download/catalog" + str(catalog_replica_list.index(catalog_replica)+1) + "_db.txt").json()
                books.update(response["books"])
                local_db = "databases/" + app.config.get("name") + "_db.txt"
                with open(local_db, "wb") as db:
                    db.write(bytes(response["file_data"], 'utf-8'))
                    return

            except requests.exceptions.ConnectionError:
                print(catalog_replica + " is down")
                return

    # TODO: case where the current replica is the only one up
    return


# Download entire database to another replica
@app.route("/download/<filename>", methods=["GET"])
def download(filename):
    with books_lock:
        with database_lock:
            file_data = codecs.open("databases/" + filename, 'rb').read()
            return {
                "file_data": file_data.decode('utf-8'),
                "books": books,
            }

# Respond to ping messages
@app.route("/ping/", methods=["POST"])
def ping():
    return {
        "status": True,
    }


################################################################################
# Helper functions for dealing with local database
################################################################################

# Initialize the order database as a CSV txt file
def initialize_orders():
    with open(app.config["local_db"], mode='w') as catalog_log:
        fieldnames = ['order_id', 'item_number', 'attribute', 'operation', 'number', 'status']
        writer = csv.DictWriter(catalog_log, fieldnames=fieldnames)
        writer.writeheader()


# Get the list of orders as a dictionary
def get_order_list():
    with open(app.config["local_db"], mode='r') as catalog_log:
        csv_reader = csv.DictReader(catalog_log)
        return [row for row in csv_reader]


# Get the number of orders
def get_order_num():
    order_list = get_order_list()
    return len(order_list)


# Create an order field to log into the CSV txt order database
def create_order(order_id, item_number, attribute, operation, number, status):
    return {'order_id': order_id, 'item_number': item_number, 'attribute': attribute, 'operation': operation,
            'number': number, 'status': status}


# Write an order into the CSV txt order database
def log_order(order):
    with open(app.config.get("local_db"), mode='a') as catalog_log:
        fieldnames = ['order_id', 'item_number', 'attribute', 'operation', 'number', 'status']
        writer = csv.DictWriter(catalog_log, fieldnames=fieldnames)
        writer.writerow(order)


################################################################################
# Functions for querying the catalog server
################################################################################


# Query endpoint. Include a data payload with the request (ex: {"item_number": 100})
@app.route("/query/", methods=["POST"])
def query():
    output = {}
    # If the request payload specifies a topic, grab all entries that match that topic
    query_data = json.loads(request.data)
    if "topic" in query_data.keys():
        topic = query_data["topic"]
        with books_lock:
            for key, value in books.items():
                if value["topic"] == topic:
                    output[key] = value

    # If the request payload specifies an item number, grab all entries with that item number
    elif "item_number" in query_data.keys():
        item_number = query_data["item_number"]
        with books_lock:
            for key, value in books.items():
                if value["item_number"] == item_number:
                    output[key] = value

    # If no matches are found in the search, print a message
    if len(output) == 0:
        print("No matches found")

    return output


# Updating an endpoint/Replicating an order
@app.route("/replicate/<item_number>/<attribute>/<operation>/<int:number>", methods=["POST"])
@app.route("/update/<item_number>/<attribute>/<operation>/<int:number>", methods=["POST"])
def update(item_number, attribute, operation, number):

    # Check to make sure that the operation is valid
    valid_attribute = ["stock", "price"]
    valid_operation = ["increase", "decrease"]

    if (attribute not in valid_attribute) or (operation not in valid_operation):
        abort(400)

    if number < 0:
        abort(400)

    # If the current machine is not the primary replica forward the request
    if app.config.get("primary_catalog") != app.config.get("local_ip"):
        if "replicate" in request.path:
            with books_lock:
                order_id = get_order_num() + 1
                if operation == "increase":
                    for book in books:
                        if str(books[book]["item_number"] == str(item_number)):
                            books[book][attribute] += number
                            status = True

                elif operation == "decrease":
                    for book in books:
                        if str(books[book]["item_number"]) == str(item_number):
                            if books[book][attribute] > 0:
                                books[book][attribute] -= number
                                print(books[book][attribute])
                                status = True
                            else:
                                status = False

            order = create_order(order_id, item_number, attribute, operation, number, status)
            log_order(order)
            if status:
                return {
                    "status": True,
                }
            else:
                return {
                    "status": False,
                }

        else:
            response = forward_query(item_number, attribute, operation, number, app.config.get("primary_catalog"))
            return response
    # Else the current server is the primary replica, execute locally
    else:
        with books_lock:
            order_id = get_order_num() + 1
            if operation == "increase":
                for book in books:
                    if str(books[book]["item_number"] == str(item_number)):
                        books[book][attribute] += number
                        status = True

            elif operation == "decrease":
                for book in books:
                    if str(books[book]["item_number"]) == str(item_number):
                        if books[book][attribute] > 0:
                            books[book][attribute] -= number
                            print(books[book][attribute])
                            status = True
                        else:
                            status = False

        order = create_order(order_id, item_number, attribute, operation, number, status)

        # TODO: some kind of blocking mechanism needed here for all the other replica to be notified
        # Write order to local database
        log_order(order)
        # Sync order with other replicas
        sync_order(order)

        #  Invalidate the frontend cache
        response = requests.post("http://" + FRONTEND_IP + "/invalidate/" + str(item_number)).text
        print(response)

        if status:
            return {
                "status": True,
            }
        else:
            return {
                "status": False,
            }

################################################################################
# Config initialization and Flask startup
################################################################################


# Load the necessary configuration for the local catalog server
def load_config():
    # Local configurations
    app.config["name"] = sys.argv[1]
    app.config["local_ip"] = config[sys.argv[1]]
    app.config["local_port"] = app.config["local_ip"].split(":")[-1]
    app.config["local_db"] = "databases/" + app.config["name"] + "_db.txt"

    # Create database file
    open(app.config.get("local_db"), "w").close()

    # List of other replicas
    order_replica_list = [ORDER_IP1, ORDER_IP2]
    app.config["order_replica_list"] = order_replica_list
    catalog_replica_list = [CATALOG_IP1, CATALOG_IP2]
    app.config["catalog_replica_list"] = catalog_replica_list

    # Set the default primary order server to the first IP in the list. Also set the catalog server so that order1
    # talks to catalog1 and order2 talks to catalog2
    app.config["primary_order"] = ORDER_IP1
    app.config["primary_catalog"] = CATALOG_IP1


if __name__ == "__main__":
    load_config()

    #time.sleep(5)
    broadcast_coordinator()
    sync_entire()

    app.run(host='0.0.0.0', port=app.config.get("local_port"), threaded=True)
