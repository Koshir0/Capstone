import unittest
from app import app

class AppTestCase(unittest.TestCase):

    def setUp(self):
        self.client = app.test_client()
        self.success_test_data = {
             # Test data for successful requests
            "name": "John Doe",
            "age": 30,
            "gender": "male",
            "title": "Movie Title",
            "release_date": "2023-08-26"
        }
        self.error_test_data = {
            "invalid_field": "Invalid Value",
        }

    def test_get_actors_success(self):
        response = self.client.get('/actors')
        self.assertEqual(response.status_code, 200)

    def test_get_movies_success(self):
        response = self.client.get('/movies')
        self.assertEqual(response.status_code, 200)

    def test_add_actor_success(self):
        response = self.client.post('/actors', json=self.success_test_data)
        self.assertEqual(response.status_code, 200)

    def test_add_actor_unauthorized(self):
        response = self.client.post('/actors', json=self.success_test_data)
        self.assertEqual(response.status_code, 403)


    def test_rbac_casting_assistant(self):
        with app.app_context():
            current_user_role = 'casting_assistant'
            response = self.client.get('/actors')
            self.assertEqual(response.status_code, 200)

            response = self.client.post('/actors', json=self.success_test_data)
            self.assertEqual(response.status_code, 403)


    def test_rbac_casting_director(self):
        with app.app_context():
            current_user_role = 'casting_director'
            response = self.client.post('/movies', json=self.success_test_data)
            self.assertEqual(response.status_code, 403)  # Should be denied 

    def test_rbac_executive_producer(self):
        with app.app_context():
            current_user_role = 'executive_producer'
            response = self.client.post('/movies', json=self.success_test_data)
            self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()

