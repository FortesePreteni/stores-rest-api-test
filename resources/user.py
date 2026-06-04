from flask_restful import Resource, reqparse  # Import Resource and reqparse for API resource management
from flask import request  # Import request to handle incoming data
from flask_jwt_extended import create_access_token  # Import create_access_token to generate JWT tokens
from models.user import UserModel  # Import UserModel to interact with the user data
from security import authenticate

# User Registration Resource
class UserRegister(Resource):
    # Argument parser for handling incoming request data
    parser = reqparse.RequestParser()
    parser.add_argument('username', type=str, required=True, help="This field cannot be blank.")
    parser.add_argument('password', type=str, required=True, help="This field cannot be blank.")

    # POST method to register a new user
    def post(self):
        data = UserRegister.parser.parse_args()  # Parse request data using the defined parser

        if UserModel.find_by_username(data['username']):  # Check if a user already exists with the same username
            return {"message": "A user with that username already exists"}, 400

        user = UserModel(**data)  # Create a new UserModel instance with the parsed data
        user.save_to_db()  # Save the user instance to the database
        return {"message": "User created successfully."}, 201  # Respond with a success message

# User Login Resource (Authentication)
class UserLogin(Resource):
    # POST method to handle user authentication
    def post(self):
        data = request.get_json()  # Parse incoming JSON data from the request
        username = data.get('username')  # Extract the username
        password = data.get('password')  # Extract the password

        user = authenticate(username, password)  # Authenticate the user using the security module
        if user:
            access_token = create_access_token(identity=user.id)  # Generate an access token using the user's ID
            return {"access_token": access_token}, 200  # Return the generated token
        return {"message": "Invalid credentials"}, 401  # Respond with an error message if authentication fails
