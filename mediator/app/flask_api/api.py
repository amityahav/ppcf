from flask import Blueprint
from flask_restx import Api

from app.flask_api.route.protocol_one import api as protocol_one
from app.flask_api.route.protocol_two import api as protocol_two
from app.flask_api.route.protocol_three import api as protocol_three


api_bp = Blueprint('api', __name__)
api = Api(api_bp, version='1', title='Mediator', doc='/')
api_prefix = "/mediator"
# Register API routes
api.add_namespace(protocol_one, path=api_prefix)
api.add_namespace(protocol_two, path=api_prefix)
api.add_namespace(protocol_three, path=api_prefix)
