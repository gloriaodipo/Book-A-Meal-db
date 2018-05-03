import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask_bcrypt import Bcrypt

import app

db = app.db

class Base(db.Model):
    __abstract__ = True
    __table_args__ = {'extend_existing': True}
    def save(self):
        """Save a meal to the database"""
        db.session.add(self)
        db.session.commit()

    def delete(self):
        """Delete a meal from the database"""
        db.session.delete(self)
        db.session.commit()

class User(Base):
    
    __tablename__ = 'user'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True,nullable=True, unique=True)
    email = db.Column(db.String(120), index=True,nullable=True, unique=True)
    password = db.Column(db.String(128), nullable=True)

    # self.password_hash = Bcrypt().generate_password_hash(password).decode('utf-8')

    def password_is_valid(self, password):
        """
        Checks the password against it's hash to validate the user's password
        """
        return Bcrypt().check_password_hash(self.password, password)

class Meal(Base):

    __tablename__ = 'meal'

    id = db.Column(db.Integer, primary_key=True)
    meal_name = db.Column(db.String, nullable=False)
    price = db.Column(db.Float, nullable=False)

    
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