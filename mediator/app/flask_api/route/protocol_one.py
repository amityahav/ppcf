from flask import request
from flask_restx import Resource, Namespace
from app.libs.offline_phase import OfflinePhase

api = Namespace('protocol_one')


@api.route('/protocol_one')
class ProtocolOne(Resource):

    @api.doc(doc=False)
    def post(self):
        try:
            data = request.json
            OfflinePhase().protocol_one(data)

        except Exception as e:
            return {"message": str(e)}

    def put(self):
        OfflinePhase().save_similarity_matrix()
