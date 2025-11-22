# -*- coding: utf-8 -*-
from flask import Blueprint, request
from models.user import UserManager
from utils.helpers import hash_password, success_response, error_response, generate_session_id

# إنشاء Blueprint للمصادقة
auth_bp = Blueprint('auth', __name__)

# إدارة المستخدمين والجلسات
user_manager = UserManager()
sessions = {}  # session_id -> user_id

@auth_bp.route('/register', methods=['POST'])
def register():
    """تسجيل مستخدم جديد"""
    try:
        data = request.get_json()
        if not data:
            return error_response("يجب إرسال بيانات JSON")
        
        username = data.get('username', '').strip()
        email = data.get('email', '').strip().lower()
        password = data.get('password', '').strip()
        
        # التحقق من البيانات
        if not all([username, email, password]):
            return error_response("جميع الحقول مطلوبة")
        
        if len(password) < 6:
            return error_response("كلمة المرور يجب أن تكون 6 أحرف على الأقل")
        
        try:
            # إنشاء المستخدم
            user = user_manager.create_user(
                username=username,
                email=email,
                password_hash=hash_password(password)
            )
            
            # إنشاء جلسة
            session_id = generate_session_id()
            sessions[session_id] = user.user_id
            
            return success_response(
                "تم إنشاء الحساب بنجاح!",
                {
                    "user": user.to_dict(),
                    "session_id": session_id
                },
                201
            )
            
        except ValueError as e:
            return error_response(str(e))
    
    except Exception as e:
        return error_response("حدث خطأ في السيرفر", 500)

@auth_bp.route('/login', methods=['POST'])
def login():
    """تسجيل دخول المستخدم"""
    try:
        data = request.get_json()
        if not data:
            return error_response("يجب إرسال بيانات JSON")
        
        email = data.get('email', '').strip().lower()
        password = data.get('password', '').strip()
        
        if not all([email, password]):
            return error_response("البريد الإلكتروني وكلمة المرور مطلوبان")
        
        # مصادقة المستخدم
        user = user_manager.authenticate_user(email, hash_password(password))
        if not user:
            return error_response("البريد الإلكتروني أو كلمة المرور غير صحيحة", 401)
        
        # إنشاء جلسة جديدة
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

@auth_bp.route('/profile', methods=['GET'])
def get_profile():
    """الحصول على الملف الشخصي"""
    session_id = request.headers.get('Authorization', '').replace('Bearer ', '')
    user_id = sessions.get(session_id)
    
    if not user_id:
        return error_response("غير مصرح بالوصول", 401)
    
    user = user_manager.get_user_by_id(user_id)
    if not user:
        return error_response("المستخدم غير موجود", 404)
    
    return success_response("تم تحميل الملف الشخصي", {"user": user.to_dict()})

def get_current_user(session_id):
    """الحصول على المستخدم الحالي من الجلسة"""
    user_id = sessions.get(session_id)
    return user_manager.get_user_by_id(user_id) if user_id else None
