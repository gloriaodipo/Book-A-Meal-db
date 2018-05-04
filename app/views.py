from flask import Flask, request, jsonify
from flask_restful import Api, Resource
import json

from .models import User
from .models import Meal
from .decorators import token_required
from .decorators import admin_token_required

app = Flask(__name__)
api = Api(app)

class UserSignupAPI(Resource):
    def post(self):
        user = request.get_json()
        admin = user.get('admin', '')
        if user.get('username') is None or user.get('email') is None or user.get('password') is None:
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
        if user.password_is_valid(password):
            token = user.generate_token()
            return {'message':'Ssup, you are in!', 'token':token}, 200
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
    def get(self, user):
        meals = Meal.get_all()
        result = {}
        for meal in meals:
            meal_dict = {'meal_name': meal.meal_name, 'price':meal.price, 'category':meal.category}
            result.update({str(meal.id): meal_dict})
        result = jsonify(result)
        result.status_code = 200
        return result



api.add_resource(UserSignupAPI, '/api/v1/user/signup')
api.add_resource(MealsAPI, '/api/v1/meals')
api.add_resource(UserLoginAPI, '/api/v1/user/login')

if __name__ == '__main__':
    app.run(debug=True)
