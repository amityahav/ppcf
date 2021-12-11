from flask import Blueprint
from flask_restx import Api

from app.flask_api.route.start import api as start
from app.flask_api.route.predict import api as predict

api_bp = Blueprint('api', __name__)
api = Api(api_bp, version='1', title='Vendors', doc='/')
api_prefix = "/vendors"
# Register API routes
api.add_namespace(start, path=api_prefix)
api.add_namespace(predict, path=api_prefix)
