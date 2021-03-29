from flask import Flask, request
import requests
import yaml
import json

## Define Flask frontend
app = Flask("catalog")

## Load Server configs from yaml
with open('config.yml', 'r') as file:
    config = yaml.load(file, Loader=yaml.FullLoader)

FRONTEND_IP = config['frontend']
ORDER_IP = config['order']
CATALOG_IP = config['catalog']

books = {
    "RPC for Dummies": {
        "item_number": 345,
        "topic": "systems"
    },
    "Cooking for the Impatient Graduate Student": {
        "item_number": 359,
        "topic": "gradschool"
    }
}

@app.route("/testing/", methods = ["GET"])
def testing():
    data = json.loads(request.data)
    print(data)
    return {"get": "fucked"}

## Query endpoint
# Include a data payload with the request (ex: {"item_number": 100})
@app.route("/query/", methods = ["GET"])
def query():
    output = {}
    query_data = json.loads(request.data)
    if "topic" in query_data.keys():
        topic = query_data["topic"]
        for key, value in books.items():
            if value["topic"] == topic:
                output[key] = value

    elif "item_number" in query_data.keys():
        item_number = query_data["item_number"]
        for key, value in books.items():
            if value["item_number"] == item_number:
                output[key] = value
    if len(output) == 0:
            print("No matches found")

    return output


## Update endpoint
# Include a data payload, the keys of which will be set in the databse
# ex: update_data = {"New Book": {"item_number": 111, "topic": "knowledge"}}
@app.route("/update/", methods = ["POST"])
def update():
    update_data = json.loads(request.data)
    for key, value in update_data.items():
        books[key] = value
    return {"Success": True}

if __name__ == "__main__":
    CATALOG_PORT = config['catalog'].split(":")[2]
    app.run(host='0.0.0.0',port = CATALOG_PORT)

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
        "topic": "test_topic"
    }
}
with open('config.yml', 'r') as file:
    config = yaml.load(file, Loader=yaml.FullLoader)

query_path = f"{config['catalog']}/query"
update_path = f"{config['catalog']}/update"
"""
# Sample request bodies
"""
r = requests.get(query_path, data=json.dumps(query_data))
response_contents = json.loads(r.content)
"""