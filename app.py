from app import create_app
from flask_cors import CORS

app = create_app()
CORS(app, supports_credentials=True, origins=["http://localhost:5173"])

if __name__ == "__main__":    
      app.run(debug=True)
