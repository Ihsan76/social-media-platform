from flask import Flask, jsonify, render_template_string, request
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os
import json
from datetime import datetime, timedelta
from models import db, User, SocialAccount, ScheduledPost

load_dotenv()

def create_app():
    app = Flask(__name__)
    
    # الإعدادات الأساسية
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key')
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'jwt-secret-key')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///social_media.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # تهيئة الإضافات
    db.init_app(app)
    CORS(app)
    jwt = JWTManager(app)
    
    # إنشاء الجداول
    with app.app_context():
        db.create_all()
    
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
                .container { background: white; padding: 40px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); max-width: 700px; margin: 0 auto; }
                h1 { color: #333; margin-bottom: 20px; }
                .status { background: #4CAF50; color: white; padding: 15px; border-radius: 8px; margin: 20px 0; font-size: 18px; }
                .db-status { background: #2196F3; color: white; padding: 15px; border-radius: 8px; margin: 15px 0; font-size: 16px; }
                .endpoints { text-align: right; margin: 25px 0; background: #f8f9fa; padding: 20px; border-radius: 8px; }
                .endpoints h3 { color: #333; margin-bottom: 15px; text-align: center; }
                .endpoints ul { list-style: none; padding: 0; }
                .endpoints li { margin: 10px 0; padding: 10px; background: white; border-radius: 5px; border-right: 4px solid #667eea; }
                .endpoints a { color: #667eea; text-decoration: none; font-weight: bold; }
                .endpoints a:hover { text-decoration: underline; }
                .note { background: #fff3cd; color: #856404; padding: 15px; border-radius: 8px; margin: 20px 0; border: 1px solid #ffeaa7; }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>🚀 نظام إدارة وسائل التواصل الاجتماعي</h1>
                
                <div class="status">✅ الخدمة تعمل بنجاح</div>
                <div class="db-status">🗄️ قاعدة البيانات PostgreSQL نشطة</div>
                
                <p style="font-size: 18px; color: #555; margin: 20px 0;">
                    مرحباً بك في النظام المتكامل لإدارة حسابات وسائل التواصل الاجتماعي
                </p>
                
                <div class="endpoints">
                    <h3>🔗 واجهات برمجة التطبيقات المتاحة:</h3>
                    <ul>
                        <li>📊 <a href="/api/health">/api/health</a> - حالة الخدمة</li>
                        <li>ℹ️ <a href="/api/version">/api/version</a> - معلومات النسخة</li>
                        <li>👥 <a href="/api/accounts">/api/accounts</a> - إدارة الحسابات <small>(تتطلب مصادقة)</small></li>
                        <li>📅 <a href="/api/schedule">/api/schedule</a> - جدولة المنشورات <small>(تتطلب مصادقة)</small></li>
                        <li>�� <a href="/api/auth/login">/api/auth/login</a> - تسجيل الدخول</li>
                    </ul>
                </div>

                <div class="note">
                    <strong>💡 ملاحظة:</strong> بعض الواجهات تتطلب مصادقة. استخدم <code>/api/auth/login</code> أولاً للحصول على token.
                </div>
                
                <p style="margin-top: 30px;">
                    👉 <a href="https://github.com/Ihsan76/social-media-platform" style="color: #667eea; text-decoration: none; font-weight: bold;">تصفح المستودع على GitHub</a>
                </p>
            </div>
        </body>
        </html>
        """
        return render_template_string(html_content)
    
    @app.route('/api/health')
    def health_check():
        try:
            # اختبار اتصال قاعدة البيانات
            db.session.execute('SELECT 1')
            db_status = "connected"
        except Exception as e:
            db_status = f"disconnected: {str(e)}"
            
        return jsonify({
            "status": "healthy", 
            "message": "Social Media Platform API is running",
            "database": db_status,
            "timestamp": datetime.utcnow().isoformat()
        })
    
    @app.route('/api/version')
    def version():
        return jsonify({
            "version": "1.0.0", 
            "platform": "Social Media Manager",
            "database": "PostgreSQL",
            "features": ["إدارة الحسابات", "جدولة المنشورات", "تحليل الإحصائيات"]
        })
    
    # واجهات برمجة التطبيقات لإدارة الحسابات
    @app.route('/api/accounts', methods=['GET', 'POST'])
    @jwt_required()
    def manage_accounts():
        # الحصول على هوية المستخدم من الـ token
        current_user_id = get_jwt_identity()
        
        if request.method == 'GET':
            # جلب جميع الحسابات
            accounts = SocialAccount.query.filter_by(user_id=current_user_id).all()
            return jsonify({
                "accounts": [
                    {
                        "id": acc.id,
                        "platform": acc.platform,
                        "account_name": acc.account_name,
                        "is_active": acc.is_active,
                        "created_at": acc.created_at.isoformat()
                    } for acc in accounts
                ],
                "total": len(accounts),
                "user_id": current_user_id
            })
        
        elif request.method == 'POST':
            # إضافة حساب جديد
            data = request.get_json()
            new_account = SocialAccount(
                platform=data.get('platform'),
                account_name=data.get('account_name'),
                access_token=data.get('access_token'),
                user_id=current_user_id
            )
            db.session.add(new_account)
            db.session.commit()
            
            return jsonify({
                "message": "تم إضافة الحساب بنجاح",
                "account_id": new_account.id
            }), 201
    
    # واجهات برمجة التطبيقات لجدولة المنشورات
    @app.route('/api/schedule', methods=['GET', 'POST'])
    @jwt_required()
    def schedule_posts():
        current_user_id = get_jwt_identity()
        
        if request.method == 'GET':
            # جلب المنشورات المجدولة
            posts = ScheduledPost.query.filter_by(user_id=current_user_id).all()
            return jsonify({
                "scheduled_posts": [
                    {
                        "id": post.id,
                        "content": post.content,
                        "platforms": json.loads(post.platforms) if post.platforms else [],
                        "scheduled_time": post.scheduled_time.isoformat(),
                        "status": post.status,
                        "created_at": post.created_at.isoformat()
                    } for post in posts
                ],
                "total": len(posts)
            })
        
        elif request.method == 'POST':
            # جدولة منشور جديد
            data = request.get_json()
            new_post = ScheduledPost(
                content=data.get('content'),
                platforms=json.dumps(data.get('platforms', [])),
                scheduled_time=datetime.fromisoformat(data.get('scheduled_time')),
                user_id=current_user_id,
                status='scheduled'
            )
            db.session.add(new_post)
            db.session.commit()
            
            return jsonify({
                "message": "تم جدولة المنشور بنجاح",
                "post_id": new_post.id
            }), 201
    
    # واجهة تسجيل الدخول (مؤقتة للتطوير)
    @app.route('/api/auth/login', methods=['POST', 'GET'])
    def login():
        if request.method == 'GET':
            return jsonify({
                "message": "استخدم POST للحصول على token",
                "example": {
                    "method": "POST",
                    "url": "/api/auth/login",
                    "headers": {"Content-Type": "application/json"}
                }
            })
        
        # استخدام string كـ identity بدلاً من integer
        access_token = create_access_token(
            identity="user_1",  # استخدام string بدلاً من integer
            expires_delta=timedelta(days=30)
        )
        return jsonify({
            "access_token": access_token,
            "user_id": "user_1",
            "message": "تم تسجيل الدخول بنجاح",
            "expires_in": "30 يوم",
            "instructions": "استخدم هذا الـ token في header: Authorization: Bearer YOUR_TOKEN"
        })
    
    return app

if __name__ == '__main__':
    app = create_app()
    port = int(os.environ.get('PORT', 8080))
    app.run(debug=False, host='0.0.0.0', port=port)
