from flask import request
from flask_restx import Resource, Namespace

from app.libs.online_phase import OnlinePhase

api = Namespace('protocol_three')


@api.route('/protocol_three', doc=False)
class ProtocolThree(Resource):

    def post(self):
        try:
            data = request.json
            _, user_id, item_id = data['vendor_id'], data['user_id'], data['item_id']
            return OnlinePhase().protocol_three(user_id, item_id)

        except Exception as e:
            return {"message": str(e)}
