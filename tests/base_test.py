"""
BaseTest

This class should be the parent class to each unit test.
It allows for instantiation of the database dynamically,
and makes sure that it is a new, blank database each time.
"""

# Import TestCase from unittest module for creating test cases
from unittest import TestCase
# Import the Flask application instance
from app import app
# Import the database instance
from db import db

# Define BaseTest class which inherits from TestCase
class BaseTest(TestCase):
    # Class variable for setting the SQLite in-memory database URI
    SQLALCHEMY_DATABASE_URI = "sqlite://"

    @classmethod
    # Class method to set up database configuration before any tests are run
    def setUpClass(cls):
        # Configure the SQLAlchemy database URI for the app
        app.config['SQLALCHEMY_DATABASE_URI'] = BaseTest.SQLALCHEMY_DATABASE_URI
        # Ensure DEBUG mode is off during testing to mimic production environment more closely
        app.config['DEBUG'] = False
        # Initialize app context to apply configurations
        app.config['PROPOGATE_EXEPTIONS'] = True
        with app.app_context():
            # Initialize the app with the database setup
            db.init_app(app)

    # Method to set up the database before each test method
    def setUp(self):
        # Set up database within the application context
        with app.app_context():
            # Create all tables for the database
            db.create_all()
        # Store a test client of the app in instance variable for test use
        self.app = app.test_client
        # Store the application context for possible use in tests
        self.app_context = app.app_context

    # Method to tear down the database after each test method
    def tearDown(self):
        # Access the application context for database teardown
        with app.app_context():
            # Remove the database session
            db.session.remove()
            # Drop all tables from the database
            db.drop_all()

