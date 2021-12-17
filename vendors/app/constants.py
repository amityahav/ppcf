MEDIATOR_API_BASE = 'http://127.0.0.1:5001/mediator'
MEDIATOR_PROTOCOL_ONE_ENDPOINT = f'{MEDIATOR_API_BASE}/protocol_one'
MEDIATOR_PROTOCOL_TWO_ENDPOINT = f'{MEDIATOR_API_BASE}/protocol_two'
MEDIATOR_PROTOCOL_THREE_ENDPOINT = f'{MEDIATOR_API_BASE}/protocol_three'
MEDIATOR_PROTOCOL_FOUR_ENDPOINT = f'{MEDIATOR_API_BASE}/protocol_four'

VENDORS_API_BASE = 'http://127.0.0.1:5000/vendors'
VENDORS_PREDICT_ENDPOINT = f'{VENDORS_API_BASE}/predict'

SHARED_DIR_PATH = '../shared/'
DATA_PATH = 'app/data'
ITEMS_INFO_PATH = f'{DATA_PATH}/raw_data/u.item'
SIMILARITY_MATRIX_PATH = '../mediator/app/data/similarity_matrix.npy'
ENCRYPTED_USER_ITEM_PATH = '../mediator/app/data/encrypted_user_item_matrix.npy'
ENCRYPTED_MASK_PATH = '../mediator/app/data/encrypted_mask.npy'

TEST_SET_PATH = 'app/data/raw_data/u1.test'

h = 4
