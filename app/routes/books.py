from flask import Flask, Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import os
import json
import uuid

books = Blueprint("books", __name__)

@books.route("/test", methods=["GET"])
def get_books():
    return jsonify({"message": "This route is reachable!"}), 200

BOOKS_FILE = 'books.json'

def load_data(file):
    """ Load JSON data from a file. """
    if os.path.exists(file):
        with open(file, 'r') as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []
    return []

def save_data(file, data):
    """ Save JSON data to a file. """
    with open(file, 'w') as f:
        json.dump(data, f, indent=4)

    data = request.get_json()
    required_fields = ['title', 'author', 'description', 'language', 'year', 'pages', 'tags', 'image', 'slug', 'link']
    if not all(field in data for field in required_fields):
            return jsonify({'error': 'Missing required fields'}), 400   

    books = load_data(BOOKS_FILE)
    new_book = {
            'id': str(uuid.uuid4()),
            'title': data['title'],
            'author': data['author'],
            'description': data['description'],
            'language': data['language'],
            'year': data['year'],
            'pages': data['pages'],
            'tags': data['tags'],
            'image': data['image'],
            'slug': data['slug'],
            'link': data['link'],
            # 'created_by': user['id']
        }
    books.append(new_book)
    save_data(BOOKS_FILE, books)
    return jsonify(new_book), 201

@books.route('/books', methods=['GET'])
def get_books():
    """ Get all books. """
    books = load_data(BOOKS_FILE)
    return jsonify(books)

@books.route('/books/<book_id>', methods=['GET'])
def get_book(book_id):
    """ Get a single book by ID. """
    books = load_data(BOOKS_FILE)
    book = next((b for b in books if b['id'] == book_id), None)
    if not book:
        return jsonify({'error': 'Book not found'}), 404
    return jsonify(book)

@books.route('/books/<book_id>', methods=['PUT'])
def update_book(book_id):
    """ Update a book (only the creator can update). """
    # user = get_authenticated_user()
    # if not user:
    return jsonify({'error': 'Authentication required'}), 401
    
    books = load_data(BOOKS_FILE)
    book = next((b for b in books if b['id'] == book_id), None)
    if not book:
        return jsonify({'error': 'Book not found'}), 404
    
    if book['created_by'] != user['id']:
        return jsonify({'error': 'Permission denied'}), 403
    
    data = request.get_json()
    for key, value in data.items():
        if key in book:
            book[key] = value
    
    save_data(BOOKS_FILE, books)
    return jsonify(book)

@books.route('/books/<book_id>', methods=['DELETE'])
def delete_book(book_id):
    """ Delete a book (only the creator can delete). """
    # user = get_authenticated_user()
    # if not user:
    return jsonify({'error': 'Authentication required'}), 401
    
    books = load_data(BOOKS_FILE)
    book = next((b for b in books if b['id'] == book_id), None)
    if not book:
        return jsonify({'error': 'Book not found'}), 404
    
    if book['created_by'] != user['id']:
        return jsonify({'error': 'Permission denied'}), 403
    
    books.remove(book)
    save_data(BOOKS_FILE, books)
    return jsonify({'message': 'Book deleted'}), 200

if __name__ == '__main__':
    books.run(debug=True)