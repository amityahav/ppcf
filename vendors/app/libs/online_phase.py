import requests
import json
import jsonpickle
import math
import numpy as np
import threading

from app.libs.vendors import Vendors
from app.helpers.utils import Singleton
from app.constants import MEDIATOR_PROTOCOL_THREE_ENDPOINT, MEDIATOR_PROTOCOL_FOUR_ENDPOINT, \
    VENDORS_PREDICT_ENDPOINT, TEST_SET_PATH, h


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
        item_info_map = self._vendors.get_info_map()

        return {"message": {
            "item": f'{item_id}: {item_info_map[str(item_id)]}',
            "prediction": prediction
        }}

    def protocol_four(self, data):
        # Step 1
        vendor_id, user_id = data['vendor_id'], data['user_id']
        start, end = self._vendors.get_vendors()[vendor_id].get_item_range()
        data['start'], data['end'] = start, end
        response = requests.post(MEDIATOR_PROTOCOL_FOUR_ENDPOINT, data=json.dumps(data), headers=self._headers)

        # Step 7
        private_key = self._vendors.get_he()['private_key']
        data = jsonpickle.decode(json.loads(response.content))
        x = [private_key.decrypt(n) for n in data['x']]
        y = [private_key.decrypt(n) for n in data['y']]

        # Step 8
        x_sorted = np.argsort(x)[::-1]
        result = []
        number_of_recs = h
        item_info_map = self._vendors.get_info_map()

        for index in x_sorted:
            if number_of_recs == 0:
                break

            if y[index] == 0:
                result.append(index + start)
                number_of_recs = number_of_recs - 1

        return {"message": {
            "user_id": user_id,
            f'{h} most recommended items': [f'{i}: {item_info_map[str(i)]}' for i in result]
        }}

    def compute_error(self):
        errors = []

        with open(TEST_SET_PATH, 'r') as test_set:

            lines = np.array(test_set.readlines())
            lines = np.split(lines, 40)
            threads = []

            for line in lines:
                thread = threading.Thread(target=lambda: self.error_calc(line, errors))
                threads.append(thread)
                thread.start()

            for thread in threads:
                thread.join()

        return {"message":
                {"error_rate": sum(errors) / len(errors)}}

    def error_calc(self, lines, errors):
        for line in lines:  # user id | item id | rating | timestamp
            user_id, item_id, rating, _ = list(map(int, line.split('\t')))
            vendor_id = self.find_vendor_for_item(item_id)
            fields = {
                "vendor_id": vendor_id,
                "user_id": user_id,
                "item_id": item_id
            }
            response = requests.post(VENDORS_PREDICT_ENDPOINT, json.dumps(fields), headers=self._headers)
            data = json.loads(response.content)
            prediction = int(data['message']['prediction'])
            errors.append(abs(rating - prediction))

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
