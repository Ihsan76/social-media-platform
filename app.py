# -*- coding: utf-8 -*-
import os
from flask import Flask, render_template, jsonify
from config import config
from routes import all_blueprints
from utils.helpers import json_response

def create_app(config_name='default'):
    """دالة إنشاء التطبيق - Factory Pattern"""
    app = Flask(__name__)
    
    # تحميل الإعدادات
    app.config.from_object(config[config_name])
    
    # تسجيل الـBlueprints
    for blueprint in all_blueprints:
        app.register_blueprint(blueprint, url_prefix='/api')
    
    # المسارات الأساسية
    @app.route('/')
    def home():
        """الصفحة الرئيسية"""
        return render_template('index.html')
    
    @app.route('/api/')
    def api_home():
        """الصفحة الرئيسية للـAPI"""
        data = {
            "message": "مرحباً! منصة إدارة الوسائط الاجتماعية تعمل بنجاح! 🚀",
            "status": "نشط",
            "version": "2.0.0",
            "endpoints": {
                "auth": {
                    "register": "/api/auth/register",
                    "login": "/api/auth/login",
                    "profile": "/api/auth/profile"
                },
                "social": {
                    "connect": "/api/social/connect",
                    "accounts": "/api/social/accounts",
                    "platform_accounts": "/api/social/accounts/<platform>"
                },
                "system": {
                    "health": "/api/health",
                    "status": "/api/status"
                }
            }
        }
        return json_response(data)
    
    @app.route('/api/health')
    def health():
        """فحص صحة النظام"""
        from routes.auth import user_manager, sessions
        from models.social_account import SocialAccountManager
        
        social_manager = SocialAccountManager()
        
        data = {
            "status": "صحي",
            "message": "الخدمة تعمل بشكل طبيعي",
            "statistics": {
                "users_count": len(user_manager.users),
                "active_sessions": len(sessions),
                "social_accounts": len(social_manager.accounts)
            },
            "version": "2.0.0"
        }
        return json_response(data)
    
    @app.route('/api/status')
    def status():
        """حالة النظام"""
        data = {
            "status": "نشط",
            "environment": config_name,
            "debug_mode": app.config['DEBUG']
        }
        return json_response(data)
    
    # معالجة الأخطاء
    @app.errorhandler(404)
    def not_found(error):
        return json_response({"error": "الصفحة غير موجودة"}, 404)
    
    @app.errorhandler(500)
    def internal_error(error):
        return json_response({"error": "حدث خطأ داخلي في السيرفر"}, 500)
    
    return app

# إنشاء التطبيق
app = create_app()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=app.config['DEBUG'])
