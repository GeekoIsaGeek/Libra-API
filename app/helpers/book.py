import os
import json
from app.config import Config
from werkzeug.utils import secure_filename
from app.models import db, Book
import time

INITIAL_BOOKS = 'test_books.json'

def init_books():
    if Book.query.count() == 0:
      with open(INITIAL_BOOKS, 'r', encoding='utf-8') as f:
            books = json.load(f)  
            for book in books:
                book = {**book,  
                    'title':json.dumps(book['title']), 
                    'author':json.dumps(book['author']), 
                    'description':json.dumps(book['description']), 
                    'language': json.dumps(book['language'])
                }
                db.session.add(Book(**book))
            db.session.commit()         

def collect_request_data(request):
    """ Transform request data into a dictionary. """
    form_data = {
        'title': request.form.get('title'),
        'author': request.form.get('author'),
        'description': request.form.get('description'),
        'language': request.form.get('language'),
        'year': request.form.get('year'),
        'pages': request.form.get('pages'),
        'tags': request.form.get('tags'),
        'slug': request.form.get('slug'),
    }
    return form_data

def prepare_book(form_data, user_id, update=False):
    """ Prepare book data for saving. """
    if 'image' in form_data:
        imagePath = os.path.join(Config.IMAGE_FOLDER, secure_filename(f"{int(time.time())}_{form_data['image'].filename}")) 
        form_data['image'].save(imagePath)
        form_data['image'] = imagePath.split('/uploads/')[1]

    if 'file' in form_data:
        bookFilePath = os.path.join(Config.BOOK_FOLDER, secure_filename(f"{int(time.time())}_{form_data['file'].filename}"))
        form_data['file'].save(bookFilePath)
        form_data['file'] = bookFilePath.split('/uploads/')[1]

    if not update:
        created_by = user_id if not "created_by" in form_data else form_data['created_by']

        form_data.update({
            'created_by': created_by,
        })
        
    return form_data
    
