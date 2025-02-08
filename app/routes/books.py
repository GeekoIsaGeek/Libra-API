from flask import Blueprint, request, jsonify

books = Blueprint("books", __name__)

@books.route("/test", methods=["GET"])
def get_books():
    return jsonify({"message": "This route is reachable!"}), 200