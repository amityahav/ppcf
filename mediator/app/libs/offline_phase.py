import numpy as np
from app.helpers.utils import Singleton
from app.libs.mediator import Mediator
from app.constants import DATA_PATH


class OfflinePhase(metaclass=Singleton):
    _mediator = Mediator()

    def protocol_one(self, data):
        i, j, z1, z2, z3 = data["i"], data["j"], data["z1"], data["z2"], data["z3"]

        if z2 * z3 != 0:
            self._mediator.get_similarity_matrix()[i, j] = z1 / (z2 * z3) ** 0.5
            self._mediator.get_similarity_matrix()[j, i] = z1 / (z2 * z3) ** 0.5

    def protocol_two(self, encrypted_user_item_matrix, encrypted_mask, start, end):
        self.copy_arrays(np.array(encrypted_user_item_matrix), np.array(encrypted_mask), start, end)

    def save_similarity_matrix(self):
        np.save(f'{DATA_PATH}/similarity_matrix', self._mediator.get_similarity_matrix())

    def save_encrypted_matrices(self):
        np.save(f'{DATA_PATH}/encrypted_user_item_matrix', self._mediator.get_encrypted_user_item_matrix())
        np.save(f'{DATA_PATH}/encrypted_mask', self._mediator.get_encrypted_mask())

    def copy_arrays(self, enc_user_item, enc_mask, start, end):
        self._mediator.get_encrypted_user_item_matrix()[1:, start: end + 1] = enc_user_item
        self._mediator.get_encrypted_mask()[1:, start: end + 1] = enc_mask

