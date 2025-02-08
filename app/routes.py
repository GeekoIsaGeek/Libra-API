import os
from flask import Flask, request, jsonify, send_from_directory, abort, Blueprint, make_response
from app.config import Config
import uuid
import json
from werkzeug.security import generate_password_hash
from flask_jwt_extended import create_access_token

main = Blueprint("main", __name__)

@main.after_request
def add_headers(response):
    response.headers['Access-Control-Allow-Origin'] = os.getenv("CLIENT_URL")
    response.headers['Access-Control-Allow-Credentials'] = 'true'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    return response

def allowed_file(filename):
   return "." in filename and filename.rsplit(".", 1)[1].lower() in Config.ALLOWED_EXTENSIONS

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
    

USERS_FILE = 'users.json'

def load_user(email):
    """Load a user by its ID."""
    users = load_users()
    for user in users:
        if user['email'] == email:
            return user
    return None

def load_users():
    """Load the users from the JSON file."""
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, 'r') as file:
            try:
                users = json.load(file)
            except json.JSONDecodeError:
                users = []
    else:
        users = []
    return users


def save_users(users):
    """Save the users to the JSON file."""
    with open(USERS_FILE, 'w') as file:
        json.dump(users, file, indent=4)

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

    if user is None or not user['password'] == generate_password_hash(data['password']):
        return jsonify({'error': 'Invalid credentials'}), 400
    
    access_token = create_access_token(identity=user['username'])

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
        'password': generate_password_hash(data['password'])
    }

    access_token = create_access_token(identity=new_user['username'])
    
    users.append(new_user)
    save_users(users)

    user_response = new_user.copy()
    user_response.pop('password')  

    return jsonify({
        'user': user_response,
        'access_token': access_token
    }), 201

