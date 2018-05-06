import sys
import os
import unittest
import json
from . import app, db

   
class MealsTestCase(unittest.TestCase):
    """This is the class for meals test cases"""

    def setUp(self):
        """Initialize app and define test variables"""
        db.drop_all()
        db.create_all()
        self.app = app
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.data = {
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
    
    def test_add_meals(self):
        """Test API can add a meal (POST request)"""
        response = self.client.post('/api/v1/user/signup', data = json.dumps(self.admin), content_type = 'application/json')
        response = self.client.post('/api/v1/user/login', data=json.dumps({'username': 'cindy', 'email': 'cindy@gmail.com', 'password': 'admin'}), content_type='application/json')
        
        token = json.loads(response.data.decode('utf-8'))['token']
        headers = {'Authorization': 'Bearer {}'.format(token)}

        response = self.client.post('/api/v1/meals', headers = headers, data = json.dumps(self.data) , content_type = 'application/json')
        result = json.loads(response.data.decode('utf-8'))
        self.assertEqual(result["message"], "meal added")
        self.assertEqual(response.status_code, 201) 

    def test_get_all_meals(self):
        """Test API can get all meals (GET request)"""
        response = self.client.post('/api/v1/user/signup', data = json.dumps(self.admin), content_type = 'application/json')
        response = self.client.post('/api/v1/user/login', data=json.dumps({'username': 'cindy', 'email': 'cindy@gmail.com', 'password': 'admin'}), content_type='application/json')
        
        token = json.loads(response.data.decode('utf-8'))['token']
        headers = {'Authorization': 'Bearer {}'.format(token)}

        response = self.client.post('/api/v1/meals',headers=headers, data = json.dumps(self.data) , content_type = 'application/json')
        response = self.client.get('/api/v1/meals',headers=headers, data = json.dumps(self.data) , content_type = 'application/json')
        self.assertEqual(response.status_code, 200) 

    def test_update_meal(self):
        """Test API can modify/update details of a given meal using meal_id (PUT request)"""
        response = self.client.post('/api/v1/user/signup', data = json.dumps(self.admin), content_type = 'application/json')
        response = self.client.post('/api/v1/user/login', data=json.dumps({'username': 'cindy', 'email': 'cindy@gmail.com', 'password': 'admin'}), content_type='application/json')
        
        token = json.loads(response.data.decode('utf-8'))['token']
        headers = {'Authorization': 'Bearer {}'.format(token)}
        
        response = self.client.post('/api/v1/meals',headers = headers, data = json.dumps(self.data) , content_type = 'application/json')
        data = {'new_data':{'price':700}}
        response = self.client.put('/api/v1/meals/1',headers=headers, data = json.dumps(data) , content_type = 'application/json')
        result = json.loads(response.data.decode('utf-8'))
        self.assertEqual(result["message"], "Updated successfully")
        self.assertEqual(response.status_code, 200) 

    def test_delete_meal(self):
        """Test API can delete a meal using meal_id (DELETE request)"""
        response = self.client.post('/api/v1/user/signup', data = json.dumps(self.admin), content_type = 'application/json')
        response = self.client.post('/api/v1/user/login', data=json.dumps({'username': 'cindy', 'email': 'cindy@gmail.com', 'password': 'admin'}), content_type='application/json')
        
        token = json.loads(response.data.decode('utf-8'))['token']
        headers = {'Authorization': 'Bearer {}'.format(token)}
        
        response = self.client.post('/api/v1/meals', headers = headers, data = json.dumps(self.data) , content_type = 'application/json')
        response = self.client.delete('/api/v1/meals/1', headers=headers)
        result = json.loads(response.data.decode('utf-8'))
        self.assertEqual(result["message"], "Meal 1 deleted")
        self.assertEqual(response.status_code, 200) 

    def test_only_admin_can_add_meal(self):
        """Test API cannot add a meal if not admin (POST request)"""
        response = self.client.post('/api/v1/user/signup', data = json.dumps(self.user), content_type = 'application/json')
        response = self.client.post('/api/v1/user/login', data=json.dumps({'username': 'chris', 'email': 'chris@gmail.com', 'password': 'passw'}), content_type='application/json')
        
        token = json.loads(response.data.decode('utf-8'))['token']
        headers = {'Authorization': 'Bearer {}'.format(token)}

        response = self.client.post('/api/v1/meals', headers = headers, data = json.dumps(self.data) , content_type = 'application/json')
        result = json.loads(response.data.decode('utf-8'))
        self.assertEqual(result["message"], "Unauthorized")
        self.assertEqual(response.status_code, 401)    

    def test_only_admin_can_get_meals(self):
        """Test API only admin can get all meals (GET request)"""
        response = self.client.post('/api/v1/user/signup', data = json.dumps(self.user), content_type = 'application/json')
        response = self.client.post('/api/v1/user/login', data=json.dumps({'username': 'chris', 'email': 'chris@gmail.com', 'password': 'passw'}), content_type='application/json')
        
        token = json.loads(response.data.decode('utf-8'))['token']
        headers = {'Authorization': 'Bearer {}'.format(token)}

        response = self.client.post('/api/v1/meals',headers=headers, data = json.dumps(self.data) , content_type = 'application/json')
        response = self.client.get('/api/v1/meals',headers=headers, data = json.dumps(self.data) , content_type = 'application/json')
        self.assertEqual(response.status_code, 401) 

    def test_only_admin_can_update_meal(self):
        """Test API only admin can modify/update details of a given meal (PUT request)"""
        response = self.client.post('/api/v1/user/signup', data = json.dumps(self.user), content_type = 'application/json')
        response = self.client.post('/api/v1/user/login', data=json.dumps({'username': 'chris', 'email': 'chris@gmail.com', 'password': 'passw'}), content_type='application/json')
        
        token = json.loads(response.data.decode('utf-8'))['token']
        headers = {'Authorization': 'Bearer {}'.format(token)}
        
        response = self.client.post('/api/v1/meals',headers = headers, data = json.dumps(self.data) , content_type = 'application/json')
        data = {'new_data':{'price':700}}
        response = self.client.put('/api/v1/meals/1',headers=headers, data = json.dumps(data) , content_type = 'application/json')
        result = json.loads(response.data.decode('utf-8'))
        self.assertEqual(result["message"], "Unauthorized")
        self.assertEqual(response.status_code, 401)

    def test_only_admin_can_delete_meal(self):
        """Test API only admin can delete a meal (DELETE request)"""
        response = self.client.post('/api/v1/user/signup', data = json.dumps(self.user), content_type = 'application/json')
        response = self.client.post('/api/v1/user/login', data=json.dumps({'username': 'chris', 'email': 'chris@gmail.com', 'password': 'passw'}), content_type='application/json')
        
        token = json.loads(response.data.decode('utf-8'))['token']
        headers = {'Authorization': 'Bearer {}'.format(token)}
        
        response = self.client.post('/api/v1/meals', headers = headers, data = json.dumps(self.data) , content_type = 'application/json')
        response = self.client.delete('/api/v1/meals/1', headers=headers)
        result = json.loads(response.data.decode('utf-8'))
        self.assertEqual(result["message"], "Unauthorized")
        self.assertEqual(response.status_code, 401)

    def tearDown(self):
        db.drop_all()

if __name__ == '__main__':
    unittest.main()
