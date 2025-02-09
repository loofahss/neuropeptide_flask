from flask import Flask
from flask_cors import CORS
from app.routes import init_routes

def create_app():
    app = Flask(__name__)
    CORS(app, resources={r"/*": {"origins": "*"}})
    init_routes(app)

    return app
