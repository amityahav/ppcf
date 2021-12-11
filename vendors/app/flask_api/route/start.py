from flask import jsonify, request
from flask_restx import Resource, Namespace, fields
from app.libs.offline_phase import OfflinePhase

api = Namespace('start')

start_fields = api.model('Start_Offline_Phase', {
    'number_of_vendors': fields.Integer(default=1)
})

responses = {
    200: "OK",
    400: "Bad Request"
}


@api.route('/start')
class Start(Resource):

    @api.doc(description=f'Start Offline Phase', responses=responses)
    @api.expect(start_fields)
    def post(self):
        try:
            data = request.json
            number_of_vendors = data['number_of_vendors']
            OfflinePhase().init_offline_phase(number_of_vendors)

            return {"message": "Offline Phase has completed successfully"}

        except Exception as e:
            return {"message": str(e)}
