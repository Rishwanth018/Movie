from flask import Flask, send_from_directory
from flask_cors import CORS
from dotenv import load_dotenv
import os

# Load environment variables from .env
load_dotenv()

# Import Blueprints
from authentication import auth_bp
from watchlist import watchlist_bp

# Create Flask app
app = Flask(__name__)
CORS(app)  # Allow requests from frontend

# Register routes
app.register_blueprint(auth_bp, url_prefix="/api/auth")
app.register_blueprint(watchlist_bp, url_prefix="/api/watchlist")

# Serve static frontend files from ../public
@app.route('/')
def serve_index():
    return send_from_directory('../public', 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory('../public', path)

# Run server
if __name__ == "__main__":
    print("🚀 Server running at http://127.0.0.1:5000")
    app.run(debug=True)
