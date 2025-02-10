import os

from dotenv import load_dotenv

load_dotenv()

class Config:
   ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "webp", "pdf", 'epub'}

   JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')

   UPLOAD_FOLDER = os.path.join(os.getcwd(), "uploads")
   IMAGE_FOLDER = os.path.join(UPLOAD_FOLDER, "images")
   BOOK_FOLDER = os.path.join(UPLOAD_FOLDER, "books")

   os.makedirs(UPLOAD_FOLDER, exist_ok=True)

