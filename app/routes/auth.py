from flask import Blueprint,request,jsonify
from flask_jwt_extended import create_access_token, get_jwt_identity,jwt_required
from app.extensions import pwd_context
from app.models import User
from sqlalchemy import or_
from app.models import db

auth = Blueprint("auth", __name__)

@auth.route('/user', methods=['GET'])
@jwt_required()
def get_authenticated_user():
    try:
        email = get_jwt_identity()
        user = User.query.filter_by(email=email).first().to_dict()
        
        if user is None:
            return jsonify({'error': 'User not found'}), 404

        del user['password']

        return jsonify(user), 200

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

    user = User.query.filter_by(email=data['email']).first().to_dict()

    if user is None or not pwd_context.verify(data['password'], user['password']):
        return jsonify({'error': 'Invalid credentials'}), 400
    
    access_token = create_access_token(identity=user['email'])

    return jsonify({
        'user': user,
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
    
    user = User.query.filter(or_(User.username == data['username'], User.email == data['email'])).first()

    if user:
        return jsonify({'error': 'User with provided email or username already exists!'}), 400
    
    new_user = User(
        username=data['username'],
        email=data['email'],
        password=pwd_context.hash(data['password'])
    )

    db.session.add(new_user)
    db.session.commit()

    new_user = new_user.to_dict()

    del new_user['password']

    access_token = create_access_token(identity=new_user['email'])

    return jsonify({
        'user': new_user,
        'access_token': access_token
    }), 201
