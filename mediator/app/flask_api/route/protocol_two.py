import jsonpickle
from flask import jsonify, request
from flask_restx import Resource, Namespace, fields

from app.libs.offline_phase import OfflinePhase

api = Namespace('protocol_two')


@api.route('/protocol_two')
class ProtocolTwo(Resource):

    @api.doc(doc=False)
    def post(self):
        try:
            data = jsonpickle.decode(request.get_json())
            OfflinePhase().protocol_two(data)
        except Exception as e:
            return {"message": str(e)}

    def put(self):
        OfflinePhase().save_encrypted_matrices()

