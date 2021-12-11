from flask import Flask
from .flask_api import api
from app.libs.vendors import Vendors

app = Flask(__name__)
app.register_blueprint(api.api_bp)

Vendors()
