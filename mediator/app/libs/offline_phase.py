import numpy as np
from app.helpers.utils import Singleton
from app.libs.mediator import Mediator


class OfflinePhase(metaclass=Singleton):
    _mediator = Mediator()
    count = 0

    def protocol_one(self, data):
        i, j, z1, z2, z3 = data["i"], data["j"], data["z1"], data["z2"], data["z3"]

        if z2 * z3 != 0:
            self._mediator.get_similarity_matrix()[i, j] = z1 / (z2 * z3) ** 0.5
            self._mediator.get_similarity_matrix()[j, i] = z1 / (z2 * z3) ** 0.5

    def protocol_two(self, encrypted_user_item_matrix, encrypted_mask, start, end):
        self.copy_arrays(np.array(encrypted_user_item_matrix), np.array(encrypted_mask), start, end)

    def save_similarity_matrix(self):
        np.save('app/data/similarity_matrix', self._mediator.get_similarity_matrix())

    def save_encrypted_matrices(self):
        np.save('app/data/encrypted_user_item_matrix', self._mediator.get_encrypted_user_item_matrix())
        np.save('app/data/encrypted_mask', self._mediator.get_encrypted_mask())

    def copy_arrays(self, enc_user_item, enc_mask, start, end):  # TODO ENSURE CONCURRENCY WORKS
        self._mediator.get_encrypted_user_item_matrix()[:, start: end + 1] = enc_user_item
        self._mediator.get_encrypted_mask()[:, start: end + 1] = enc_mask
        # rows, columns = arr.shape
        # for i in range(rows):
        #     for j in range(columns):
        #         arr[i, j]._pyfhel = self._mediator.get_he()
        #         arr2[i, j]._pyfhel = self._mediator.get_he()
        #         self._mediator.get_encrypted_user_item_matrix()[i, start + j] = arr[i, j]
        #         self._mediator.get_encrypted_mask()[i, start + j] = arr2[i, j]
