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


class TestCatalog(unittest.TestCase):

    # Test to make sure that the topic query is correct
    def test_query_by_topic(self):
        topic_query = {
            "topic": "systems"
        }
        response = requests.post(CATALOG_IP + '/query/', json=topic_query).json()
        dict1 = {
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
            }
        }
        self.assertDictEqual(response, dict1)

        topic_query = {
            "topic": "gradschool"
        }
        response = requests.post(CATALOG_IP + '/query/', json=topic_query).json()
        dict2 = {
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
        self.assertDictEqual(response, dict2)
        print("PASSED: Query by topic yields correct dictionaries")

    # Test to make sure that query by item_id is correct
    def test_query_by_item(self):

        item_query = {
            "item_number": 1
        }
        response = requests.post(CATALOG_IP + '/query/', json=item_query).json()

        dict1 = list(response.values())[0]
        dict_keys = list(dict1.keys())

        self.assertIn("price", dict_keys)
        self.assertIn("stock", dict_keys)
        self.assertIn("item_number", dict_keys)
        self.assertIn("topic", dict_keys)
        print("PASSED: Query by item_id yields correct keys")

    # Test to make sure that updating the catalog server performs accordingly
    def test_update(self):

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
        original_amount = list(num_items_response.values())[0]["stock"]
        original_price = list(num_items_response.values())[0]["price"]

        # create update payload
        update_payload = {}
        update_payload[book] = num_items_response[book]
        if update_payload[book]["stock"] <= 0:
            return {"status": False}
        update_payload[book]["stock"] -= 1
        update_payload[book]["price"] -= 1

        response = requests.post(CATALOG_IP + '/update/', json=update_payload).json()
        self.assertTrue(response["Success"])

        # Query again to self assert
        num_items_response = requests.post(CATALOG_IP + '/query/', json=item_query).json()

        if len(num_items_response.keys()) == 0:
            return {"status": False}

        # no topic, reuse item_number
        updated_amount = list(num_items_response.values())[0]["stock"]
        updated_price = list(num_items_response.values())[0]["price"]

        self.assertEqual(original_price - updated_price, 1)
        self.assertEqual(original_amount - updated_amount, 1)
        print("PASSED: Decrease stock & price operation correct")


if __name__ == "__main__":
    unittest.main()
