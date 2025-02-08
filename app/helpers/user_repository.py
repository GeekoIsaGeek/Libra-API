import json
import os

USERS_FILE = 'users.json'

def save_users(users):
    """Save the users to the JSON file."""
    with open(USERS_FILE, 'w') as file:
        json.dump(users, file, indent=4)

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

def load_user(email):
    """Load a user by its ID."""
    users = load_users()
    for user in users:
        if user['email'] == email:
            return user
    return None
