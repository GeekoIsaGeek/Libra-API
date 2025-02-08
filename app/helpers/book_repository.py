import os
import json
import uuid
from flask import jsonify

BOOKS_FILE = 'books.json'
INITIAL_BOOKS = 'test_books.json'

def init_books():
   """ Initialize the books file with some data. """
   if not os.path.exists(BOOKS_FILE):
      with open(INITIAL_BOOKS, 'r', encoding='utf-8') as f:
            books = json.load(f)
            save_books(books)

def load_books():
    """ Load JSON data from a file. """
    if os.path.exists(BOOKS_FILE):
        with open(BOOKS_FILE, 'r', encoding='utf-8') as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []
    return []

def save_books(data):
    """ Save JSON data to a file. """
    with open(BOOKS_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

    required_fields = ['title', 'author', 'description', 'language', 'year', 'pages', 'tags', 'image', 'slug', 'link']
    if not all(field in data for field in required_fields):
            return jsonify({'error': 'Missing required fields'}), 400   

    books = load_books(BOOKS_FILE)
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
    save_books(BOOKS_FILE, books)
    return jsonify(new_book), 201
