from flask import Flask, jsonify, render_template_string
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
    
    @app.route('/')
    def home():
        html_content = """
        <!DOCTYPE html>
        <html dir="rtl">
        <head>
            <meta charset="UTF-8">
            <title>نظام إدارة وسائل التواصل الاجتماعي</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; text-align: center; }
                .container { background: white; padding: 40px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); max-width: 600px; margin: 0 auto; }
                h1 { color: #333; }
                .status { background: #4CAF50; color: white; padding: 10px; border-radius: 5px; margin: 20px 0; }
                .endpoints { text-align: left; margin: 20px 0; }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>🚀 نظام إدارة وسائل التواصل الاجتماعي</h1>
                <div class="status">✅ الخدمة تعمل بنجاح</div>
                <p>مرحباً بك في النظام المتكامل لإدارة حسابات وسائل التواصل الاجتماعي</p>
                
                <div class="endpoints">
                    <h3>واجهات برمجة التطبيقات المتاحة:</h3>
                    <ul>
                        <li><a href="/api/health">/api/health</a> - حالة الخدمة</li>
                        <li><a href="/api/version">/api/version</a> - معلومات النسخة</li>
                    </ul>
                </div>
                
                <p>👉 <a href="https://github.com/Ihsan76/social-media-platform">تصفح المستودع على GitHub</a></p>
            </div>
        </body>
        </html>
        """
        return render_template_string(html_content)
    
    @app.route('/api/health')
    def health_check():
        return jsonify({"status": "healthy", "message": "Social Media Platform API is running"})
    
    @app.route('/api/version')
    def version():
        return jsonify({"version": "1.0.0", "platform": "Social Media Manager"})
    
    return app

if __name__ == '__main__':
    app = create_app()
    port = int(os.environ.get('PORT', 8080))
    app.run(debug=False, host='0.0.0.0', port=port)
