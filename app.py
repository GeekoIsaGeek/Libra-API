import os
from app import create_app
from flask_cors import CORS

app = create_app()
CORS(app, resources={r"/*": {"origins": [os.getenv('CLIENT_URL'), 'http://localhost:5174', "http://localhost:5173"]}}, supports_credentials=True)

if __name__ == "__main__":  
      app.run(debug=True)
