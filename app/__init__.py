import os
from flask import Flask
from app.extensions import jwt
from app.helpers.book import init_books
from app.routes.main import main
from app.models import db
from flask_migrate import Migrate

def create_app():
   app = Flask(__name__)
   
   app.config.from_object("app.config.Config")

   jwt.init_app(app)

   app.register_blueprint(main)

   db.init_app(app)
   migrate = Migrate(app, db)

   with app.app_context():
      os.mkdir(app.config['IMAGE_FOLDER']) if not os.path.exists(app.config['IMAGE_FOLDER']) else None
      os.mkdir(app.config['BOOK_FOLDER']) if not os.path.exists(app.config['BOOK_FOLDER']) else None

      db.create_all()
      
      # init_books()
      
   return app