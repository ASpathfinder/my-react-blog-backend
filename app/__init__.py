from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from . config import Config
from flask_cors import CORS
from flask_jwt_extended import JWTManager

sa = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(Config)
    app.config.from_pyfile('config.py')

    sa.init_app(app)
    migrate.init_app(app, sa)
    jwt.init_app(app)
    CORS(app, supports_credentials=True)

    from . api import api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api')

    return app


