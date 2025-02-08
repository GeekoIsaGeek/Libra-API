import os
from flask import request, jsonify, send_from_directory, abort, Blueprint, make_response
from app.config import Config
import uuid
from flask_jwt_extended import create_access_token, get_jwt_identity,jwt_required
from app.extensions import pwd_context
from app.helpers.validation import allowed_file
from app.helpers.user_repository import load_user, load_users, save_users

main = Blueprint("main", __name__)

@main.after_request
def add_headers(response):
    response.headers['Access-Control-Allow-Origin'] = os.getenv("CLIENT_URL")
    response.headers['Access-Control-Allow-Credentials'] = 'true'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    return response

@main.route("/")
def home():
    return "Heyyo! Do not worry, the service is running smoothly."

@main.route("/upload", methods=["POST"])
def upload_file():
   if "file" not in request.files:
       return {"error": "No file provided"}, 400

   file = request.files["file"]

   if file.filename == "":
       return {"error": "No selected file"}, 400

   if file and allowed_file(file.filename):
       file.save(os.path.join(Config.UPLOAD_FOLDER, file.filename))
       return {"message": "File uploaded successfully"}, 200

   return {"error": "File not allowed"}, 400

@main.route("/uploads/<filename>", methods=["GET"])
def get_media(filename):
    if not os.path.exists(os.path.join(Config.UPLOAD_FOLDER, filename)):
        return abort(404)
    response = make_response(send_from_directory(Config.UPLOAD_FOLDER, filename))
    return response

@main.route('/user', methods=['GET'])
@jwt_required()
def get_authenticated_user():
    print("Fetching user data")
    try:
        print(request.headers)

        email = get_jwt_identity()
        print(f"Authenticated user: {email}")

        user = load_user(email)
        if user is None:
            return jsonify({'error': 'User not found'}), 404

        user_response = user.copy()
        user_response.pop('password', None)  

        return jsonify(user_response), 200

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': 'An error occurred while fetching user data'}), 500
    

@main.route('/login', methods=['POST'])
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

@main.route('/register', methods=['POST'])
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

