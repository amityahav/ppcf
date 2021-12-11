import numpy as np

user_item = np.zeros(shape=(944, 1683), dtype='int32')  # users and items indices start from 1

with open("raw_data/u1.base", 'r', encoding='utf-8') as training_set:
    for line in training_set:  # user id | item id | rating | timestamp
        record = list(map(int, line.split('\t')))
        user_item[record[0], record[1]] = record[2]

np.save('user_item_matrix', user_item)
