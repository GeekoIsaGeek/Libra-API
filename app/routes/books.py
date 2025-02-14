from flask import Blueprint, request, jsonify
from app.helpers.book import load_books, save_book, prepare_book, transform_request_data
from flask_jwt_extended import get_jwt_identity, jwt_required
from app.models import User

books = Blueprint("books", __name__)

@books.route('/books', methods=['GET', 'POST'])
@jwt_required(optional=True)
def index():
    """ Get all books or create a new one. """
    if request.method == 'GET':
        books = load_books()
        return jsonify(books), 200
    
    if request.method == 'POST':
        user = User.query.filter_by(email=get_jwt_identity()).first().to_dict()
        if not user:
            return jsonify({'error': 'Authentication required'}), 401
        
        if 'image' not in request.files or 'file' not in request.files:
            return jsonify({'error': 'Missing files'}), 400

        form_data = transform_request_data(request)

        if not all(field in form_data for field in ['title', 'author', 'description', 'language', 'year', 'pages', 'tags', 'slug']):
            return jsonify({'error': 'Missing required fields'}), 400
        
        book = prepare_book({**form_data, 'file': request.files['file'], 'image': request.files['image'] }, user['id'])
        save_book(book, extend=True)

        return jsonify(book), 201

@books.route('/books/<book_id>', methods=['GET'])
def get_book(book_id):
    """ Get a single book by ID. """
    books = load_books()
    book = next((b for b in books if str(b['id']) == str(book_id)), None)
    if not book:
        return jsonify({'error': 'Book not found'}), 404
    return jsonify(book)

@books.route('/books/<book_id>', methods=['PUT'])
@jwt_required()
def update_book(book_id):
    """ Update a book (only the creator can update). """
    user = load_user(get_jwt_identity())
    if not user:
        return jsonify({'error': 'Authentication required'}), 401
    
    form_data = transform_request_data(request)

    if 'file' in request.files:
        form_data['file'] = request.files['file']
    if 'image' in request.files:
        form_data['image'] = request.files['image']

    prepared_book = prepare_book(form_data, user['id'], update=True)
    books = load_books()

    updated_book = {}

    for i, book in enumerate(books):
        if str(book['id']) == str(book_id):
            if book['created_by'] != user['id']:
                return jsonify({'error': 'Permission denied'}), 403     
            updated_book = {**book, **prepared_book}
            books[i] = updated_book 
            break

    save_book(books)
    return jsonify(updated_book), 200

@books.route('/books/<book_id>', methods=['DELETE'])
@jwt_required()
def delete_book(book_id):
    """ Delete a book (only the creator can delete). """
    user = load_user(get_jwt_identity())
    if not user:
        return jsonify({'error': 'Authentication required'}), 401
    
    books = load_books()
    book = next((b for b in books if str(b['id']) == str(book_id)), None)
    if not book:
        return jsonify({'error': 'Book not found'}), 404
    
    if book['created_by'] != user['id']:
        return jsonify({'error': 'Permission denied'}), 403
    
    books.remove(book)
    save_book(books)
    return jsonify({'message': 'Book deleted'}), 200
