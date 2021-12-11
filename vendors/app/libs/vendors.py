import numpy as np
from Pyfhel import Pyfhel
from app.helpers.utils import Singleton
from app.constants import SHARED_DIR_PATH


class Vendors(metaclass=Singleton):

    def __init__(self):
        self._vendors_list = []
        self._user_item_matrix = np.load('app/data/user_item_matrix.npy')
        self._HE = Pyfhel()
        self.init_encryption()

    def init_encryption(self):
        self._HE.contextGen(p=65537, m=2 ** 12)
        self._HE.keyGen()
        self._HE.saveContext(f'{SHARED_DIR_PATH}/context.con')
        self._HE.savepublicKey(f'{SHARED_DIR_PATH}/publickey.pk')

    def add_vendor(self, vendor):
        self._vendors_list.append(vendor)

    def get_user_item_matrix(self):
        return self._user_item_matrix

    def get_he(self):
        return self._HE

    def get_vendors(self):
        return self._vendors_list
