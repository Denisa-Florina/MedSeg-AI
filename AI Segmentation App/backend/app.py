from flask import Flask
from flask_cors import CORS
import os
import sys

from services.firebaseService import firebase_service
from datetime import datetime
import hashlib


sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
    app.config['UPLOAD_FOLDER'] = 'uploads'
    app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024
    

    allowed_origins = [
        "http://localhost:3000",
        "http://localhost:3001",
        os.environ.get('FRONTEND_URL', 'https://medsegai.web.app/') 
    ]
    
    CORS(app, 
         supports_credentials=True, 
         origins=allowed_origins,
         allow_headers=['Content-Type', 'Authorization'],
         methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'])
    

    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    

    from backend.api.routes.authRoutes import auth_bp
    from backend.api.routes.patientRoutes import patient_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(patient_bp)
    
    @app.route('/api/health')
    def health_check():
        return {'status': 'healthy', 'message': 'MedSeg AI Backend is running'}, 200


    return app

app = create_app()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
