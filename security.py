from hmac import compare_digest  # Secure string comparison using compare_digest from hmac
from models.user import UserModel  # Import UserModel for database operations

# Function to authenticate the user
def authenticate(username, password):
    user = UserModel.find_by_username(username)  # Find the user by username
    if user and compare_digest(user.password, password):  # Securely compare the provided password with the stored password
        return user  # Return the user if credentials match

# Function to retrieve a user identity
def identity(payload):
    user_id = payload['identity']  # Extract user identity (usually from a JWT payload)
    return UserModel.find_by_id(user_id)  # Find and return the user by ID
