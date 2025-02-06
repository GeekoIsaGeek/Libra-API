import os
from flask import Flask, request, send_from_directory, abort, Blueprint, make_response
from app.config import Config

main = Blueprint("main", __name__)

def allowed_file(filename):
   return "." in filename and filename.rsplit(".", 1)[1].lower() in Config.ALLOWED_EXTENSIONS

@main.route("/")
def home():
    return "Hey jude"

@main.route("/upload", methods=["POST"])
def upload_file():
   if "file" not in request.files:
       return {"error": "No file provided"}, 400

   file = request.files["file"]

   if file.filename == "":
       return {"error": "No selected file"}, 400

   if file and allowed_file(file.filename):
       file.save(os.path.join(Config.UPLOAD_FOLDER, file.filename))
       return {"message": "File uploaded successfully"}, 200

   return {"error": "File not allowed"}, 400

@main.route("/uploads/<filename>", methods=["GET"])
def get_media(filename):
    response = make_response(send_from_directory(Config.UPLOAD_FOLDER, filename))
    return response
    