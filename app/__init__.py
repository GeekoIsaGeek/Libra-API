from flask import Flask
from app.extensions import jwt

def create_app():
   app = Flask(__name__)
   
   app.config.from_object("app.config.Config")

   jwt.init_app(app)

   from app.routes.main import main
   app.register_blueprint(main)

   return app