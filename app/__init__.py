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
app.config.from_object(config.app_config['development'])

api=Api(app)

from .views import UserSignupAPI
from .views import UserLoginAPI
from .views import MealsAPI
from .models import User
from .models import Meal

api.add_resource(UserSignupAPI, '/api/v1/user/signup')
api.add_resource(MealsAPI, '/api/v1/meals')
api.add_resource(UserLoginAPI, '/api/v1/user/login')