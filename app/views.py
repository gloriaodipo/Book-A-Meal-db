from flask import Flask, request, jsonify
from flask_restful import Api, Resource
import json

from app.models import User

app = Flask(__name__)
app(Api)

class UserSignupAPI(Resource):
    def post(self):
        user = request.get_json()
        if user.get('username') is None or user.get('email') is None or user.get('password') is None:
            result = jsonify({'message': 'All fields required'}) 
            result.status_code = 400
            return result
    
        new_user = User(username=user.get('username'), email=user.get('email'), password=user.get('password'))
        new_user.save()

        result = jsonify({'message': 'Successfully registered'})
        result.status_code = 201
        return result

# class UserLoginAPI(Resource):

#     def post(self):
#         access = request.get_json()
#         username = access.get('username')
#         password = access.get('password')
#         for user in users:
#             if username == user.username:
#                 if password == user.password:
#                     result = jsonify({"message": "You are successfully logged in"})
#                     result.status_code = 200
#                     return result
#                 else:
#                     result =jsonify({'message': 'Wrong password.'})
#                     result.status_code = 401
#                     return result

#             result = jsonify({"message": "User unavailable"})
#             result.status_code = 404
#             return result
                       


# api.add_resource(UserLoginAPI, '/api/v1/user/login')
# api.add_resource(MealsAPI, '/api/v1/meals')
# api.add_resource(SingleMealAPI, '/api/v1/meals/<int:meal_id>')
# api.add_resource(OrdersAPI, '/api/v1/orders')
# api.add_resource(SingleOrderAPI, '/api/v1/orders/<int:order_id>')
# api.add_resource(MenuAPI, '/api/v1/menu')

# if __name__ == '__main__':
#     app.run(debug=True)
