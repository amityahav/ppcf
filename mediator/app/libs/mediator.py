import numpy as np
import json
import jsonpickle

from pathlib import Path
from app.helpers.utils import Singleton
from app.constants import NUMBER_OF_ITEMS, NUMBER_OF_USERS, SHARED_DIR_PATH, SIMILARITY_MATRIX_PATH, \
                          ENCRYPTED_USER_ITEM_PATH, ENCRYPTED_MASK_PATH


class Mediator(metaclass=Singleton):

    def __init__(self):

        if not Path(SIMILARITY_MATRIX_PATH).is_file():
            self._similarity_matrix = np.zeros(shape=(NUMBER_OF_ITEMS + 1, NUMBER_OF_ITEMS + 1))
        else:
            self._similarity_matrix = np.load(SIMILARITY_MATRIX_PATH)

        if Path(ENCRYPTED_USER_ITEM_PATH).is_file() and Path(ENCRYPTED_MASK_PATH).is_file():
            np_load_old = np.load
            np.load = lambda *a, **k: np_load_old(*a, allow_pickle=True, **k)
            self._encrypted_user_item_matrix = np.load(ENCRYPTED_USER_ITEM_PATH)
            self._encrypted_masked = np.load(ENCRYPTED_MASK_PATH)
            # restore np.load for future normal usage
            np.load = np_load_old
        else:
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

