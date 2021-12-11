from flask import Flask
from .flask_api import api

app = Flask(__name__)
app.register_blueprint(api.api_bp)
