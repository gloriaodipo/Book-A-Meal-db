from app import app
import unittest
import json


class UserTestCase(unittest.TestCase):
    """This class represents the user login and signup test case."""

    def setUp(self):
        """Initialize app and define test variables"""
        self.app = app
        self.app.config
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.data = {
                    "username":"carenakinyi", 
                    "email":"carenakinyi@gmail.com",
                    "password":"passw"
                    }
    
    def test_login(self):
        """Test API can successfully log in registered users using username and password (POST request)"""
        response = self.client.post('/api/v1/user/login', data=json.dumps({'username': 'gloriaodipo', 'password': 'bubble'}), content_type='application/json')
        result = json.loads(response.data)
        self.assertEqual(result["message"], "You are successfully logged in")
        self.assertEqual(response.status_code, 200)

    def test_wrong_login(self):
        """Test API cannot authenticate login when wrong password is used or no password supplied (POST request)"""
        response = self.client.post('/api/v1/user/login', data=json.dumps({'username': 'gloriaodipo', 'password': 'wrong_password'}), content_type='application/json')
        result = json.loads(response.data)
        self.assertEqual(result['message'], 'Wrong password.')
        self.assertEqual(response.status_code, 401)

    def test_login_nonexistent_user(self):
        """Test API cannot authenticate login when user is nonexistent (POST request)"""
        response = self.client.post('/api/v1/user/login', data=json.dumps({'username': 'nonexistent', 'password': 'wrong_password'}), content_type='application/json')
        result = json.loads(response.data)
        self.assertEqual(result['message'], 'User unavailable')
        self.assertEqual(response.status_code, 404)    

    def test_signup(self):
        """Test API can successfully register a new user (POST request)"""
        response = self.client.post('/api/v1/user/signup', data = json.dumps(self.data), content_type = 'application/json')
        print (response.data)
        result = json.loads(response.data)
        self.assertEqual(result["message"], "Successfully registered")
        self.assertEqual(response.status_code, 201)

    def test_wrong_signup(self):
        """Test API cannot successfully register a new user if any field is left blank(POST request)"""
        response = self.client.post('/api/v1/user/signup', data = json.dumps({'email':'glodipo@gmail.com', 'password': ''}) , content_type = 'application/json')
        result = json.loads(response.data)
        self.assertEqual(result["message"], "All fields required")
        self.assertEqual(response.status_code, 400)

if __name__ == '__main__':
    unittest.main()
