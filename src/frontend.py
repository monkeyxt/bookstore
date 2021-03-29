from flask import Flask
import requests
import yaml

# Define Flask frontend
app = Flask("frontend")

# Load Server configs from yaml
with open('config.yml', 'r') as file:
    config = yaml.load(file, Loader=yaml.FullLoader)

FRONTEND_IP = config['frontend']
ORDER_IP = config['order']
CATALOG_IP = config['catalog']


# Search for the requested topic
@app.route("/search/<topic>", methods=["GET"])
def search(topic):

    topic_query = {
        "topic": topic
    }
    books = requests.get(CATALOG_IP + '/query/', json=topic_query).json()

    # Parse the json of the search result
    search_result = []
    for book in books["items"]:
        search_result.extend(["Title: ", book, " "])
        search_result.extend(["ID: ", str(books["items"][book]), "\n"])

    # Return the search result in a string
    return "".join(search_result)


# Lookup the requested item number
@app.route("/lookup/<item_number>")
def lookup(item_number):

    item_query = {
        "item_number": item_number
    }
    books = requests.get(CATALOG_IP + '/query/', json=item_query).json()

    # Parse the lookup result
    lookup_result = []
    for book in books:
        lookup_result.extend(["Title: ", book, "\n"])
        lookup_result.extend(["Cost: ", str(books[book]["cost"]), "\n"])
        lookup_result.extend(["Amount: ", str(books[book]["amount"]), "\n"])

    # Return the lookup result in a string
    return "".join(lookup_result)


# Buy the requested item number
@app.route("/buy/<item_number>")
def buy(item_number):
    response = requests.get(ORDER_IP + '/buy/' + item_number).json()

    # Use the 'status' boolean in json to check if the purchase was successful
    if response["status"]:
        return "Successfully purchased: " + response["title"] + "\n"
    else:
        return "Failed to purchase: " + response["title"] + "\n"


if __name__ == "__main__":
    FRONTEND_PORT = config['frontend'].split(":")[2]
    app.run(host='0.0.0.0', port=FRONTEND_PORT)
