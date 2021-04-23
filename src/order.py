from flask import Flask, make_response
import requests
import yaml
import sys
import time
from threading import Lock
import csv
import codecs

# Define Flask frontend
app = Flask("order")

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

# Acquire order lock
order_lock = Lock()


################################################################################
# Helper functions for managing replicas
################################################################################

# Hold election and name the current server the primary. This is a watered down version of election algorithm since
# there are only two servers
def hold_election():
    return


# Notify other order nodes who is now the primary replica for order servers
def broadcast_coordinator():
    order_replica_list = app.config.get("order_replica_list")
    local_order_server = app.config.get("local_ip")
    for order_replica in order_replica_list:
        if order_replica != local_order_server:
            try:
                requests.get("http://" + order_replica + "/notify/" + app.config.get("primary_order"))
            except requests.exceptions.ConnectionError:
                print("The other replica is down. Failed to notify")


# Get notified who is the primary replica
@app.route("/notify/<primary>", methods=["GET"])
def notify(primary):
    app.config["primary_order"] = primary
    return


# Forwarding the query to the primary order replica
def forward_query(item_number, primary):
    try:
        response = requests.post("http://" + primary + '/buy/' + item_number).json()
        return response
    except requests.exceptions.ConnectionError:
        # Primary order server is down, make self primary and try again
        app.config["primary_order"] = app.config.get("local_ip")
        return forward_query(item_number, app.config.get("primary_order"))


# Sync an order to another other replica
def sync_order(order):
    order_id = str(order["order_id"])
    processing_time = str(order["processing_time"])
    item_number = str(order["item_number"])
    title = str(order["title"])
    status = str(order["status"])

    order_replica_list = app.config.get("order_replica_list")
    local_order_server = app.config.get("local_ip")
    for order_replica in order_replica_list:
        if order_replica != local_order_server:
            try:
                requests.post(
                    "http://" + order_replica + '/replicate/' + order_id + '/' + processing_time + '/' + item_number
                    + '/' + title + '/' + status).json()
            except requests.exceptions.ConnectionError:
                print("The other replica is down. Failed to sync order")
                return
    return


# Replicate the order from another server and store in local log to be consistent
@app.route("/replicate/<order_id>/<processing_time>/<item_number>/<title>/<status>")
def replicate(order_id, processing_time, item_number, title, status):
    order_id = int(order_id)
    processing_time = float(processing_time)
    status = (status == "True")

    order = create_order(order_id, processing_time, item_number, title, status)
    log_order(order)
    return


# Sync entire database from another replica
def sync_entire():
    order_replica_list = app.config.get("order_replica_list")
    local_order_server = app.config.get("local_ip")
    for order_replica in order_replica_list:
        if order_replica != local_order_server:
            try:
                response = requests.get("http://" + order_replica + "/download/"
                                        + "order" + str(order_replica_list.index(order_replica)+1) + "_db.txt")
                local_db = app.config.get("name") + "_db.txt"
                with open(local_db, "wb") as db:
                    db.write(response.content)
                    print(local_order_server + " successfully synced with primary replica.")
                    return
            except requests.exceptions.ConnectionError:
                print(order_replica + " is either down or the database has not been created.")
                return

    # TODO: case where the current replica is the only one up
    return


# Download entire database to another replica
@app.route("/download/<filename>")
def download(filename):
    file_data = codecs.open(filename, 'rb').read()
    response = make_response()
    response.data = file_data
    return response


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
    with open(app.config["local_db"], mode='w') as order_log:
        fieldnames = ['order_id', 'processing_time', 'item_number', 'title', 'status']
        writer = csv.DictWriter(order_log, fieldnames=fieldnames)
        writer.writeheader()


# Get the list of orders as a dictionary
def get_order_list():
    with open(app.config["local_db"], mode='r') as order_log:
        csv_reader = csv.DictReader(order_log)
        return [row for row in csv_reader]


# Get the number of orders
def get_order_num():
    order_list = get_order_list()
    return len(order_list)


