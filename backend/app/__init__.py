from flask import Flask
from flask_cors import CORS
import os
from dotenv import load_dotenv

def create_app():
    app = Flask(__name__)

    # Load environment variables
    load_dotenv()

    # Configure CORS
    frontend_origin = os.getenv('FRONTEND_ORIGIN', 'http://localhost:5173')
    CORS(app, origins=[frontend_origin])

    # Configure upload settings
    app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024  # 10MB limit

    # Register blueprints
    from app.routes import bp as api_bp
    app.register_blueprint(api_bp, url_prefix='/api')

    return app