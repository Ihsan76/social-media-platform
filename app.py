# -*- coding: utf-8 -*-
import os
import json
from flask import Flask, request, Response
from models import User, SocialAccount
from datetime import datetime
import hashlib
import uuid

app = Flask(__name__)

# تخزين مؤقت (سيتم استبداله بقاعدة بيانات لاحقاً)
users_db = {}
sessions = {}

# وظائف مساعدة
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def create_session(user_id):
    session_id = str(uuid.uuid4())
    sessions[session_id] = user_id
    return session_id

# المسارات الأساسية
@app.route('/')
def home():
    data = {
        "message": "مرحباً! منصة إدارة الوسائط الاجتماعية تعمل بنجاح! 🚀",
        "status": "نشط",
        "version": "1.0.0",
        "endpoints": {
            "auth": {
                "register": "/auth/register",
                "login": "/auth/login",
                "profile": "/auth/profile"
            },
            "social": {
                "connect": "/social/connect",
                "accounts": "/social/accounts"
            }
        }
    }
    return Response(json.dumps(data, ensure_ascii=False, indent=2), mimetype='application/json; charset=utf-8')

# نظام المصادقة
@app.route('/auth/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        
        if not all([username, email, password]):
            return Response(json.dumps({"error": "جميع الحقول مطلوبة"}, ensure_ascii=False), 
                          mimetype='application/json; charset=utf-8', status=400)
        
        # التحقق من وجود المستخدم
        for user in users_db.values():
            if user.email == email or user.username == username:
                return Response(json.dumps({"error": "المستخدم موجود مسبقاً"}, ensure_ascii=False), 
                              mimetype='application/json; charset=utf-8', status=400)
        
        # إنشاء مستخدم جديد
        user_id = str(uuid.uuid4())
        new_user = User(
            user_id=user_id,
            username=username,
            email=email,
            password_hash=hash_password(password)
        )
        
        users_db[user_id] = new_user
        session_id = create_session(user_id)
        
        response_data = {
            "message": "تم إنشاء الحساب بنجاح!",
            "user": new_user.to_dict(),
            "session_id": session_id
        }
        
        return Response(json.dumps(response_data, ensure_ascii=False, indent=2), 
                      mimetype='application/json; charset=utf-8', status=201)
    
    except Exception as e:
        return Response(json.dumps({"error": "حدث خطأ في السيرفر"}, ensure_ascii=False), 
                      mimetype='application/json; charset=utf-8', status=500)

@app.route('/auth/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    
    # البحث عن المستخدم
    user = None
    for u in users_db.values():
        if u.email == email and u.password_hash == hash_password(password):
            user = u
            break
    
    if not user:
        return Response(json.dumps({"error": "البريد الإلكتروني أو كلمة المرور غير صحيحة"}, ensure_ascii=False), 
                      mimetype='application/json; charset=utf-8', status=401)
    
    session_id = create_session(user.user_id)
    
    response_data = {
        "message": "تم تسجيل الدخول بنجاح!",
        "user": user.to_dict(),
        "session_id": session_id
    }
    
    return Response(json.dumps(response_data, ensure_ascii=False, indent=2), 
                  mimetype='application/json; charset=utf-8')

@app.route('/auth/profile', methods=['GET'])
def get_profile():
    session_id = request.headers.get('Authorization', '').replace('Bearer ', '')
    user_id = sessions.get(session_id)
    
    if not user_id or user_id not in users_db:
        return Response(json.dumps({"error": "غير مصرح بالوصول"}, ensure_ascii=False), 
                      mimetype='application/json; charset=utf-8', status=401)
    
    user = users_db[user_id]
    return Response(json.dumps(user.to_dict(), ensure_ascii=False, indent=2), 
                  mimetype='application/json; charset=utf-8')

# المسارات الأخرى
@app.route('/health')
def health():
    data = {"status": "صحي", "message": "الخدمة تعمل بشكل طبيعي", "users_count": len(users_db)}
    return Response(json.dumps(data, ensure_ascii=False, indent=2), mimetype='application/json; charset=utf-8')

@app.route('/test')
def test():
    data = {
        "test_arabic": "اختبار النص العربي ✅",
        "welcome": "أهلاً وسهلاً في منصتنا"
    }
    return Response(json.dumps(data, ensure_ascii=False, indent=2), mimetype='application/json; charset=utf-8')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
