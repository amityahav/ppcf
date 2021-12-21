import jsonpickle
import numpy as np
import random
from app.helpers.utils import Singleton
from app.libs.mediator import Mediator
from app.constants import q


class OnlinePhase(metaclass=Singleton):
    _mediator = Mediator()

    def protocol_three(self, user_id, item_id):

        # Step 2
        q_nearst_neighbors = self.q_nearst_neighbors(item_id)

        # Step 3
        s_m = np.zeros(shape=(self._mediator.get_similarity_matrix().shape[0] - 1,))
        for index in q_nearst_neighbors:
            s_m[index - 1] = self._mediator.get_similarity_matrix()[index, item_id]

        # Step 4
        random_multiplier = random.randint(1, 100)

        # Step 5
        encrypted_user_item_row = self._mediator.get_encrypted_user_item_matrix()[user_id, 1:]
        encrypted_mask_row = self._mediator.get_encrypted_mask()[user_id, 1:]
        random_vector = random_multiplier * s_m

        x = np.dot(encrypted_user_item_row, random_vector)
        y = np.dot(encrypted_mask_row, random_vector)

        return jsonpickle.encode({"x": x, "y": y})

    def protocol_four(self, data):
        vendor_id, user_id, start, end = data['vendor_id'], data['user_id'], data['start'], data['end']

        # Step 2
        q_nearst_neighbors_lists = [self.q_nearst_neighbors(item, protocol_four=True) for item in range(start, end + 1)]
        s_m_matrix = np.zeros(shape=(self._mediator.get_similarity_matrix().shape[0] - 1, end - start + 1))
        for item_id, lst in enumerate(q_nearst_neighbors_lists):
            for index in lst:
                s_m_matrix[index - 1, item_id] = self._mediator.get_similarity_matrix()[index, item_id + start]

        # Step 3
        random_multiplier = random.randint(1, 100)

        # Step 4
        encrypted_mask_row = self._mediator.get_encrypted_mask()[user_id, 1:]
        random_vectors = random_multiplier * s_m_matrix
        x = np.array([np.dot(encrypted_mask_row, random_vectors[:, item]) for item in range(end - start + 1)])

        # Step 5
        public_key = self._mediator.get_public_key()
        y = np.copy(encrypted_mask_row[start - 1: end])
        for i in range(y.shape[0]):
            y[i] = y[i] + public_key.encrypt(0)

        # Step 6
        random_shift_factor = random.randint(1, 100)
        self._mediator.set_random_shifter(random_shift_factor)
        x, y = self.random_permutation(x), self.random_permutation(y)
        return jsonpickle.encode({"x": x, "y": y})

    def random_permutation(self, arr):
        return np.roll(arr, self._mediator.get_random_shifter())

    def invert_random_permutation(self, data):
        permutation = data['x']
        length = data['length']
        random_shift_factor = self._mediator.get_random_shifter()
        original_indices = [(index - random_shift_factor) % length for index in permutation]
        return jsonpickle.encode({"result": np.random.permutation(original_indices)})

    def q_nearst_neighbors(self, item_id, protocol_four=False):
        result = []
        item_col = self._mediator.get_similarity_matrix()[:, item_id]
        sorted_item_col = np.argsort(item_col)[::-1]
        index = np.argwhere(sorted_item_col == item_id)
        sorted_item_col = np.delete(sorted_item_col, index)
        index_0 = np.argwhere(sorted_item_col == 0)
        sorted_item_col = np.delete(sorted_item_col, index_0)

        for i in range(q):
            if not protocol_four and self._mediator.get_similarity_matrix()[sorted_item_col[i], item_id] == 0:
                break
            result.append(sorted_item_col[i])

        return result
