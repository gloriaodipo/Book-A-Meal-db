from datetime import datetime
from flask import request, jsonify
from flask_restful import Resource
import json

from .models import User, Meal
from .decorators import token_required, admin_token_required


class UserSignupAPI(Resource):
    def post(self):
        user = request.get_json()
        admin = user.get('admin', '')
        username = user.get('username', None)
        email = user.get('email', None)
        password = user.get('password', None)

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
                return 'Meal not found', 404
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
