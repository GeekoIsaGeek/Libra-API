from flask import Blueprint, request, jsonify
from app.helpers.book_repository import load_books, save_books
from flask_jwt_extended import get_jwt_identity, jwt_required
from app.helpers.user_repository import load_user

books = Blueprint("books", __name__)

@books.route('/books', methods=['GET'])
def get_books():
    """ Get all books. """
    books = load_books()
    return jsonify(books)

@books.route('/books/<book_id>', methods=['GET'])
def get_book(book_id):
    """ Get a single book by ID. """
    books = load_books()
    book = next((b for b in books if b['id'] == book_id), None)
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
    
    books = load_books()
    book = next((b for b in books if b['id'] == book_id), None)
    if not book:
        return jsonify({'error': 'Book not found'}), 404
    
    if book['created_by'] != user['id']:
        return jsonify({'error': 'Permission denied'}), 403
    
    data = request.get_json()
    for key, value in data.items():
        if key in book:
            book[key] = value
    
    save_books(books)
    return jsonify(book)

@books.route('/books/<book_id>', methods=['DELETE'])
@jwt_required()
def delete_book(book_id):
    """ Delete a book (only the creator can delete). """
    user = load_user(get_jwt_identity())
    if not user:
        return jsonify({'error': 'Authentication required'}), 401
    
    books = load_books()
    book = next((b for b in books if b['id'] == book_id), None)
    if not book:
        return jsonify({'error': 'Book not found'}), 404
    
    if book['created_by'] != user['id']:
        return jsonify({'error': 'Permission denied'}), 403
    
    books.remove(book)
    save_books(books)
    return jsonify({'message': 'Book deleted'}), 200
