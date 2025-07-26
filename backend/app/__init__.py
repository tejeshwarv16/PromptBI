# backend/app/__init__.py

from flask import Flask
from flask_cors import CORS # <-- 1. Import CORS

def create_app():
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__)
    
    # 2. Initialize CORS and allow requests from your frontend's origin
    CORS(app, resources={r"/*": {"origins": "http://localhost:5173"}})

    # Register a blueprint for our routes
    from . import routes
    app.register_blueprint(routes.bp)

    return app