from flask import Flask
from app.extensions import jwt
from app.helpers.book_repository import init_books

def create_app():
   app = Flask(__name__)
   
   app.config.from_object("app.config.Config")

   jwt.init_app(app)

   from app.routes.main import main
   app.register_blueprint(main)

   with app.app_context():
      init_books()

   return app