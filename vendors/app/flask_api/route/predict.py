from flask import jsonify, request
from flask_restx import Resource, Namespace, fields
from app.libs.online_phase import OnlinePhase

api = Namespace('predict')

start_fields = api.model('Predict_rating', {
    'vendor_id': fields.Integer(default=1),
    'user_id': fields.Integer(),
    'item_id': fields.Integer()
})

responses = {
    200: "OK",
    400: "Bad Request"
}


@api.route('/predict')
class Predict(Resource):

    @api.doc(description=f'Get Prediction for a rating', responses=responses)
    @api.expect(start_fields)
    def post(self):
        try:
            data = request.json
            OnlinePhase().protocol_three(data)

        except Exception as e:
            return {"message": str(e)}
