from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from config import app_config


app = Flask(__name__)
db = SQLAlchemy(app)
app.config.from_object(app_config['development'])

api=Api(app)
bcrypt = Bcrypt(app)
from .views import UserSignupAPI
from .models import User
api.add_resource(UserSignupAPI, '/api/v1/user/signup')