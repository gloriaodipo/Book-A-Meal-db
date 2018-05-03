from app import db
from flask_bcrypt import Bcrypt

class Base(db.Model):
    __abstract__ = True
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
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True,nullable=True, unique=True)
    email = db.Column(db.String(120), index=True,nullable=True, unique=True)
    password_hash = db.Column(db.String(128), nullable=True)

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