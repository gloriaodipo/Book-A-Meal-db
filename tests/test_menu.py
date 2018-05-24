import sys
import os
import unittest
import json
from . import create_app, db

   
class MenuTestCase(unittest.TestCase):
    """This is the class for meals test cases"""

    def setUp(self):
        """Initialize app and define test variables"""
        self.app = create_app('testing')
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.drop_all()
        db.create_all()
        
        self.data ={
                    "meal_name": "rice beef", 
                    "price": 500,
                    "category": "dish"
                    }
                    
        self.admin = {
                    "username": "cindy",
                    "email": "cindy@gmail.com",
                    "password": "admin",
                    "admin": True
                    }

        self.user = {
            "username": "chris",
            "email": "chris@gmail.com",
            "password": "passw"
            }          
    
    def test_add_meals_to_menu(self):
        """Test API can add a meal item to menu (POST request)"""
        response = self.client.post('/api/v1/user/signup', data = json.dumps(self.admin), content_type = 'application/json')
        response = self.client.post('/api/v1/user/login', data=json.dumps({'username': 'cindy', 'email': 'cindy@gmail.com', 'password': 'admin'}), content_type='application/json')
        
        token = json.loads(response.data.decode('utf-8'))['token']
        headers = {'Authorization': 'Bearer {}'.format(token)}

        meal_list = json.dumps(self.data)
        menu = {'meal_list':[meal_list]}

        response = self.client.post('/api/v1/menu', headers = headers, data = json.dumps(menu) , content_type = 'application/json')
        result = json.loads(response.data.decode('utf-8'))
        self.assertEqual(result["message"], "menu created")
        self.assertEqual(response.status_code, 201) 

    def test_cannot_add_meals_to_menu(self):
        """Test API cannot add a meal item to menu if not admin (POST request)"""
        response = self.client.post('/api/v1/user/signup', data = json.dumps(self.user), content_type = 'application/json')
        response = self.client.post('/api/v1/user/login', data=json.dumps({'username': 'chris', 'email': 'chris@gmail.com', 'password': 'passw'}), content_type='application/json')
        
        token = json.loads(response.data.decode('utf-8'))['token']
        headers = {'Authorization': 'Bearer {}'.format(token)}

        meal_list = json.dumps(self.data)
        menu = {'meal_list':[meal_list]}

        response = self.client.post('/api/v1/menu', headers = headers, data = json.dumps(menu) , content_type = 'application/json')
        result = json.loads(response.data.decode('utf-8'))
        self.assertEqual(result["message"], "Unauthorized")
        self.assertEqual(response.status_code, 401)

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
