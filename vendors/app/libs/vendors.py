import numpy as np
import json
import jsonpickle
from app.helpers.utils import Singleton
from app.constants import SHARED_DIR_PATH, DATA_PATH


class Vendors(metaclass=Singleton):

    def __init__(self):
        self._vendors_list = []
        self._user_item_matrix = np.load(f'{DATA_PATH}/user_item_matrix.npy')

        with open(f'{DATA_PATH}/private_key.pk', 'r') as f:
            self.private_key = jsonpickle.decode(json.load(f))

        with open(f'{SHARED_DIR_PATH}/public_key.pk', 'r') as f:
            self.public_key = jsonpickle.decode(json.load(f))

    def add_vendor(self, vendor):
        self._vendors_list.append(vendor)

    def get_user_item_matrix(self):
        return self._user_item_matrix

    def get_he(self):
        return {
            "public_key": self.public_key,
            "private_key": self.private_key
        }

    def get_vendors(self):
        return self._vendors_list
