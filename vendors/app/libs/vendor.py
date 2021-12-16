

class Vendor:

    def __init__(self, start, end, he, user_item_matrix):

        self._start = start
        self._end = end
        self._he = he
        self._user_item_matrix = user_item_matrix
        self._average_ratings = None

    def is_valid_item(self, index):
        if index > self._end or index < self._start:
            return False
        return True

    def get_item_ratings(self, index):

        if not self.is_valid_item(index):
            raise "out of bounds"
        return self._user_item_matrix[1:, index]

    def get_item_range(self):

        return self._start, self._end

    def get_average_ratings(self):
        return self._average_ratings

    def set_average_ratings(self, avg_ratings):
        self._average_ratings = avg_ratings

