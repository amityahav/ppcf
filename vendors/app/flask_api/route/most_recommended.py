from flask import request
from flask_restx import Resource, Namespace, fields
from app.libs.online_phase import OnlinePhase
from app.constants import h

api = Namespace('most_recommended')

start_fields = api.model('get_top_h_unrated_items', {
    'vendor_id': fields.Integer(default=1),
    'user_id': fields.Integer()
})

responses = {
    200: "OK",
    400: "Bad Request"
}


@api.route('/most_recommended')
class Predict(Resource):

    @api.doc(description=f'Get the top {h} yet unrated items', responses=responses)
    @api.expect(start_fields)
    def post(self):
        try:
            data = request.json
            return OnlinePhase().protocol_four(data)

        except Exception as e:
            return {"message": str(e)}
