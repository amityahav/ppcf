import json
import math
import random
import threading
from pathlib import Path

import jsonpickle
import numpy as np
import requests

from app.constants import MEDIATOR_PROTOCOL_ONE_ENDPOINT, MEDIATOR_PROTOCOL_TWO_ENDPOINT, SIMILARITY_MATRIX_PATH, \
                          ENCRYPTED_USER_ITEM_PATH, ENCRYPTED_MASK_PATH
from app.helpers.utils import Singleton
from app.libs.vendor import Vendor
from app.libs.vendors import Vendors


class OfflinePhase(metaclass=Singleton):
    _vendors = Vendors()
    _headers = {'Content-type': 'application/json'}

    def init_offline_phase(self, number_of_vendors):
        total_amount_of_items = self._vendors.get_user_item_matrix().shape[1] - 1
        items_per_vendor = math.floor(total_amount_of_items / number_of_vendors)
        threads = []

        for i in range(number_of_vendors):
            start = i * items_per_vendor + 1
            end = i * items_per_vendor + items_per_vendor if i != number_of_vendors - 1 else total_amount_of_items
            vendor = Vendor(start, end, self._vendors.get_he(), self._vendors.get_user_item_matrix())
            self._vendors.add_vendor(vendor)

        if not Path(SIMILARITY_MATRIX_PATH).is_file():
            # PROTOCOL 1
            for j in range(number_of_vendors):
                for k in range(j, number_of_vendors):
                    thread = threading.Thread(target=lambda: self.protocol_one(self._vendors.get_vendors()[j],
                                                                               self._vendors.get_vendors()[k]))
                    threads.append(thread)
                    thread.start()

            for thread in threads:
                thread.join()

            requests.put(MEDIATOR_PROTOCOL_ONE_ENDPOINT)

        threads = []

        # PROTOCOL 2
        for i in range(number_of_vendors):
            thread = threading.Thread(target=lambda: self.protocol_two(self._vendors.get_vendors()[i]))
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

        if Path(ENCRYPTED_USER_ITEM_PATH).is_file() and Path(ENCRYPTED_MASK_PATH).is_file():
            return

        requests.put(MEDIATOR_PROTOCOL_TWO_ENDPOINT)

    def protocol_one(self, v_j, v_k):

        # STEP 1
        random_multiplier = random.randint(1, 100)
        v_j_item_range = v_j.get_item_range()
        v_k_item_range = v_k.get_item_range()

        for i in range(v_j_item_range[0], v_j_item_range[1] + 1):

            for j in range(v_k_item_range[0], v_k_item_range[1] + 1):
                v_j_item_col = v_j.get_item_ratings(i)
                v_k_item_col = v_k.get_item_ratings(j)

                # STEP 2 + 3 + 4
                z1 = np.dot(random_multiplier * v_j_item_col, v_k_item_col).item()
                z2 = random_multiplier * np.dot(v_j_item_col, v_j_item_col).item()
                z3 = random_multiplier * np.dot(v_k_item_col, v_k_item_col).item()

                data = {
                    "i": i,
                    "j": j,
                    "z1": z1,
                    "z2": z2,
                    "z3": z3
                }
                requests.post(MEDIATOR_PROTOCOL_ONE_ENDPOINT, data=json.dumps(data), headers=self._headers)

    def protocol_two(self, v_j):

        start, end = v_j.get_item_range()

        # Step 1 + 2
        items = self._vendors.get_user_item_matrix()[1:, start: end + 1]
        mask = self.mask(items)
        ratings_sum = np.sum(items, axis=0, dtype='float32')
        mask_sum = np.sum(mask, axis=0, dtype='float32')
        average_ratings = np.divide(ratings_sum, mask_sum, out=np.zeros_like(ratings_sum), where=mask_sum != 0)
        adjusted_items_ratings = np.subtract(items, average_ratings) * mask

        v_j.set_average_ratings(average_ratings)

        if Path(ENCRYPTED_USER_ITEM_PATH).is_file() and Path(ENCRYPTED_MASK_PATH).is_file():
            return

        # Step 4
        rows, cols = mask.shape
        adjusted_items_ratings = adjusted_items_ratings.tolist()
        mask = mask.tolist()

        encrypted_user_item_matrix, encrypted_mask = self.encrypt_matrices(adjusted_items_ratings, mask, rows, cols)

        requests.post(MEDIATOR_PROTOCOL_TWO_ENDPOINT,
                      data=json.dumps(jsonpickle.encode({
                          "enc_user_item_matrix": encrypted_user_item_matrix,
                          "enc_mask": encrypted_mask,
                          "start": start,
                          "end": end
                      })),
                      headers=self._headers)

    @staticmethod
    def mask(matrix):
        return matrix > 0

    def encrypt_matrices(self, user_item, mask, rows, cols):
        count = 0
        public_key = self._vendors.get_he()["public_key"]
        zero = public_key.encrypt(0)
        one = public_key.encrypt(1)
        enc_user_item = []
        enc_mask = []
        for i in range(rows):
            new_row1 = []
            new_row2 = []
            for j in range(cols):
                if user_item[i][j] == 0:
                    new_row1.append(zero)
                else:
                    new_row1.append(public_key.encrypt(user_item[i][j]))

                if mask[i][j] == 0:
                    new_row2.append(zero)
                else:
                    new_row2.append(one)
                print(count)
                count += 1
            enc_user_item.append(new_row1)
            enc_mask.append(new_row2)
        return enc_user_item, enc_mask
