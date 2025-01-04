# web_app/backend/app.py

from flask import Flask, request, g
from flask_cors import CORS
import os, uuid
from database.db_setup import init_db
from routes.upload_routes import upload_bp
from routes.extract_routes import extract_bp

def create_app():
    app = Flask(__name__)
    CORS(app)

    CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}}, supports_credentials=True)
    
    init_db()
    os.makedirs(os.path.join(app.root_path, 'uploads'), exist_ok=True)
    os.makedirs(os.path.join(app.root_path, 'temp_frames'), exist_ok=True)

    # Session handling
    @app.before_request
    def assign_session_id():
        session_id = request.cookies.get('SESSION_ID')
        if not session_id:
            session_id = str(uuid.uuid4())
        g.session_id = session_id

    @app.after_request
    def set_session_cookie(response):
        if hasattr(g, 'session_id'):
            response.set_cookie('SESSION_ID', g.session_id)
        return response

    # Register routes
    app.register_blueprint(upload_bp, url_prefix='/api')
    app.register_blueprint(extract_bp, url_prefix='/api')

    @app.route('/')
    def index():
        return "Flask with ephemeral session_id"

    return app

if __name__ == "__main__":
    application = create_app()
    application.run(debug=True, host='0.0.0.0', port=8098)
