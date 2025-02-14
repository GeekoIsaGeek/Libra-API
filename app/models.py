from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json

db = SQLAlchemy()

class User(db.Model):
   id = db.Column(db.Integer, primary_key=True, autoincrement=True)
   username = db.Column(db.String(50), unique=True, nullable=False)
   email = db.Column(db.String(120), unique=True, nullable=False)
   password = db.Column(db.String(120), nullable=False)
   created_at = db.Column(db.DateTime, nullable=False, default=datetime.now())
   updated_at = db.Column(db.DateTime, nullable=False, default=datetime.now(), onupdate=datetime.now())

   def to_dict(self):
       return {
           'id': self.id,
           'username': self.username,
           'email': self.email,
           'password': self.password,
       }

class Book(db.Model):
   id = db.Column(db.Integer, primary_key=True, autoincrement=True)
   title = db.Column(db.JSON, nullable=False)
   author = db.Column(db.JSON, nullable=False)
   description = db.Column(db.JSON, nullable=False)
   language = db.Column(db.JSON, nullable=False)
   year = db.Column(db.Integer, nullable=False)
   pages = db.Column(db.Integer, nullable=False)
   tags = db.Column(db.JSON, nullable=False)
   image = db.Column(db.String(120), nullable=False)
   slug = db.Column(db.String(120), nullable=False)
   file = db.Column(db.String(120), nullable=False)
   created_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
   created_at = db.Column(db.DateTime, nullable=False, default=datetime.now())
   updated_at = db.Column(db.DateTime, nullable=False, default=datetime.now(), onupdate=datetime.now())

   def to_dict(self):
       return {
           'id': self.id,
           'title': json.loads(self.title),
           'author': json.loads(self.author),
           'description': json.loads(self.description),
           'language': json.loads(self.language),
           'year': self.year,
           'pages': self.pages,
           'tags': json.loads(self.tags),
           'image': self.image,
           'slug': self.slug,
           'file': self.file,
           'created_by': self.created_by,
       }