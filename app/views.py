from datetime import datetime
from flask import request, jsonify
from flask_restful import Resource
import json

from .models import User, Meal, Order, Menu 
from .decorators import token_required, admin_token_required


class UserSignupAPI(Resource):
    def post(self):
        user = request.get_json()
        admin = user.get('admin', '')
        username = user.get('username', None)
        email = user.get('email', None)
        password = user.get('password', None)

        users = User.get_all()
        for user in users:
            if username == user.username:
                return {'message': 'User already exists'}, 202

        if username is None or len(username)==0  or email is None or len(email)==0 or password is None or len(password)==0:
            return {'message': 'All fields required'}, 400
    
        new_user = User(username=user.get('username'), email=user.get('email'), password=user.get('password'))
        if admin == True:
            new_user.make_user_admin()
        new_user.save()

        return {'message': 'Successfully registered'}, 201

class UserLoginAPI(Resource):
    def post(self):
        user = request.get_json()
        username = user.get('username')
        password = user.get('password')
        user = User.get(username=username)

        if username is None or len(username)==0 or password is None or len(password)==0:
            return {'message': 'All fields required'}, 400
        if user == None:
            return {'message':'Unavailable, please sign up first'}, 404
        if user.password_is_valid(password):
            token = user.generate_token()
            return {'message':'Login successful!', 'token':token}, 200
        else:
            return {'message':'Oops! , wrong password or username.Please try again'}, 401

class MealsAPI(Resource):
    @admin_token_required
    def post(self, user):
        meal = request.get_json()
        new_meal = Meal(meal_name=meal.get('meal_name'), price=meal.get('price'),
        category=meal.get('category'))

        new_meal.save()

        return {"message": "meal added"}, 201

    @admin_token_required
    def get(self, user, meal_id=None):
        if meal_id:
            meal = Meal.get(id=meal_id)
            if not isinstance(meal, Meal):
                return {'message': 'Meal not found'}, 404
            return {'meal_name': meal.meal_name, 'price':meal.price, 'category':meal.category}, 200
        meals = Meal.get_all()
        result = {}
        for meal in meals:
            meal_dict = {'meal_name': meal.meal_name, 'price':meal.price, 'category':meal.category}
            result.update({str(meal.id): meal_dict})
        return result, 200

    @admin_token_required
    def delete(self, user, meal_id):
        meal = Meal.get(id=meal_id)
        if not meal:
            return {'message': 'Meal not found'}, 404
        meal.delete()
        return {'message': 'Meal {} deleted'.format(meal_id)}

    @admin_token_required
    def put(self, user, meal_id):
        new_data = request.get_json()['new_data']
        meal = Meal.get(id=meal_id)
        for key in new_data:
            meal.update(key, new_data[key])
        return {
            'new_meal':{
                'meal_name': meal.meal_name,
                'price': meal.price,
                'category': meal.category},
                'message': 'Updated successfully'}, 200

class OrdersAPI(Resource):
    @token_required
    def post(self, user):
        order = request.get_json()
        new_order = Order(customer_name=order.get('customer_name'), meal_name=order.get('meal_name'),
        quantity=order.get('quantity'))

        new_order.save()
        return {'message': 'Order has been sent'}, 201

    @admin_token_required
    def get(self, user, order_id=None):
        if order_id:
            order = Order.get(id=order_id)
            if not isinstance(order, Order):
                return {'message': 'Order not found'}, 404
            return {'customer_name': order.customer_name, 'meal_name':order.meal_name, 'quantity':order.quantity}, 200
        orders = Order.get_all()
        result = {}
        for order in orders:
            order_dict = {'customer_name': order.customer_name, 'meal_name':order.meal_name, 'quantity':order.quantity}
            result.update({str(order.id): order_dict})
        return result, 200

    @token_required
    def put(self, user, order_id):
        new_data = request.get_json()['new_data']
        order = Order.get(id=order_id)
        for key in new_data:
            order.update(key, new_data[key])
        return {
            'new_order':{
                'customer_name': order.customer_name,
                'meal_name': order.meal_name,
                'quantity': order.quantity},
                'message': 'Updated successfully'}, 200    

class MenuAPI(Resource):
    @admin_token_required
    def post(self, user):
        if user.admin:
            menu = request.get_json()
            new_menu = Menu(meal_name=menu.get('meal_name'), price=menu.get('price'),
            category=menu.get('category'))

            new_menu.save()
            return {'message': 'menu created'}, 201
    