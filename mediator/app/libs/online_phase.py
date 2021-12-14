import jsonpickle
import numpy as np
import random
from app.helpers.utils import Singleton
from app.libs.mediator import Mediator
from app.constants import q


class OnlinePhase(metaclass=Singleton):
    _mediator = Mediator()

    def protocol_three(self, vendor_id, user_id, item_id):

        # Step 2
        q_nearst_neighbors = self.q_nearst_neighbors(item_id)

        # Step 3
        s_m = np.zeros(shape=(self._mediator.get_similarity_matrix().shape[0],))
        for index in q_nearst_neighbors:
            s_m[index] = self._mediator.get_similarity_matrix()[index, item_id]

        # Step 4
        random_multiplier = random.randint(1, 100)

        # Step 5
        encrypted_user_item_row = self._mediator.get_encrypted_user_item_matrix()[user_id, 1:]
        encrypted_mask_row = self._mediator.get_encrypted_mask()[user_id, 1:]
        random_vector = random_multiplier * s_m

        x = np.dot(encrypted_user_item_row, random_vector)
        y = np.dot(encrypted_mask_row, random_vector)

        return jsonpickle.encode({"x": x, "y": y})

    def q_nearst_neighbors(self, item_id):
        result = []
        item_col = self._mediator.get_similarity_matrix()[1:, item_id]
        item_col = np.concatenate(item_col[:item_id - 1], item_col[item_id:])
        sorted_item_col = np.argsort(item_col)[::-1]

        for i in range(q):
            if self._mediator.get_similarity_matrix()[sorted_item_col[i], item_id] == 0:
                break
            if sorted_item_col[i] != item_id:
                result.append(sorted_item_col[i])

        return result
