import numpy as np
import json
import jsonpickle


from app.helpers.utils import Singleton
from app.constants import NUMBER_OF_ITEMS, NUMBER_OF_USERS, SHARED_DIR_PATH


class Mediator(metaclass=Singleton):

    def __init__(self):
        self._similarity_matrix = np.zeros(shape=(NUMBER_OF_ITEMS + 1, NUMBER_OF_ITEMS + 1))
        self._encrypted_user_item_matrix = np.empty(shape=(NUMBER_OF_USERS + 1, NUMBER_OF_ITEMS + 1), dtype='object')
        self._encrypted_masked = np.empty(shape=(NUMBER_OF_USERS + 1, NUMBER_OF_ITEMS + 1), dtype='object')

        with open(f'{SHARED_DIR_PATH}/public_key.pk', 'r') as f:
            self._public_key = jsonpickle.decode(json.load(f))

    def get_similarity_matrix(self):
        return self._similarity_matrix

    def get_encrypted_user_item_matrix(self):
        return self._encrypted_user_item_matrix

    def get_encrypted_mask(self):
        return self._encrypted_masked

