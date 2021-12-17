
from flask_restx import Resource, Namespace
from app.libs.online_phase import OnlinePhase

api = Namespace('error_rate')


responses = {
    200: "OK",
    400: "Bad Request"
}


@api.route('/error_rate')
class Predict(Resource):

    @api.doc(description=f'Get Model\'s Error rate', responses=responses)
    def post(self):
        try:
            return OnlinePhase().compute_error()

        except Exception as e:
            return {"message": str(e)}
