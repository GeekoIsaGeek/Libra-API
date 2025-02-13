import os
from dotenv import load_dotenv

load_dotenv()

class Config:
   JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')

   DB_PATH = os.path.join(os.path.abspath(os.path.dirname(__name__)), "database.db")

   UPLOAD_FOLDER = os.path.join(os.getcwd(), "uploads")
   IMAGE_FOLDER = os.path.join(UPLOAD_FOLDER, "images")
   BOOK_FOLDER = os.path.join(UPLOAD_FOLDER, "books")

   SQLALCHEMY_DATABASE_URI = f"sqlite:///{DB_PATH}"
   SQLALCHEMY_TRACK_MODIFICATIONS = False

   os.makedirs(UPLOAD_FOLDER, exist_ok=True)

