from flask import Blueprint,request,jsonify
import uuid
from flask_jwt_extended import create_access_token, get_jwt_identity,jwt_required
from app.extensions import pwd_context
from app.helpers.user_repository import load_user, load_users, save_users

auth = Blueprint("auth", __name__)

@auth.route('/user', methods=['GET'])
@jwt_required()
def get_authenticated_user():
    try:
        email = get_jwt_identity()
        user = load_user(email)
        
        if user is None:
            return jsonify({'error': 'User not found'}), 404

        user_response = user.copy()
        user_response.pop('password', None)  

        return jsonify(user_response), 200

    except Exception as e:
        return jsonify({'error': 'An error occurred while fetching user data'}), 500

@auth.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    required_fields = ['email', 'password']
    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        return jsonify({'error': f'Missing fields: {", ".join(missing_fields)}'}), 400

    user = load_user(data['email'])

    if user is None or not pwd_context.verify(data['password'], user['password']):
        return jsonify({'error': 'Invalid credentials'}), 400
    
    access_token = create_access_token(identity=user['email'])

    user_response = user.copy()
    user_response.pop('password')

    return jsonify({
        'user': user_response,
        'access_token': access_token
    }), 200

@auth.route('/register', methods=['POST'])
def create_user():
    data = request.get_json()

    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    required_fields = ['username', 'email', 'password']
    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        return jsonify({'error': f'Missing fields: {", ".join(missing_fields)}'}), 400
    
    users = load_users()

    for user in users:
        if user['email'] == data['email']:
            return jsonify({'error': 'Email already exists'}), 400
        if user['username'] == data['username']:
            return jsonify({'error': 'Username already exists'}), 400
    
    new_user = {
        'id': str(uuid.uuid4()),
        'username': data['username'],
        'email': data['email'],
        'password': pwd_context.hash(data['password'])
    }

    access_token = create_access_token(identity=new_user['email'])
    
    users.append(new_user)
    save_users(users)

    user_response = new_user.copy()
    user_response.pop('password')  

    return jsonify({
        'user': user_response,
        'access_token': access_token
    }), 201
