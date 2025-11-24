from flask import Flask, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
import os

load_dotenv()

def create_app():
    app = Flask(__name__)
    
    # الإعدادات الأساسية
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key')
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'jwt-secret-key')
    
    # تمكين CORS للـ Vue.js
    CORS(app)
    
    # إعداد JWT
    jwt = JWTManager(app)
    
    # routes سندرجها لاحقاً
    @app.route('/api/health')
    def health_check():
        return jsonify({"status": "healthy", "message": "Social Media Platform API is running"})
    
    @app.route('/api/version')
    def version():
        return jsonify({"version": "1.0.0", "platform": "Social Media Manager"})
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)
