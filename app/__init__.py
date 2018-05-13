from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy


import config
db = SQLAlchemy()


def create_app(config_name):

    app = Flask(__name__)
    app.config.from_object(config.app_config[config_name])
    app.url_map.strict_slashes = False

    db.init_app(app)
    api=Api(app)

    from .views import UserSignupAPI
    from .views import UserLoginAPI
    from .views import MealsAPI

    api.add_resource(UserSignupAPI, '/api/v1/user/signup')
    api.add_resource(MealsAPI, '/api/v1/meals', '/api/v1/meals/<meal_id>')
    api.add_resource(UserLoginAPI, '/api/v1/user/login')

    return app