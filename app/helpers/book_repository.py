import os
import json
import uuid
from flask import jsonify
from app.config import Config
from werkzeug.utils import secure_filename


BOOKS_FILE = 'books.json'
INITIAL_BOOKS = 'test_books.json'

def init_books():
   """ Initialize the books file with some data. """
   if not os.path.exists(BOOKS_FILE):
      with open(INITIAL_BOOKS, 'r', encoding='utf-8') as f:
            books = json.load(f)
            save_book(books)

def load_books():
    """ Load JSON data from a file. """
    if os.path.exists(BOOKS_FILE):
        with open(BOOKS_FILE, 'r', encoding='utf-8') as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []
    return []

def transform_request_data(request):
    """ Transform request data into a dictionary. """
    data = {
        'title': json.loads(request.form.get('title', "{}")),
        'author': json.loads(request.form.get('author', "{}")),
        'description': json.loads(request.form.get('description', "{}")),
        'language': json.loads(request.form.get('language',"{}")),
        'year': request.form.get('year'),
        'pages': request.form.get('pages'),
        'tags': request.form.get('tags'),
        'slug': request.form.get('slug'),
    }
    return data

def prepare_book(form_data, user_id):
    imagePath = os.path.join(Config.IMAGE_FOLDER, secure_filename(form_data['image'].filename)) 
    form_data['image'].save(imagePath)

    bookFilePath = os.path.join(Config.BOOK_FOLDER, secure_filename(form_data['file'].filename))
    form_data['file'].save(bookFilePath)

    id = str(uuid.uuid4()) if not "id" in form_data else form_data['id']
    created_by = user_id if not "created_by" in form_data else form_data['created_by']

    form_data.update({
        'id': id,
        'created_by': created_by,
        'image': imagePath.split('/uploads')[1],
        'file': bookFilePath.split('/uploads')[1],
    })
    
    return form_data
    
def save_book(data):
    """ Save JSON data to a file, extending existing data. """
    try:
        with open(BOOKS_FILE, 'r', encoding='utf-8') as f:
            existing_data = json.load(f)
    except FileNotFoundError:
        existing_data = []

    existing_data.append(data)

    with open(BOOKS_FILE, 'w', encoding='utf-8') as f:
        json.dump(existing_data, f, indent=4, ensure_ascii=False)
