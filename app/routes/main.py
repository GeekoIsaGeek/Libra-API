import os
from flask import send_from_directory, abort, Blueprint, make_response
from app.config import Config
from app.routes.auth import auth
from app.routes.books import books
from flask_jwt_extended import jwt_required

main = Blueprint("main", __name__)

main.register_blueprint(auth)
main.register_blueprint(books)

@main.after_request
def add_headers(response):
    response.headers['Access-Control-Allow-Origin'] = os.getenv("CLIENT_URL")
    response.headers['Access-Control-Allow-Credentials'] = 'true',
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
    return response

@main.route("/")
def home():
    return "Heyyo! Do not worry buddy, the service is running smoothly."

@main.route("/uploads/books/<filename>", methods=["GET"])
def get_media(filename):
    print(filename)
    if not os.path.exists(os.path.join(Config.BOOK_FOLDER, filename)):
        return abort(404)
    response = make_response(send_from_directory(Config.BOOK_FOLDER, filename))
    return response

@main.route("/uploads/images/<filename>", methods=["GET"])
def get_image(filename):
    if not os.path.exists(os.path.join(Config.IMAGE_FOLDER, filename)):
        return abort(404)
    response = make_response(send_from_directory(Config.IMAGE_FOLDER, filename))
    return response


