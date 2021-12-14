import requests
import json

from app.libs.vendors import Vendors
from app.libs.vendor import Vendor
from app.helpers.utils import Singleton
from app.constants import MEDIATOR_PROTOCOL_THREE_ENDPOINT


class OnlinePhase(metaclass=Singleton):
    _vendors = Vendors()
    _headers = {'Content-type': 'application/json'}

    def protocol_three(self, data):
        vendor_id, item_id = data['vendor_id'], data['item_id']

        if not self.is_valid_item(vendor_id, item_id):
            return {"message": f"Invalid Item Id for Vendor#{vendor_id}"}
        response = requests.post(MEDIATOR_PROTOCOL_THREE_ENDPOINT, data=json.dumps(data), headers=self._headers)

    def is_valid_item(self, vendor_id, item_id):
        vendor = self._vendors.get_vendors()[vendor_id]
        return vendor.is_valid_item(item_id)
