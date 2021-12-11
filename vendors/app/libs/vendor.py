

class Vendor:

    def __init__(self, start, end, he, user_item_matrix):

        self._start = start
        self._end = end
        self._he = he
        self._user_item_matrix = user_item_matrix

    def get_item_ratings(self, index):

        if index > self._end or index < self._start:
            raise Exception("out of bounds")
        return self._user_item_matrix[:, index]

    def get_item_range(self):

        return self._start, self._end

