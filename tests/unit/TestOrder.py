import unittest
import requests
import yaml
import os.path

# Load Server configs from yaml
with open(os.path.dirname(os.path.realpath('__file__')) + '/../../src/config.yml', 'r') as file:
    config = yaml.load(file, Loader=yaml.FullLoader)

FRONTEND_IP = config['frontend']
ORDER_IP = config['order']
CATALOG_IP = config['catalog']


class TestOrder(unittest.TestCase):

    def test_buy(self):

        # Set the stock of item_id 1 to 1

        # Check to make sure that updating the stock number performs accordingly
        item_query = {
            "item_number": 1
        }
        # first get the number that exist - note:
        num_items_response = requests.post(CATALOG_IP + '/query/', json=item_query).json()

        if len(num_items_response.keys()) == 0:
            return {"status": False}

        # no topic, reuse item_number
        book = list(num_items_response.keys())[0]
        amount = list(num_items_response.values())[0]["stock"]

        # create update payload
        update_payload = {}
        update_payload[book] = num_items_response[book]
        update_payload[book]["stock"] -= (amount-1)

        response = requests.post(CATALOG_IP + '/update/', json=update_payload).json()
        self.assertTrue(response["Success"])

        # Purchase the only item left in item_id 1
        first_response = requests.post(ORDER_IP + '/buy/' + "1").json()
        first_buy = first_response["status"]
        self.assertTrue(first_buy)
        print("PASSED: Buy with positive stock successful")

        # Try to purchase the zero stock
        second_response = requests.post(ORDER_IP + '/buy/' + "1").json()
        second_buy = second_response["status"]
        self.assertFalse(second_buy)
        print("PASSED: Buy with zero stock unsuccessful")


if __name__ == "__main__":
    unittest.main()