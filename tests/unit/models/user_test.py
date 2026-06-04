# Import the UserModel class from the user module within the models package.
from models.user import UserModel
# Import the BaseTest class from the base_test module within the tests package.
from tests.base_test import BaseTest

# Define a new class named UserTest, which inherits from BaseTest.
class UserTest(BaseTest):
    # Define a method that tests the user creation functionality.
    def test_create_user(self):
        # Create an instance of UserModel with a username and password.
        user = UserModel('test', 'abcd')

        # Assert that the username of the user instance matches the expected value, with an error message if it fails.
        self.assertEqual(user.username, 'test',
                         "The name of the user after creation does not equal the constructor argument.")
        # Assert that the password of the user instance matches the expected value, with an error message if it fails.
        self.assertEqual(user.password, 'abcd',
                         "The password of the user after creation does not equal the constructor argument.")
