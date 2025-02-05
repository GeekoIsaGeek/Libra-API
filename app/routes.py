import os
from flask import Flask, request, send_from_directory, abort, Blueprint
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
       file.save(os.path.join(main.config['UPLOAD_FOLDER'], file.filename))
       return {"message": "File uploaded successfully"}, 200

   return {"error": "File not allowed"}, 400

@main.route("/uploads/<filename>", methods=["GET"])
def get_media(filename):
    referer = request.headers.get("Referer") or "" 

    if not any(referrer in referer for referrer in Config.ALLOWED_REFERRERS):
        return abort(403)
    
    return send_from_directory(main.config['UPLOAD_FOLDER'], filename)