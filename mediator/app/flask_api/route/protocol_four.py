from flask import request
from flask_restx import Resource, Namespace
from app.libs.online_phase import OnlinePhase

api = Namespace('protocol_four')


@api.route('/protocol_four')
class ProtocolFour(Resource):

    @api.doc(doc=False)
    def post(self):
        try:
            data = request.json
            return OnlinePhase().protocol_four(data)

        except Exception as e:
            return {"message": str(e)}

