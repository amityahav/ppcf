import numpy as np

from Pyfhel import Pyfhel
from app.helpers.utils import Singleton
from app.constants import NUMBER_OF_ITEMS, NUMBER_OF_USERS, PUBLIC_KEY_PATH, CONTEXT_PATH


class Mediator(metaclass=Singleton):

    def __init__(self):
        self._similarity_matrix = np.zeros(shape=(NUMBER_OF_ITEMS + 1, NUMBER_OF_ITEMS + 1))
        self._encrypted_user_item_matrix = np.empty(shape=(NUMBER_OF_USERS + 1, NUMBER_OF_ITEMS + 1), dtype='object')
        self._encrypted_masked = np.empty(shape=(NUMBER_OF_USERS + 1, NUMBER_OF_ITEMS + 1), dtype='object')
        self._HE = Pyfhel()
        self.init_encryption()

    def init_encryption(self):
        self._HE.restoreContext(CONTEXT_PATH)
        self._HE.restorepublicKey(PUBLIC_KEY_PATH)

    def get_similarity_matrix(self):
        return self._similarity_matrix

    def get_encrypted_user_item_matrix(self):
        return self._encrypted_user_item_matrix

    def get_encrypted_mask(self):
        return self._encrypted_masked

    def get_he(self):
        return self._HE