# Create an order field to log into the CSV txt order database
def create_order(order_id, processing_time, item_number, title, status):
    return {'order_id': order_id, 'processing_time': processing_time, 'item_number': item_number,
            'title': title, 'status': status}


# Write an order into the CSV txt order database
def log_order(order):
    with open(app.config.get("local_db"), mode='a') as order_log:
        fieldnames = ['order_id', 'processing_time', 'item_number', 'title', 'status']
        writer = csv.DictWriter(order_log, fieldnames=fieldnames)
        writer.writerow(order)


################################################################################
# Functions for updating the catalog server
################################################################################


# Query the catalog server
def query_catalog_server(item_number):
    primary = app.config.get("assigned_catalog")
    item_query = {
        "item_number": item_number
    }
    try:
        response = requests.post("http://" + primary + '/query/', json=item_query).json()
        book = list(response.keys())[0]
        amount = list(response.values())[0]["stock"]
        cost = list(response.values())[0]["price"]
        return book, amount, cost

    except requests.exceptions.ConnectionError:
        # primary catalog server must be down try another server
        print("Catalog server replica " + primary + " down")
        if primary == CATALOG_IP1:
            app.config["assigned_catalog"] = CATALOG_IP2
        else:
            app.config["assigned_catalog"] = CATALOG_IP1
        return query_catalog_server(item_number)


# Decrease the catalog server and return the new quantity
def decrement_catalog_server(item_number):
    response = requests.post(
        "http://" + app.config.get("assigned_catalog") + '/update/' + item_number + '/amount/decrease/1').json()
    status = list(response.values())[0]["status"]
    return status


@app.route("/buy/<int:item_number>", methods=["POST"])
def buy(item_number):
    # The current server is not the primary replica, forward to the primary
    if app.config.get("primary_order") != app.config.get("local_ip"):
        response = forward_query(item_number, app.config.get("primary_order"))
        return response
    # Else the current server is the primary replica, execute locally
    else:
        with order_lock:
            start = time.time()
            item, cost, amount = query_catalog_server(item_number)
            end = time.time()
            elapsed_time = end - start

            order_id = get_order_num() + 1

            if amount <= 0:
                # Item not in stock, buy failed
                status = False
            else:
                status = decrement_catalog_server(item_number)

            order = create_order(order_id, elapsed_time, item_number, book_titles[int(item_number)], status)

            # TODO: some kind of blocking mechanism needed here for all the other replica to be notified
            # Write order to local database
            log_order(order)
            # Sync order with the other replica
            sync_order(order)

            if status:
                return {
                    "status": True,
                    "elapsed_time": elapsed_time
                }
            else:
                return {
                    "status": False,
                    "elapsed_time": elapsed_time
                }


################################################################################
# Config initialization and Flask startup
################################################################################


# Load the necessary configuration for the local order server
def load_config():
    # Local configurations
    app.config["name"] = sys.argv[1]
    app.config["local_ip"] = config[sys.argv[1]]
    app.config["local_port"] = app.config["local_ip"].split(":")[-1]
    app.config["local_db"] = app.config["name"] + "_db.txt"

    # List of other replicas
    order_replica_list = [ORDER_IP1, ORDER_IP2]
    app.config["order_replica_list"] = order_replica_list
    catalog_replica_list = [CATALOG_IP1, CATALOG_IP2]
    app.config["catalog_replica_list"] = catalog_replica_list

    # Set the default primary order server to the first IP in the list. Also set the catalog server so that order1
    # talks to catalog1 and order2 talks to catalog2
    app.config["primary_order"] = ORDER_IP1
    app.config["assigned_catalog"] = catalog_replica_list[order_replica_list.index(config[sys.argv[1]])]


if __name__ == "__main__":

    # Load config for the catalog server
    load_config()

    # Wait until the other replicas boot up. Then broadcast the primary and sync databases.
    #time.sleep(5)
    #broadcast_coordinator()
    #sync_entire()

    app.run(host='0.0.0.0', port=app.config["local_port"])
