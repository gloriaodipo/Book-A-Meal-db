from app import db
from flask_bcrypt import Bcrypt

menu_meals = db.Table('menu_meals', 
                      db.Column('menu_id', db.Integer, db.ForeignKey('menu.id')),
                      db.Column('meal_id', db.Integer, db.ForeignKey('meals.id')))

class User(db.Model):
    
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True,nullable=True, unique=True)
    email = db.Column(db.String(120), index=True,nullable=True, unique=True)
    password_hash = db.Column(db.String(128), nullable=True)

    def __init__(self,username, email, password):
        """Initialize the user with an email and a password."""
        self.username = username
        self.email = email
        self.password_hash = Bcrypt().generate_password_hash(password).decode()

    def password_is_valid(self, password):
        """
        Checks the password against it's hash to validate the user's password
        """
        return Bcrypt().check_password_hash(self.password, password)

    def save(self):
        """Save a user to the database.
        Includes creating a new user and editing one.
        """
        db.session.add(self)
        db.session.commit()

class Meal(db.Model):

    __tablename__ = 'meals'

    id = db.Column(db.Integer, primary_key=True)
    meal_name = db.Column(db.String, nullable=False)
    price = db.Column(db.Float, nullable=False)

    def __init__(self, meal_name, price):
        self.meal_name = meal_name
        self.price = price

    def save(self):
        """Save a meal to the database"""
        db.session.add(self)
        db.session.commit()

    def delete(self):
        """Delete a meal from the database"""
        db.session.delete(self)
        db.session.commit()
    
class Menu(db.Model):

    __tablename__ = 'menu_items'

    id = db.Column(db.Integer, primary_key=True)
    meals = db.Column(db.String, nullable=False)
    price = db.Column(db.Integer, nullable=False)

    def __init__(self, meals, price):
        """ Initialize menu item"""
        self.meals = meals
        self.price = price

    def save(self):
        """Save a menu to the database"""
        db.session.add(self)
        db.session.commit()
    
class Order(db.Model):

    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True)
    customer_name = db.Column(db.String, nullable=False)
    meals = db.Column(db.String, nullable=False)
    price = db.Column(db.Float, nullable=False)

    def __init__(self, customer_name, meals, price):
        """Initializing the order"""
        self.customer_name = customer_name
        self.meals = meals
        self.price = price

    def save(self):
        """Save an order to the database"""
        db.session.add(self)
        db.session.commit()
          