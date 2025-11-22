# -*- coding: utf-8 -*-
import os
import json
import hashlib
import uuid
from datetime import datetime
from flask import Flask, request, Response, render_template

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

# تخزين البيانات (مؤقت - سيتم استبداله بقاعدة بيانات)
users_db = {}
sessions = {}
social_accounts_db = {}

# نماذج البيانات
class User:
    def __init__(self, user_id, username, email, password_hash):
        self.user_id = user_id
        self.username = username
        self.email = email
        self.password_hash = password_hash
        self.created_at = datetime.utcnow()
        self.preferences = {"language": "ar", "timezone": "Asia/Riyadh"}
    
    def to_dict(self):
        return {
            "user_id": self.user_id,
            "username": self.username,
            "email": self.email,
            "created_at": self.created_at.isoformat(),
            "preferences": self.preferences
        }

class SocialAccount:
    def __init__(self, account_id, platform, username, access_token, user_id):
        self.account_id = account_id
        self.platform = platform
        self.username = username
        self.access_token = access_token
        self.user_id = user_id
        self.connected_at = datetime.utcnow()
        self.stats = {"followers": 0, "posts": 0, "engagement": 0.0}
    
    def to_dict(self):
        return {
            "account_id": self.account_id,
            "platform": self.platform,
            "username": self.username,
            "connected_at": self.connected_at.isoformat(),
            "stats": self.stats
        }

# أدوات مساعدة
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def generate_session_id():
    return str(uuid.uuid4())

def json_response(data, status=200):
    return Response(
        json.dumps(data, ensure_ascii=False, indent=2),
        mimetype='application/json; charset=utf-8',
        status=status
    )

def error_response(message, status=400):
    return json_response({"error": message}, status)

def success_response(message, data=None, status=200):
    response = {"message": message}
    if data:
        response.update(data)
    return json_response(response, status)

def get_current_user(session_id):
    user_id = sessions.get(session_id)
    return users_db.get(user_id) if user_id else None

# المسارات الأساسية
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/')
def api_home():
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
                "accounts": "/api/social/accounts"
            }
        }
    }
    return json_response(data)

# نظام المصادقة
@app.route('/api/auth/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        if not data:
            return error_response("يجب إرسال بيانات JSON")
        
        username = data.get('username', '').strip()
        email = data.get('email', '').strip().lower()
        password = data.get('password', '').strip()
        
        if not all([username, email, password]):
            return error_response("جميع الحقول مطلوبة")
        
        if len(password) < 6:
            return error_response("كلمة المرور يجب أن تكون 6 أحرف على الأقل")
        
        # التحقق من وجود المستخدم
        for user in users_db.values():
            if user.email == email:
                return error_response("البريد الإلكتروني مستخدم مسبقاً")
        
        # إنشاء مستخدم جديد
        user_id = str(uuid.uuid4())
        new_user = User(user_id, username, email, hash_password(password))
        users_db[user_id] = new_user
        
        # إنشاء جلسة
        session_id = generate_session_id()
        sessions[session_id] = user_id
        
        return success_response(
            "تم إنشاء الحساب بنجاح!",
            {
                "user": new_user.to_dict(),
                "session_id": session_id
            },
            201
        )
    
    except Exception as e:
        return error_response("حدث خطأ في السيرفر", 500)

@app.route('/api/auth/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        if not data:
            return error_response("يجب إرسال بيانات JSON")
        
        email = data.get('email', '').strip().lower()
        password = data.get('password', '').strip()
        
        if not all([email, password]):
            return error_response("البريد الإلكتروني وكلمة المرور مطلوبان")
        
        # البحث عن المستخدم
        user = None
        for u in users_db.values():
            if u.email == email and u.password_hash == hash_password(password):
                user = u
                break
        
        if not user:
            return error_response("البريد الإلكتروني أو كلمة المرور غير صحيحة", 401)
        
        # إنشاء جلسة
        session_id = generate_session_id()
        sessions[session_id] = user.user_id
        
        return success_response(
            "تم تسجيل الدخول بنجاح!",
            {
                "user": user.to_dict(),
                "session_id": session_id
            }
        )
    
    except Exception as e:
        return error_response("حدث خطأ في السيرفر", 500)

@app.route('/api/auth/profile', methods=['GET'])
def get_profile():
    session_id = request.headers.get('Authorization', '').replace('Bearer ', '')
    user = get_current_user(session_id)
    
    if not user:
        return error_response("غير مصرح بالوصول", 401)
    
    return success_response("تم تحميل الملف الشخصي", {"user": user.to_dict()})

# الحسابات الاجتماعية
@app.route('/api/social/connect', methods=['POST'])
def connect_social_account():
    try:
        session_id = request.headers.get('Authorization', '').replace('Bearer ', '')
        user = get_current_user(session_id)
        
        if not user:
            return error_response("غير مصرح بالوصول", 401)
        
        data = request.get_json()
        if not data:
            return error_response("يجب إرسال بيانات JSON")
        
        platform = data.get('platform', '').strip().lower()
        username = data.get('username', '').strip()
        access_token = data.get('access_token', '').strip()
        
        if not all([platform, username, access_token]):
            return error_response("جميع الحقول مطلوبة")
        
        supported_platforms = ['twitter', 'facebook', 'instagram', 'linkedin']
        if platform not in supported_platforms:
            return error_response(f"المنصة غير مدعومة. المنصات المدعومة: {', '.join(supported_platforms)}")
        
        # إنشاء حساب اجتماعي
        account_id = str(uuid.uuid4())
        social_account = SocialAccount(account_id, platform, username, access_token, user.user_id)
        social_accounts_db[account_id] = social_account
        
        return success_response(
            f"تم ربط حساب {platform} بنجاح!",
            {"account": social_account.to_dict()},
            201
        )
    
    except Exception as e:
        return error_response("حدث خطأ في السيرفر", 500)

@app.route('/api/social/accounts', methods=['GET'])
def get_social_accounts():
    try:
        session_id = request.headers.get('Authorization', '').replace('Bearer ', '')
        user = get_current_user(session_id)
        
        if not user:
            return error_response("غير مصرح بالوصول", 401)
        
        # الحصول على حسابات المستخدم
        user_accounts = [acc for acc in social_accounts_db.values() if acc.user_id == user.user_id]
        accounts_data = [account.to_dict() for account in user_accounts]
        
        return success_response(
            "تم تحميل الحسابات الاجتماعية",
            {
                "accounts": accounts_data,
                "total_accounts": len(accounts_data)
            }
        )
    
    except Exception as e:
        return error_response("حدث خطأ في السيرفر", 500)

# فحص صحة النظام
@app.route('/api/health')
def health():
    data = {
        "status": "صحي",
        "message": "الخدمة تعمل بشكل طبيعي",
        "statistics": {
            "users_count": len(users_db),
            "active_sessions": len(sessions),
            "social_accounts": len(social_accounts_db)
        },
        "version": "2.0.0"
    }
    return json_response(data)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
