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
        response = self.client.post('/api/v1/user/signup', data = json.dumps({'last_name':'odipo', 'username':'godipo','email':'glodipo@gmail.com', 'password': ''}) , content_type = 'application/json')
        result = json.loads(response.data)
        self.assertEqual(result["message"], "All fields required")
        self.assertEqual(response.status_code, 400)

class MealsTestCase(unittest.TestCase):
    """This is the class for meals test cases"""

    def setUp(self):
        """Initialize app and define test variables"""
        self.app = app
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.data = {
                    "meal_id": 4,
                    "meal_name": "rice beef", 
                    "price": 500,
                    "category": "dish"
                    }

    def test_add_meals(self):
        """Test API can add a meal (POST request)"""
        response = self.client.post('/api/v1/meals', data = json.dumps(self.data) , content_type = 'application/json')
        result = json.loads(response.data)
        self.assertEqual(result["message"], "meal added")
        self.assertEqual(response.status_code, 201) 

    def test_get_all_meals(self):
        """Test API can get all meals (GET request)"""
        response = self.client.get('/api/v1/meals', data = json.dumps(self.data) , content_type = 'application/json')
        self.assertEqual(response.status_code, 200) 

    def test_update_meal(self):
        """Test API can modify/update details of a given meal using meal_id (PUT request)"""
        response = self.client.put('/api/v1/meals/2', data = json.dumps(self.data) , content_type = 'application/json')
        result = json.loads(response.data)
        self.assertEqual(result["message"], "meal has been modified")
        self.assertEqual(response.status_code, 200) 

    def test_delete_meal(self):
        """Test API can delete a meal using meal_id (DELETE request)"""
        response = self.client.delete('/api/v1/meals/4')
        result = json.loads(response.data)
        self.assertEqual(result["message"], "meal deleted")
        self.assertEqual(response.status_code, 200) 

class OrderTestCase(unittest.TestCase):
    """This is the class for orders test cases"""

    def setUp(self):
        """Initialize app and define test variables"""
        self.app = app
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.data = {
                    "order_id": 5,
                    "customer": "gloria", 
                    "total": "ksh1500",
                    "order_items": "chapati with beef, fresh juice"
                    }
                    
    def test_add_order(self):
        """Test API can add an order (POST request)"""
        response = self.client.post('/api/v1/orders', data = json.dumps(self.data) , content_type = 'application/json')
        result = json.loads(response.data)
        self.assertEqual(result["message"], "order added")
        self.assertEqual(response.status_code, 201)     

    def test_get_all_orders(self):
        """Test API can get all orders (GET request)"""
        response = self.client.get('/api/v1/orders', data = json.dumps(self.data) , content_type = 'application/json')
        self.assertEqual(response.status_code, 200) 

    def test_update_order(self):
        """Test can modify/update details an order using order_id (PUT request)"""
        response = self.client.put('/api/v1/orders/1', data = json.dumps(self.data) , content_type = 'application/json')
        result = json.loads(response.data)
        self.assertEqual(result["message"], "order has been modified")
        self.assertEqual(response.status_code, 200) 

class MenuTestCase(unittest.TestCase):
    """This is the class for menu test cases"""

    def setUp(self):
        """Initialize app and define test variables"""
        self.app = app
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.data = {
                    "meal_id": 2,
                    "meal_name": "rice beef", 
                    "price": 600,
                    "category": "dish"
                    }

    def test_add_menu(self):
        """Test API can add a meal (POST request)"""
        response = self.client.post('/api/v1/menu', data = json.dumps(self.data) , content_type = 'application/json')
        result = json.loads(response.data)
        self.assertEqual(result["message"], "meal added to menu")
        self.assertEqual(response.status_code, 201) 

    def test_get_menu(self):
        """Test API can get menu (GET request)"""
        response = self.client.get('/api/v1/menu', data = json.dumps(self.data) , content_type = 'application/json')
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
