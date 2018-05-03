from flask import Flask, request, jsonify
from flask_restful import Api, Resource
import json

from app.models import User

app = Flask(__name__)
api = Api(app)

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

api.add_resource(UserLoginAPI, '/api/v1/user/signup')

if __name__ == '__main__':
    app.run(debug=True)
