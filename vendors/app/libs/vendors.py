import numpy as np
import json
import jsonpickle
from app.helpers.utils import Singleton
from app.constants import SHARED_DIR_PATH, DATA_PATH, ITEMS_INFO_PATH


class Vendors(metaclass=Singleton):

    def __init__(self):
        self._vendors_list = []
        self._user_item_matrix = np.load(f'{DATA_PATH}/user_item_matrix.npy')
        self._number_of_vendors = 0
        self._items_info = {}
        self.load_items_info()

        with open(f'{DATA_PATH}/private_key.pk', 'r') as f:
            self._private_key = jsonpickle.decode(json.load(f))

        with open(f'{SHARED_DIR_PATH}/public_key.pk', 'r') as f:
            self._public_key = jsonpickle.decode(json.load(f))

    def load_items_info(self):
        with open(ITEMS_INFO_PATH, 'r', encoding="ISO-8859-1") as info:
            for line in info:  # item_id | item_name | ...
                item_id, item_name, *_ = line.split('|')
                self._items_info[item_id] = item_name

    def set_number_of_vendors(self, num):
        self._number_of_vendors = num

    def add_vendor(self, vendor):
        self._vendors_list.append(vendor)

    def get_info_map(self):
        return self._items_info

    def get_number_of_vendors(self):
        return self._number_of_vendors

    def get_user_item_matrix(self):
        return self._user_item_matrix

    def get_he(self):
        return {
            "public_key": self._public_key,
            "private_key": self._private_key
        }

    def get_vendors(self):
        return self._vendors_list
