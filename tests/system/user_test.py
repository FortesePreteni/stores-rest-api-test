# Import necessary classes and modules
from models.user import UserModel
from tests.base_test import BaseTest
import json

# Define the test class for user-related operations, inheriting from BaseTest
class UserTest(BaseTest):
    # Test for user registration
    def test_register_user(self):
        with self.app() as c:  # Get a test client from the app
            with self.app_context():  # Use the application context
                # Post request to register a new user
                r = c.post('/register', data={'username': 'test', 'password': '1234'})

                # Check that the response status code is 201 (created)
                self.assertEqual(r.status_code, 201)
                # Ensure the user is actually saved in the database
                self.assertIsNotNone(UserModel.find_by_username('test'))
                # Check that the response contains the correct success message
                self.assertDictEqual(d1={'message': 'User created successfully.'},
                                     d2=json.loads(r.data))

    # Test for registering and then logging in a user
    def test_register_and_login(self):
        with self.app() as c:  # Get a test client from the app
            with self.app_context():  # Use the application context
                # Register a user
                c.post('/register', data={'username': 'test', 'password': '1234'})
                # Post request to authenticate the user
                auth_request = c.post('/auth', data=json.dumps({
                    'username': 'test',
                    'password': '1234'
                }), headers={'Content-Type': 'application/json'})

                # Verify that the login response includes an access token
                self.assertIn('access_token', json.loads(auth_request.data).keys())

    # Test for trying to register a duplicate user
    def test_register_duplicate_user(self):
        with self.app() as c:  # Get a test client from the app
            with self.app_context():  # Use the application context
                # Register a user for the first time
                c.post('/register', data={'username': 'test', 'password': '1234'})
                # Attempt to register the same user again
                r = c.post('/register', data={'username': 'test', 'password': '1234'})

                # Check that the response status code is 400 (bad request)
                self.assertEqual(r.status_code, 400)
                # Check that the response contains the correct error message
                self.assertDictEqual(d1={'message': 'A user with that username already exists'},
                                     d2=json.loads(r.data))
