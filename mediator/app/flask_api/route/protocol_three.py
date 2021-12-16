from flask import request
from flask_restx import Resource, Namespace

from app.libs.online_phase import OnlinePhase

api = Namespace('protocol_three')


@api.route('/protocol_three')
class ProtocolThree(Resource):

    @api.doc(doc=False)
    def post(self):
        try:
            data = request.json
            vendor_id, user_id, item_id = data['vendor_id'], data['user_id'], data['item_id']
            return OnlinePhase().protocol_three(vendor_id, user_id, item_id)

        except Exception as e:
            return {"message": str(e)}
