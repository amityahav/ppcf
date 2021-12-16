import requests
import json
import jsonpickle
import math

from app.libs.vendors import Vendors
from app.helpers.utils import Singleton
from app.constants import MEDIATOR_PROTOCOL_THREE_ENDPOINT, VENDORS_PREDICT_ENDPOINT, TEST_SET_PATH


class OnlinePhase(metaclass=Singleton):
    _vendors = Vendors()
    _headers = {'Content-type': 'application/json'}

    def protocol_three(self, data):
        # Step 1
        vendor_id, item_id = data['vendor_id'], data['item_id']

        if not self.is_valid_item(vendor_id, item_id):
            return {"message": f"Invalid Item Id for Vendor#{vendor_id}"}
        response = requests.post(MEDIATOR_PROTOCOL_THREE_ENDPOINT, data=json.dumps(data), headers=self._headers)

        # Step 6
        private_key = self._vendors.get_he()['private_key']
        data = jsonpickle.decode(json.loads(response.content))
        x, y = private_key.decrypt(data['x']), private_key.decrypt(data['y'])

        # Step 7
        start, _ = self._vendors.get_vendors()[vendor_id].get_item_range()
        item_rating_average = self._vendors.get_vendors()[vendor_id].get_average_ratings()[item_id - start]
        div = x / y if y != 0 else 0
        prediction = round(item_rating_average + div)

        return {"message": {
            "item_id": item_id,
            "prediction": prediction
        }}

    def compute_error(self):

        errors = []
        with open(TEST_SET_PATH, 'r') as test_set:
            for line in test_set:  # user id | item id | rating | timestamp
                user_id, item_id, rating, _ = list(map(int, line.split('\t')))
                vendor_id = self.find_vendor_for_item(item_id)
                fields = {
                    "vendor_id": vendor_id,
                    "user_id": user_id,
                    "item_id": item_id
                }
                response = requests.post(VENDORS_PREDICT_ENDPOINT, json.dumps(fields), headers=self._headers)
                data = json.loads(response.content)
                prediction = data['message']['prediction']
                errors.append(abs(rating - prediction))
        return {"message":
                {"error_rate": sum(errors) / len(errors)}}

    def find_vendor_for_item(self, item_id):

        total_amount_of_items = self._vendors.get_user_item_matrix().shape[1] - 1
        number_of_vendors = self._vendors.get_number_of_vendors()
        items_per_vendor = math.floor(total_amount_of_items / number_of_vendors)

        remainder = 1 if item_id % items_per_vendor != 0 else 0
        quotient = item_id // items_per_vendor

        vendor_id = quotient + remainder - 1

        return vendor_id

    def is_valid_item(self, vendor_id, item_id):
        vendor = self._vendors.get_vendors()[vendor_id]
        return vendor.is_valid_item(item_id)
