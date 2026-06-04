from db import db  # Import the db instance to manage database connections

# User Model Class
class UserModel(db.Model):
    __tablename__ = 'users'  # Set the database table name for this model

    # Define the table columns
    id = db.Column(db.Integer, primary_key=True)  # Primary key column
    username = db.Column(db.String(80), unique=True)  # Unique username column
    password = db.Column(db.String(80))  # Password column

    # Initialize the UserModel with provided username and password
    def __init__(self, username, password):
        self.username = username
        self.password = password

    # Save the current instance to the database
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    # Find a user by username
    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()  # Query and return the first user found by username

    # Find a user by ID
    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()  # Query and return the first user found by ID
