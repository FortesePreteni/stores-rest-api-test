from models.user import UserModel
from models.item import ItemModel
from models.store import StoreModel
from tests.base_test import BaseTest
import json

class ItemTest(BaseTest):
    def setUp(self):
        # Initialize the test setup from the superclass
        super(ItemTest, self).setUp()
        # Simulate app context and create a user
        with self.app() as c:
            with self.app_context():
                # Create and save a new user to the database
                UserModel('test', '1234').save_to_db()

                # Authenticate and obtain an access token
                auth_request = c.post('/auth', data=json.dumps({
                    'username': 'test',
                    'password': '1234'
                }), headers={'Content-Type': 'application/json'})

                # Debug: Print the response data from auth request
                print("Auth request response data:", auth_request.data)

                # Check the status code before proceeding
                if auth_request.status_code == 200:
                    # Store the access token for use in subsequent requests
                    self.auth_header = "Bearer {}".format(json.loads(auth_request.data)['access_token'])
                else:
                    # Handle cases where auth fails
                    print(f"Authentication failed with status {auth_request.status_code}")
                    self.auth_header = None

    def test_item_no_auth(self):
        # Test access to an item without authentication
        with self.app() as c:
            response = c.get('/item/test')
            # Assert that the server responds with a 401 Unauthorized status
            self.assertEqual(response.status_code, 401)

def test_item_not_found(self):
    # Test retrieval of a non-existing item with proper authentication
    with self.app() as c:
        response = c.get('/item/test', headers={
            'Authorization': self.auth_header,
            'Content-Type': 'application/json' 
        })
        # Assert that the server responds with a 404 Not Found status
        self.assertEqual(response.status_code, 404)


def test_item_found(self):
    # Test retrieval of an existing item
    with self.app() as c:
        with self.app_context():
            # Setup: create a store and an item in the database
            StoreModel('test').save_to_db()
            ItemModel('test', 17.99, 1).save_to_db()

            response = c.get('/item/test', headers={
                'Authorization': self.auth_header,
                'Content-Type': 'application/json'  # 👈 Add this line
            })
            # Assert that the item is retrieved successfully with correct details
            self.assertEqual(response.status_code, 200)
            self.assertDictEqual({'name': 'test', 'price': 17.99}, json.loads(response.data))


    def test_delete_item(self):
        # Test deletion of an item
        with self.app() as c:
            with self.app_context():
                # Setup: create a store and an item in the database
                StoreModel('test').save_to_db()
                ItemModel('test', 17.99, 1).save_to_db()

                response = c.delete('/item/test', headers={'Authorization': self.auth_header})
                # Assert that the item is deleted successfully
                self.assertEqual(response.status_code, 200)
                self.assertDictEqual({'message': 'Item deleted'}, json.loads(response.data))

    def test_create_item(self):
        # Test creation of a new item
        with self.app() as c:
            with self.app_context():
                # Setup: create a store in the database
                StoreModel('test').save_to_db()

                response = c.post('/item/test', data=json.dumps({'price': 17.99, 'store_id': 1}),
                                  headers={'Content-Type': 'application/json', 'Authorization': self.auth_header})
                # Assert that the item is created successfully with correct details
                self.assertEqual(response.status_code, 201)
                self.assertDictEqual({'name': 'test', 'price': 17.99}, json.loads(response.data))

    def test_create_duplicate_item(self):
        # Test creation of a duplicate item
        with self.app() as c:
            with self.app_context():
                # Setup: create a store and an item in the database
                StoreModel('test').save_to_db()
                c.post('/item/test', data=json.dumps({'price': 17.99, 'store_id': 1}),
                       headers={'Content-Type': 'application/json', 'Authorization': self.auth_header})

                response = c.post('/item/test', data=json.dumps({'price': 17.99, 'store_id': 1}),
                                  headers={'Content-Type': 'application/json', 'Authorization': self.auth_header})
                # Assert that creating a duplicate item fails with a 400 Bad Request status
                self.assertEqual(response.status_code, 400)

    def test_put_item(self):
        # Test updating or creating an item using PUT method
        with self.app() as c:
            with self.app_context():
                # Setup: create a store in the database
                StoreModel('test').save_to_db()

                response = c.put('/item/test', data=json.dumps({'price': 17.99, 'store_id': 1}),
                                 headers={'Content-Type': 'application/json', 'Authorization': self.auth_header})
                # Assert that the item is created or updated successfully
                self.assertEqual(response.status_code, 200)
                self.assertDictEqual({'name': 'test', 'price': 17.99}, json.loads(response.data))
