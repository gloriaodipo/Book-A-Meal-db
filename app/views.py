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

        users = user.query.all()
        for user in users:
            if user.username == user.username:
                result = jsonify({'message': 'User already exists'}) 
                result.status_code = 202
                return result

        if username is None or len(username)==0  or email is None or len(email)==0 or password is None or len(password)==0:
            result = jsonify({'message': 'All fields required'}) 
            result.status_code = 400
            return result
    
        new_user = User(username=user.get('username'), email=user.get('email'), password=user.get('password'))
        if admin == True:
            new_user.make_user_admin()
        new_user.save()

        result = jsonify({'message': 'Successfully registered'})
        result.status_code = 201
        return result

class UserLoginAPI(Resource):
    def post(self):
        user = request.get_json()
        username = user.get('username')
        password = user.get('password')
        user = User.get(username=username)

        if username is None or len(username)==0 or password is None or len(password)==0:
            result = jsonify({'message': 'All fields required'}) 
            result.status_code = 400
            return result
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

        result = jsonify({"message": "meal added"})
        result.status_code = 201
        return result

    @admin_token_required
    def get(self, user, meal_id=None):
        if meal_id:
            meal = Meal.get(id=meal_id)
            if not isinstance(meal, Meal):
                return 'Meal not found', 404
            meal_dict = {'meal_name': meal.meal_name, 'price':meal.price, 'category':meal.category}
            result = jsonify(meal_dict)
            result.status_code = 200
            return result
        meals = Meal.get_all()
        result = {}
        for meal in meals:
            meal_dict = {'meal_name': meal.meal_name, 'price':meal.price, 'category':meal.category}
            result.update({str(meal.id): meal_dict})
        result = jsonify(result)
        result.status_code = 200
        return result

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
        result = jsonify({'new_meal':{'meal_name': meal.meal_name, 'price': meal.price, 'category': meal.category}, 'message': 'Updated successfully'})
        result.status_code = 200
        return result

# class MenuAPI(Resource):
#     @admin_token_required
#     def post(self, user):
#         post_data = request.get_json()
#         meal_items = post_data.get('meal_items', '')
#         date = post_data.get('date', '')
#         if date:
            
#             try:
#                 year, month, day = date.split('-')
#                 date = datetime(year=int(year), month=int(month), day=int(day))
#             except:
#                 return 'Ensure date is of the form YYYY-MM-DD', 400

#         # create a menu object
#         menu = Menu(date=date)
#         # looping through meal items and adding them to menu
#         if meal_items:
#             for meal_id in meal_items:
#                 meal = Meal.get(id=meal_id)
#                 if not meal:
#                     return 'Meal {} not found'.format(meal_id), 400
#                 menu.add_to_menu(meal)
#             menu.save()
#             meal_list = [[meal.id, meal.name, meal.price] for meal in menu.meals]
#             result = jsonify({'id': menu.id, 'date': menu.date, 'meal': meal_list})
#             result.status_code = 201
#             return result
#         return 'Meal list is empty!', 400
   
#     @token_required
#     def get(self, user):
#         date = datetime.utcnow().date()
#         menu = Menu.get(date=date)
#         if not menu:
#             return 'Menu for {} not found'.format(date.ctime())
#         meal_list = [[meal.id, meal.name, meal.price] for meal in menu.meals]
#         result = jsonify({'id': menu.id, 'date': menu.date, 'meal': meal_list})
#         result.status_code = 200
#         return result