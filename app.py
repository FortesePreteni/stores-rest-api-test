import os
from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt_extended import JWTManager

# Import security and resources
from security import authenticate, identity
from resources.item import Item, ItemList
from resources.store import Store, StoreList
from resources.user import UserRegister, UserLogin

# Create Flask application
app = Flask(__name__)

# Configuration
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    'DATABASE_URL',
    'sqlite:///data.db'
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config['JWT_SECRET_KEY'] = 'super-secret'

# Initialize API and JWT
api = Api(app)
jwt = JWTManager(app)

# Add API resources
api.add_resource(Store, '/store/<string:name>')
api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(StoreList, '/stores')
api.add_resource(UserRegister, '/register')
api.add_resource(UserLogin, '/auth')

# Error handler
@app.errorhandler(401)
def auth_error(err):
    return jsonify({
        'message': 'Could not authorize. Did you include a valid Authorization header?'
    }), 401


# JWT identity callback
@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data['sub']
    return identity


# Main entry point
if __name__ == '__main__':
    from db import db

    db.init_app(app)

    # Flask 3.x compatible table creation
    if app.config['DEBUG']:
        with app.app_context():
            db.create_all()

    app.run(port=5000)
