# from app import create_app

# app = create_app()

# if __name__ == "__main__":
#     app.run(debug=True)
from flask import Flask
from flask_cors import CORS
app = Flask(__name__)
from api.routes import api
CORS(app, resources={r"/*": {"origins": "*"}})
app.register_blueprint(api)
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000,debug=True)
