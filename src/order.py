from flask import Flask, request
import requests
import yaml

## Define Flask frontend
app = Flask("order")

## Load Server configs from yaml
with open('config.yml', 'r') as file:
    config = yaml.load(file, Loader=yaml.FullLoader)

FRONTEND_IP = config['frontend']
ORDER_IP = config['order']
CATALOG_IP = config['catalog']

## Buy the requested item number
@app.route("/buy/<int:item_number>")
def buy(item_number=None, topic=None):

    item_query = {
        "item_number": item_number
    }

    # NOTE: buy cannot be done with topic because only bezos can buy entire topics of books
    # if topic is not None:
    #     item_query = {
    #         "topic": topic
    #     }

    # first get the number that exist - note:
    num_items_response = requests.post(CATALOG_IP + '/query/', json=item_query).json()

    # no topic, reuse item_number
    book, amount = num_items_response.items()[0]

    # create update payload
    update_payload = {}
    update_payload[book] = amount-1

    response = requests.post(CATALOG_IP + '/update/', json=update_payload).json()

    # Use the 'status' boolean in json to check if the purchase was successful
    if response["Success"]:
        return {"status": True}
    else:
        return {"status": False}

if __name__ == "__main__":
    ORDER_PORT = config['order'].split(":")[2]
    app.run(host='0.0.0.0',port = ORDER_PORT)
