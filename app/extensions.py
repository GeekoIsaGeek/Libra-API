from flask_jwt_extended import JWTManager
from passlib.context import CryptContext

jwt = JWTManager()

pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")
