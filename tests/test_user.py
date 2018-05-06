import sys
import os
import unittest
import json
from . import app, db

class UserTestCase(unittest.TestCase):
    """This class represents the user login and signup test case."""

    def setUp(self):
        """Initialize app and define test variables"""
        self.app = app
        db.drop_all()
        db.create_all()
        self.app.config
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.data = {
                    "username":"carenakinyi", 
                    "email":"carenakinyi@gmail.com",
                    "password":"passw"
                    }
    
    def test_signup(self):
        """Test API can successfully register a new user (POST request)"""
        response = self.client.post('/api/v1/user/signup', data = json.dumps(self.data), content_type = 'application/json')
        print (response.data)
        result = json.loads(response.data.decode('utf-8'))
        self.assertEqual(result["message"], "Successfully registered")
        self.assertEqual(response.status_code, 201)

    def test_wrong_signup(self):
        """Test API cannot successfully register a new user if any field is left blank(POST request)"""
        response = self.client.post('/api/v1/user/signup', data = json.dumps({'email':'glodipo@gmail.com', 'password': ''}) , content_type = 'application/json')
        result = json.loads(response.data.decode('utf-8'))
        self.assertEqual(result["message"], "All fields required")
        self.assertEqual(response.status_code, 400)

    def test_login(self):
        """Test API can successfully log in registered users using username and password (POST request)"""
        response = self.client.post('/api/v1/user/signup', data = json.dumps(self.data), content_type = 'application/json')
        response = self.client.post('/api/v1/user/login', data=json.dumps({'username': 'carenakinyi', 'email': 'carenakinyi@gmail.com', 'password': 'passw'}), content_type='application/json')
        result = json.loads(response.data.decode('utf-8'))
        self.assertEqual(result["message"], "Login successful!")
        self.assertEqual(response.status_code, 200)

    def test_wrong_login(self):
        """Test API cannot authenticate login when wrong password or username is entered (POST request)"""
        response = self.client.post('/api/v1/user/signup', data = json.dumps(self.data), content_type = 'application/json')
        response = self.client.post('/api/v1/user/login', data=json.dumps({'username': 'carenakinyi', 'password': 'wrong_password'}), content_type='application/json')
        result = json.loads(response.data.decode('utf-8'))
        self.assertEqual(result['message'], 'Oops! , wrong password or username.Please try again')
        self.assertEqual(response.status_code, 401)

    def test_cannot_login_if_no_username_or_password(self):
        """Test API cannot authenticate login when either password or username is missing (POST request)"""
        response = self.client.post('/api/v1/user/signup', data = json.dumps(self.data), content_type = 'application/json')
        response = self.client.post('/api/v1/user/login', data=json.dumps({'username': '', 'password': 'wrong_password'}), content_type='application/json')
        result = json.loads(response.data.decode('utf-8'))
        self.assertEqual(result['message'], 'All fields required')
        self.assertEqual(response.status_code, 400)

    def test_login_nonexistent_user(self):
        """Test API cannot authenticate login when user is nonexistent (POST request)"""
        response = self.client.post('/api/v1/user/login', data=json.dumps({'username': 'nonexistent', 'password': 'wrong_password'}), content_type='application/json')
        result = json.loads(response.data.decode('utf-8'))
        self.assertEqual(result['message'], 'Unavailable, please sign up first')
        self.assertEqual(response.status_code, 404) 

    def tearDown(self):
        db.drop_all()

if __name__ == '__main__':
    unittest.main()    