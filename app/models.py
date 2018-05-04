import sys
import os
from datetime import datetime, timedelta
import jwt
from flask import current_app
from werkzeug.security import generate_password_hash, check_password_hash
import app

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

db = app.db


class Base(db.Model):
    __abstract__ = True
    __table_args__ = {'extend_existing': True}
    def save(self):
        """Save to the database"""
        db.session.add(self)
        db.session.commit()

    def delete(self):
        """Delete from the database"""
        db.session.delete(self)
        db.session.commit()

class User(Base):
    
    __tablename__ = 'user'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, index=True,nullable=False, unique=True)
    email = db.Column(db.String, index=True,nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    admin = db.Column(db.Boolean, default=False)
    
    def __init__(self,username, email, password ):
        self.password = generate_password_hash(password)
        self.username = username
        self.email = email

    def make_user_admin(self):
        self.admin = True
        self.save()

    @staticmethod
    def get_all():
        return User.query.all()

    @staticmethod
    def get(**kwargs):
        """This method gets a user."""
        return User.query.filter_by(**kwargs).first()    

    def password_is_valid(self, password):
        """
        Checks the password against it's hash to validate the user's password
        """
        return check_password_hash(self.password, password)
    
    def generate_token(self):
        payload = {'exp': datetime.utcnow()+timedelta(minutes=60),
                    'iat': datetime.utcnow(),
                    'username': self.username}
        token = jwt.encode(payload, current_app.config.get('SECRET'), algorithm='HS256')
        return token.decode()
    
    @staticmethod
    def decode_token(token):
        payload = jwt.decode(token, current_app.config.get('SECRET'), algorithms=['HS256'])
        return payload['username']

class Meal(Base):

    __tablename__ = 'meal'

    id = db.Column(db.Integer, primary_key=True)
    meal_name = db.Column(db.String, nullable=False)
    price = db.Column(db.Float, nullable=False)
    category = db.Column(db.String, nullable=False)

    @staticmethod
    def get_all():
        return Meal.query.all()

    def __repr__(self):
        """Return a representation of a meal instance."""
        return "<Meal: {}>".format(self.meal)

    
class Menu(Base):

    __tablename__ = 'menu'

    id = db.Column(db.Integer, primary_key=True)
    meals = db.Column(db.String, nullable=False)

class Order(Base):

    __tablename__ = 'order'

    id = db.Column(db.Integer, primary_key=True)
    customer_name = db.Column(db.String, nullable=False)
    meals = db.Column(db.String, nullable=False)
    price = db.Column(db.Float, nullable=False)

    @staticmethod
    def get(**kwargs):
        """This method gets all the orders for a given user."""
        return Order.query.filter_by(**kwargs).first()

    @staticmethod
    def get_all():
        """This method gets all the orders for a given user."""
        return Order.query.all()

    def __repr__(self):
        """Return a representation of an order instance."""
        return '<Menu Date {}>'.format(self.date.ctime())