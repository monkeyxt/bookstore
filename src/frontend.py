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
@app.route("/search/<topic>")
def search(topic):

    topic_query = {
        "topic": topic
    }
    books = requests.post(CATALOG_IP + '/query/', json=topic_query).json()

    # Parse the json of the search result
    search_result = []
    for book in books:
        search_result.extend(["Title: ", book, " "])
        search_result.extend(["ID: ", str(books[book]['item_number']), "\n"])

    # Return the search result in a string
    return "".join(search_result)


# Lookup the requested item number
@app.route("/lookup/<int:item_number>")
def lookup(item_number):

    item_query = {
        "item_number": item_number
    }
    books = requests.post(CATALOG_IP + '/query/', json=item_query).json()

    # Parse the lookup result
    lookup_result = []
    for book in books:
        lookup_result.extend(["Title: ", book, "\n"])
        lookup_result.extend(["Price: ", str(books[book]["price"]), "\n"])
        lookup_result.extend(["Stock: ", str(books[book]["stock"]), "\n"])

    # Return the lookup result in a string
    return "".join(lookup_result)


# Buy the requested item number
@app.route("/buy/<item_number>")
def buy(item_number):
    response = requests.post(ORDER_IP + '/buy/' + item_number).json()

    # Use the 'status' boolean in json to check if the purchase was successful
    if response["status"]:
        return "Successfully purchased: " + str(item_number) + "\n"
    else:
        return "Failed to purchase: " + str(item_number) + "\n"


if __name__ == "__main__":
    FRONTEND_PORT = config['frontend'].split(":")[2]
    app.run(host='0.0.0.0', port=FRONTEND_PORT)
