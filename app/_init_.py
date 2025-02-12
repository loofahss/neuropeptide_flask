from flask import Flask
from .routes import api_bp  # 导入蓝图
from flask_cors import CORS
def create_app():
    app = Flask(__name__)
    CORS(app, resources={r"/*": {"origins": "*"}})
    # 注册蓝图
    app.register_blueprint(api_bp, url_prefix='/api')  # 将所有路由的 URL 前缀设置为 /api
    
    return app
