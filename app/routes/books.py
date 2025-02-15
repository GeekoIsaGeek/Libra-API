from flask import Blueprint, request, jsonify
from app.helpers.book import prepare_book, collect_request_data
from flask_jwt_extended import get_jwt_identity, jwt_required
from app.models import User, Book
from app.models import db
from app.config import Config
import os

books = Blueprint("books", __name__)

@books.route('/books', methods=['GET', 'POST'])
@jwt_required(optional=True)
def index():
    """ Get all books or create a new one. """
    if request.method == 'GET':
        books = [book.to_dict() for book in Book.query.all()]
        return jsonify(books), 200
    
    if request.method == 'POST':
        user = User.query.filter_by(email=get_jwt_identity()).first()

        if not user:
            return jsonify({'error': 'Authentication required'}), 401
        else :
            user = user.to_dict()
        
        if 'image' not in request.files or 'file' not in request.files:
            return jsonify({'error': 'Missing files'}), 400
        
        if Book.query.filter_by(slug=request.form.get('slug')).first():
            return jsonify({'error': 'Book already exists'}), 400

        form_data = collect_request_data(request)

        if not all(field in form_data for field in ['title', 'author', 'description', 'language', 'year', 'pages', 'tags', 'slug']):
            return jsonify({'error': 'Missing required fields'}), 400
        
        book = prepare_book({**form_data, 'file': request.files['file'], 'image': request.files['image'] }, user['id'])
        created_book = Book(**book)

        db.session.add(created_book)
        db.session.commit()

        return jsonify(created_book.to_dict()), 201

@books.route('/books/<book_id>', methods=['GET'])
def get_book(book_id):
    """ Get a single book by ID. """
    book = Book.query.filter_by(id=book_id).first()

    if not book:
        return jsonify({'error': 'Book not found'}), 404
    else: 
        book = book.to_dict()

    return jsonify(book)

@books.route('/books/<book_id>', methods=['PUT'])
@jwt_required()
def update_book(book_id):
    """ Update a book (only the creator can update). """
    user = User.query.filter_by(email=get_jwt_identity()).first()
    if not user:
        return jsonify({'error': 'Authentication required'}), 401
    else:
        user = user.to_dict()
    
    form_data = collect_request_data(request)

    if 'file' in request.files:
        form_data['file'] = request.files['file']
    if 'image' in request.files:
        form_data['image'] = request.files['image']

    prepared_book = prepare_book(form_data, user['id'], update=True)

    book = Book.query.filter_by(id=int(book_id)).first()
    
    if not book:
        return jsonify({'error': 'Book not found'}), 404
    else:
        book = book.to_dict()

    if book['created_by'] != user['id']:
        return jsonify({'error': 'Permission denied'}), 403
    
    updated_book = {**book, **prepared_book}

    db.session.query(Book).filter_by(id=book_id).update(updated_book)
    db.session.commit()

    return jsonify(Book(**updated_book).to_dict()), 200

@books.route('/books/<book_id>', methods=['DELETE'])
@jwt_required()
def delete_book(book_id):
    """ Delete a book (only the creator can delete). """
    user = User.query.filter_by(email=get_jwt_identity()).first()

    if not user:
        return jsonify({'error': 'Authentication required'}), 401
    else:
        user = user.to_dict()
    
    book = Book.query.filter_by(id=book_id).first()
    if not book:
        return jsonify({'error': 'Book not found'}), 404
    else:
        book = book.to_dict()
    
    if book['created_by'] != user['id']:
        return jsonify({'error': 'Permission denied'}), 403
    
    if book['image']:
        os.remove(os.path.join(Config.UPLOAD_FOLDER, book['image']))
    if book['file']:
        os.remove(os.path.join(Config.UPLOAD_FOLDER, book['file']))
    
    db.session.query(Book).filter_by(id=book_id).delete()
    db.session.commit()

    return jsonify({'message': 'Book deleted'}), 200
