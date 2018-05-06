from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import config

app = Flask(__name__)
db = SQLAlchemy(app)
app.config.from_object(config.app_config['testing'])
app.url_map.strict_slashes = False

api=Api(app)

from .views import UserSignupAPI
from .views import UserLoginAPI
from .views import MealsAPI
from .views import MenuAPI

api.add_resource(UserSignupAPI, '/api/v1/user/signup')
api.add_resource(MealsAPI, '/api/v1/meals', '/api/v1/meals/<meal_id>')
api.add_resource(UserLoginAPI, '/api/v1/user/login')
api.add_resource(MenuAPI, '/api/v1/menu')