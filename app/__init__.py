from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import config

app = Flask(__name__)
db = SQLAlchemy(app)
app.config.from_object(config.app_config['development'])

api=Api(app)
bcrypt = Bcrypt(app)
from .views import UserSignupAPI
from .models import User
api.add_resource(UserSignupAPI, '/api/v1/user/signup')