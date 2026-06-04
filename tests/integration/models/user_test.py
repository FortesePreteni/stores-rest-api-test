from models.user import UserModel  # Imports the UserModel class from the models.user module.
from tests.base_test import BaseTest  # Imports the BaseTest class from the tests.base_test module.

class UserTest(BaseTest):  # Defines a new class UserTest which inherits from BaseTest.
    def test_crud(self):  # Defines a method test_crud to test CRUD operations on the UserModel.
        with self.app_context():  # Starts a context for the application where the test will run.
            user = UserModel('test', 'abcd')  # Creates an instance of UserModel with username 'test' and password 'abcd'.

            # Asserts that no user with username 'test' exists in the database before the user is saved to the database.
            self.assertIsNone(UserModel.find_by_username('test'), "Found an user with name 'test' before save_to_db")
            
            # Asserts that no user with id 1 exists in the database before the user is saved to the database.
            self.assertIsNone(UserModel.find_by_id(1), "Found an user with id '1' before save_to_db")

            user.save_to_db()  # Calls the save_to_db method to save the user instance to the database.

            # Asserts that a user with username 'test' exists in the database after the user is saved to the database.
            self.assertIsNotNone(UserModel.find_by_username('test'),
                                 "Did not find an user with name 'test' after save_to_db")
            
            # Asserts that a user with id 1 exists in the database after the user is saved to the database.
            self.assertIsNotNone(UserModel.find_by_id(1), "Did not find an user with id '1' after save_to_db")
