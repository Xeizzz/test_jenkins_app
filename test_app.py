import unittest
import json
from app import app

class TestApp(unittest.TestCase):
    
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
    
    def test_hello_endpoint(self):
        response = self.app.get('/')
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['message'], 'Hello from Jenkins!')
        self.assertEqual(data['status'], 'ok')
        self.assertIn('timestamp', data)
    
    def test_health_endpoint(self):
        response = self.app.get('/health')
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['status'], 'healthy')
    
    def test_greet_endpoint(self):
        response = self.app.get('/greet/John')
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['greeting'], 'Hello, John!')
        self.assertIn('timestamp', data)
    
    def test_calculate_add(self):
        response = self.app.post('/api/v1/calculate',
                                json={'operation': 'add', 'a': 5, 'b': 3})
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['result'], 8)
    
    def test_calculate_subtract(self):
        response = self.app.post('/api/v1/calculate',
                                json={'operation': 'subtract', 'a': 10, 'b': 4})
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['result'], 6)
    
    def test_calculate_multiply(self):
        response = self.app.post('/api/v1/calculate',
                                json={'operation': 'multiply', 'a': 3, 'b': 7})
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['result'], 21)
    
    def test_calculate_divide(self):
        response = self.app.post('/api/v1/calculate',
                                json={'operation': 'divide', 'a': 15, 'b': 3})
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['result'], 5)
    
    def test_calculate_divide_by_zero(self):
        response = self.app.post('/api/v1/calculate',
                                json={'operation': 'divide', 'a': 10, 'b': 0})
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['error'], 'Division by zero')
    
    def test_calculate_invalid_operation(self):
        response = self.app.post('/api/v1/calculate',
                                json={'operation': 'power', 'a': 2, 'b': 3})
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['error'], 'Invalid operation')
    
    def test_calculate_missing_params(self):
        response = self.app.post('/api/v1/calculate',
                                json={'operation': 'add'})
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['error'], 'Missing parameters')

if __name__ == '__main__':
    unittest.main()