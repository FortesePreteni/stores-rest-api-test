# Import necessary classes and functions
from models.item import ItemModel
from models.store import StoreModel
from tests.base_test import BaseTest
import json

# Define a test class that inherits from BaseTest
class StoreTest(BaseTest):
    def test_store_not_found(self):
        # Test if getting a non-existent store returns a 404
        with self.app() as c:
            r = c.get('/store/test')
            self.assertEqual(r.status_code, 404)

    def test_store_found(self):
        # Test if a store can be created and then correctly found with a 200 status
        with self.app() as c:
            with self.app_context():
                StoreModel('test').save_to_db()
                r = c.get('/store/test')
                self.assertEqual(r.status_code, 200)
                self.assertDictEqual(d1={'name': 'test', 'items': []}, d2=json.loads(r.data))

    def test_store_with_items_found(self):
        # Test if a store with items returns the correct data and status
        with self.app() as c:
            with self.app_context():
                StoreModel('test').save_to_db()
                ItemModel('test', 2.99, 1).save_to_db()
                r = c.get('/store/test')
                self.assertEqual(r.status_code, 200)
                self.assertDictEqual(d1={'name': 'test', 'items': [{'name': 'test', 'price': 2.99}]}, d2=json.loads(r.data))

    def test_delete_store(self):
        # Test deleting a store and ensuring the response indicates successful deletion
        with self.app() as c:
            with self.app_context():
                StoreModel('test').save_to_db()
                r = c.delete('/store/test')
                self.assertEqual(r.status_code, 200)
                self.assertDictEqual(d1={'message': 'Store deleted'}, d2=json.loads(r.data))

    def test_create_store(self):
        # Test creating a new store and ensuring it exists in the database
        with self.app() as c:
            with self.app_context():
                r = c.post('/store/test')
                self.assertEqual(r.status_code, 201)
                self.assertIsNotNone(StoreModel.find_by_name('test'))
                self.assertDictEqual(d1={'name': 'test', 'items': []}, d2=json.loads(r.data))

    def test_create_duplicate_store(self):
        # Test that creating a duplicate store results in a 400 status
        with self.app() as c:
            with self.app_context():
                c.post('/store/test')
                r = c.post('/store/test')
                self.assertEqual(r.status_code, 400)

    def test_store_list(self):
        # Test getting a list of stores and ensuring the correct data is returned
        with self.app() as c:
            with self.app_context():
                StoreModel('test').save_to_db()
                r = c.get('/stores')
                self.assertDictEqual(d1={'stores': [{'name': 'test', 'items': []}]}, d2=json.loads(r.data))

    def test_store_with_items_list(self):
        # Test getting a list of stores with items and ensuring the correct detailed data is returned
        with self.app() as c:
            with self.app_context():
                StoreModel('test').save_to_db()
                ItemModel('test', 17.99, 1).save_to_db()
                r = c.get('/stores')
                self.assertDictEqual(d1={'stores': [{'name': 'test', 'items': [{'name': 'test', 'price': 17.99}]}]}, d2=json.loads(r.data))
