import jsonpickle
from flask import request
from flask_restx import Resource, Namespace
from app.libs.offline_phase import OfflinePhase

api = Namespace('protocol_two')


@api.route('/protocol_two')
class ProtocolTwo(Resource):

    @api.doc(doc=False)
    def post(self):
        try:
            data = jsonpickle.decode(request.get_json())
            enc_user_item_matrix, enc_mask, start, end = data["enc_user_item_matrix"], data["enc_mask"], data["start"], data["end"]
            OfflinePhase().protocol_two(enc_user_item_matrix, enc_mask, start, end)
        except Exception as e:
            return {"message": str(e)}

    def put(self):
        OfflinePhase().save_encrypted_matrices()


