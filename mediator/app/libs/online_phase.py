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

    def q_nearst_neighbors(self, item_id):
        result = []
        item_col = self._mediator.get_similarity_matrix()[:, item_id]
        sorted_item_col = np.argsort(item_col)[::-1]

        for i in range(q):
            if self._mediator.get_similarity_matrix()[sorted_item_col[i], item_id] == 0:
                break
            result.append(sorted_item_col[i])

        return result
