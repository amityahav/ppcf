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

        response = requests.post(MEDIATOR_PROTOCOL_THREE_ENDPOINT, data=json.dumps(data), headers=self._headers)
