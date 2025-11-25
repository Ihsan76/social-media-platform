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
                .container { background: white; padding: 40px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); max-width: 800px; margin: 0 auto; }
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
                .btn { padding: 12px 24px; border: none; border-radius: 5px; cursor: pointer; font-size: 16px; margin: 10px; }
                .login-btn { background: #28a745; color: white; }
                .login-btn:hover { background: #218838; }
                .test-btn { background: #007bff; color: white; }
                .test-btn:hover { background: #0056b3; }
                .test-btn:disabled { background: #6c757d; cursor: not-allowed; }
                .token-display { background: #f8f9fa; padding: 15px; border-radius: 5px; margin: 15px 0; text-align: left; font-family: monospace; word-break: break-all; }
                .copy-btn { background: #6c757d; color: white; border: none; padding: 5px 10px; border-radius: 3px; cursor: pointer; margin-left: 10px; }
                .result { background: #e9ecef; padding: 15px; border-radius: 5px; margin: 15px 0; text-align: left; max-height: 300px; overflow-y: auto; }
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

                <!-- قسم الحصول على Token -->
                <div style="margin: 25px 0;">
                    <button class="btn login-btn" onclick="getAuthToken()">🔐 احصل على رمز الدخول (Token)</button>
                </div>

                <!-- عرض الـ Token -->
                <div id="tokenResult" style="display: none;">
                    <h3>🔑 رمز الدخول:</h3>
                    <div class="token-display">
                        <span id="tokenText"></span>
                        <button class="copy-btn" onclick="copyToken()">نسخ</button>
                    </div>
                    <p><small>استخدم هذا الرمز في رأس الطلبات: <code>Authorization: Bearer YOUR_TOKEN</code></small></p>
                    
                    <!-- أزرار تجربة الـ APIs -->
                    <div style="margin: 20px 0;">
                        <h4>🧪 تجربة الواجهات:</h4>
                        <button class="btn test-btn" onclick="testAccountsAPI()" id="testAccountsBtn">👥 جلب الحسابات</button>
                        <button class="btn test-btn" onclick="testScheduleAPI()" id="testScheduleBtn">📅 جلب المنشورات المجدولة</button>
                        <button class="btn test-btn" onclick="addSampleAccount()" id="addAccountBtn">➕ إضافة حساب تجريبي</button>
                    </div>
                    
                    <!-- عرض النتائج -->
                    <div id="apiResult" class="result" style="display: none;">
                        <h4>📊 النتيجة:</h4>
                        <pre id="resultText"></pre>
                    </div>
                </div>
                
                <div class="endpoints">
                    <h3>🔗 واجهات برمجة التطبيقات المتاحة:</h3>
                    <ul>
                        <li>📊 <a href="/api/health">/api/health</a> - حالة الخدمة</li>
                        <li>ℹ️ <a href="/api/version">/api/version</a> - معلومات النسخة</li>
                        <li>👥 <a href="/api/accounts">/api/accounts</a> - إدارة الحسابات <small>(تتطلب مصادقة)</small></li>
                        <li>📅 <a href="/api/schedule">/api/schedule</a> - جدولة المنشورات <small>(تتطلب مصادقة)</small></li>
                    </ul>
                </div>

                <div class="note">
                    <strong>💡 ملاحظة:</strong> بعض الواجهات تتطلب مصادقة. استخدم الزر أعلاه للحصول على token ثم جرب الواجهات.
                </div>
                
                <p style="margin-top: 30px;">
                    👉 <a href="https://github.com/Ihsan76/social-media-platform" style="color: #667eea; text-decoration: none; font-weight: bold;">تصفح المستودع على GitHub</a>
                </p>
            </div>

            <script>
                let currentToken = '';

                async function getAuthToken() {
                    try {
                        const response = await fetch('/api/auth/login', {
                            method: 'POST',
                            headers: {
                                'Content-Type': 'application/json'
                            }
                        });
                        
                        const data = await response.json();
                        
                        if (response.ok) {
                            currentToken = data.access_token;
                            document.getElementById('tokenText').textContent = currentToken;
                            document.getElementById('tokenResult').style.display = 'block';
                            
                            // تفعيل أزرار التجربة
                            document.getElementById('testAccountsBtn').disabled = false;
                            document.getElementById('testScheduleBtn').disabled = false;
                            document.getElementById('addAccountBtn').disabled = false;
                        } else {
                            alert('خطأ: ' + (data.message || 'فشل في الحصول على الرمز'));
                        }
                    } catch (error) {
                        alert('خطأ في الاتصال: ' + error.message);
                    }
                }

                function copyToken() {
                    navigator.clipboard.writeText(currentToken).then(() => {
                        alert('تم نسخ الرمز إلى الحافظة');
                    });
                }

                async function testAccountsAPI() {
                    if (!currentToken) {
                        alert('الرجاء الحصول على token أولاً');
                        return;
                    }

                    try {
                        const response = await fetch('/api/accounts', {
                            method: 'GET',
                            headers: {
                                'Authorization': `Bearer ${currentToken}`,
                                'Content-Type': 'application/json'
                            }
                        });
                        
                        const data = await response.json();
                        showResult(data);
                    } catch (error) {
                        showResult({ error: error.message });
                    }
                }

                async function testScheduleAPI() {
                    if (!currentToken) {
                        alert('الرجاء الحصول على token أولاً');
                        return;
                    }

                    try {
                        const response = await fetch('/api/schedule', {
                            method: 'GET',
                            headers: {
                                'Authorization': `Bearer ${currentToken}`,
                                'Content-Type': 'application/json'
                            }
                        });
                        
                        const data = await response.json();
                        showResult(data);
                    } catch (error) {
                        showResult({ error: error.message });
                    }
                }

                async function addSampleAccount() {
                    if (!currentToken) {
                        alert('الرجاء الحصول على token أولاً');
                        return;
                    }

                    try {
                        const response = await fetch('/api/accounts', {
                            method: 'POST',
                            headers: {
                                'Authorization': `Bearer ${currentToken}`,
                                'Content-Type': 'application/json'
                            },
                            body: JSON.stringify({
                                platform: 'twitter',
                                account_name: 'حساب_تجريبي',
                                access_token: 'token_12345'
                            })
                        });
                        
                        const data = await response.json();
                        showResult(data);
                    } catch (error) {
                        showResult({ error: error.message });
                    }
                }

                function showResult(data) {
                    document.getElementById('resultText').textContent = JSON.stringify(data, null, 2);
                    document.getElementById('apiResult').style.display = 'block';
                }
            </script>
        </body>
        </html>
        """
        return render_template_string(html_content)
    
    @app.route('/api/health')
    def health_check():
        try:
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
    
    @app.route('/api/accounts', methods=['GET', 'POST'])
    @jwt_required()
    def manage_accounts():
        current_user_id = get_jwt_identity()
        
        if request.method == 'GET':
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
    
    @app.route('/api/schedule', methods=['GET', 'POST'])
    @jwt_required()
    def schedule_posts():
        current_user_id = get_jwt_identity()
        
        if request.method == 'GET':
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
    
    @app.route('/api/auth/login', methods=['POST'])
    def login():
        access_token = create_access_token(
            identity="user_1",
            expires_delta=timedelta(days=30)
        )
        return jsonify({
            "access_token": access_token,
            "user_id": "user_1",
            "message": "تم تسجيل الدخول بنجاح",
            "expires_in": "30 يوم"
        })
    
    return app

if __name__ == '__main__':
    app = create_app()
    port = int(os.environ.get('PORT', 8080))
    app.run(debug=False, host='0.0.0.0', port=port)
