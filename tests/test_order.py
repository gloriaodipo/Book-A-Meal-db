import sys
import os
import unittest
import json
from . import create_app, db

class OrdersTestCase(unittest.TestCase):
    """This is the class for orders test cases"""

    def setUp(self):
        """Initialize app and define test variables"""
        self.app = create_app('testing')
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.drop_all()
        db.create_all()
        
        self.data = {
                    "customer_name": "Chris", 
                    "meal_name": "chapo",
                    "quantity": 2
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
    
    def test_add_orders(self):
        """Test API can add an order (POST request)"""
        response = self.client.post('/api/v1/user/signup', data = json.dumps(self.user), content_type = 'application/json')
        response = self.client.post('/api/v1/user/login', data=json.dumps({'username': 'chris', 'email': 'chris@gmail.com', 'password': 'passw'}), content_type='application/json')
        
        token = json.loads(response.data.decode('utf-8'))['token']
        headers = {'Authorization': 'Bearer {}'.format(token)}

        response = self.client.post('/api/v1/orders', headers = headers, data = json.dumps(self.data) , content_type = 'application/json')
        result = json.loads(response.data.decode('utf-8'))
        self.assertEqual(result["message"], "Order has been sent")
        self.assertEqual(response.status_code, 201) 

    def test_get_all_orders(self):
        """Test API can get all orders (GET request)"""
        response = self.client.post('/api/v1/user/signup', data = json.dumps(self.admin), content_type = 'application/json')
        response = self.client.post('/api/v1/user/login', data=json.dumps({'username': 'cindy', 'email': 'cindy@gmail.com', 'password': 'admin'}), content_type='application/json')
        
        token = json.loads(response.data.decode('utf-8'))['token']
        headers = {'Authorization': 'Bearer {}'.format(token)}

        response = self.client.post('/api/v1/orders',headers=headers, data = json.dumps(self.data) , content_type = 'application/json')
        response = self.client.get('/api/v1/orders',headers=headers, data = json.dumps(self.data) , content_type = 'application/json')
        self.assertEqual(response.status_code, 200) 

    def test_can_get_single_order(self):
        """Test API can get single order (GET request)"""
        response = self.client.post('/api/v1/user/signup', data = json.dumps(self.admin), content_type = 'application/json')
        response = self.client.post('/api/v1/user/login', data=json.dumps({'username': 'cindy', 'email': 'cindy@gmail.com', 'password': 'admin'}), content_type='application/json')
        
        token = json.loads(response.data.decode('utf-8'))['token']
        headers = {'Authorization': 'Bearer {}'.format(token)}

        response = self.client.post('/api/v1/orders',headers=headers, data = json.dumps(self.data) , content_type = 'application/json')
        response = self.client.get('/api/v1/orders/1',headers=headers, data = json.dumps(self.data) , content_type = 'application/json')
        self.assertEqual(response.status_code, 200)

    def test_cannot_get_invalid_order(self):
        """Test API cannot get invalid order (GET request)"""
        response = self.client.post('/api/v1/user/signup', data = json.dumps(self.admin), content_type = 'application/json')
        response = self.client.post('/api/v1/user/login', data=json.dumps({'username': 'cindy', 'email': 'cindy@gmail.com', 'password': 'admin'}), content_type='application/json')
        
        token = json.loads(response.data.decode('utf-8'))['token']
        headers = {'Authorization': 'Bearer {}'.format(token)}

        response = self.client.post('/api/v1/orders',headers=headers, data = json.dumps(self.data) , content_type = 'application/json')
        response = self.client.get('/api/v1/orders/10',headers=headers, data = json.dumps(self.data) , content_type = 'application/json')
        result = json.loads(response.data.decode('utf-8'))
        self.assertEqual(result["message"], "Order not found")
        self.assertEqual(response.status_code, 404)

    def test_update_order(self):
        """Test API can modify/update details of a given order(PUT request)"""
        response = self.client.post('/api/v1/user/signup', data = json.dumps(self.user), content_type = 'application/json')
        response = self.client.post('/api/v1/user/login', data=json.dumps({'username': 'chris', 'email': 'chris@gmail.com', 'password': 'passw'}), content_type='application/json')
        
        token = json.loads(response.data.decode('utf-8'))['token']
        headers = {'Authorization': 'Bearer {}'.format(token)}
        
        response = self.client.post('/api/v1/orders',headers = headers, data = json.dumps(self.data) , content_type = 'application/json')
        data = {'new_data':{'quantity':5}}
        response = self.client.put('/api/v1/orders/1',headers=headers, data = json.dumps(data) , content_type = 'application/json')
        result = json.loads(response.data.decode('utf-8'))
        self.assertEqual(result["message"], "Updated successfully")
        self.assertEqual(response.status_code, 200) 

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()