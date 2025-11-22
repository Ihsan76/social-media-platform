# -*- coding: utf-8 -*-
import os
import json
import hashlib
import uuid
from datetime import datetime
from flask import Flask, request, Response, render_template

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

# تخزين البيانات
users_db = {}
sessions = {}
social_accounts_db = {}

# استيراد نظام اللغات
from translations import get_translation, get_supported_languages, SUPPORTED_LANGUAGES

def get_user_language(request):
    """الحصول على لغة المستخدم المفضلة"""
    # أولاً: التحقق من الجلسة
    session_id = request.headers.get('Authorization', '').replace('Bearer ', '')
    if session_id and session_id in sessions:
        user_id = sessions[session_id]
        user = users_db.get(user_id)
        if user and user.preferences.get('language'):
            return user.preferences['language']
    
    # ثانياً: التحقق من header الطلب
    accept_language = request.headers.get('Accept-Language', '')
    if 'ar' in accept_language:
        return 'ar'
    elif 'fr' in accept_language:
        return 'fr'
    
    # ثالثاً: الافتراضي للإنجليزية
    return 'en'

def get_text(lang, key):
    """دالة مساعدة للحصول على النص المترجم"""
    return get_translation(lang, key)

def json_response(data, status=200):
    return Response(
        json.dumps(data, ensure_ascii=False, indent=2),
        mimetype='application/json; charset=utf-8',
        status=status
    )

def error_response(message, status=400, lang='en'):
    """إنشاء استجابة خطأ مترجمة"""
    translated_message = get_text(lang, message) if isinstance(message, str) and message in TRANSLATION_KEYS else message
    return json_response({"error": translated_message}, status)

def success_response(message, data=None, status=200, lang='en'):
    """إنشاء استجابة نجاح مترجمة"""
    translated_message = get_text(lang, message) if isinstance(message, str) and message in TRANSLATION_KEYS else message
    response = {"message": translated_message}
    if data:
        response.update(data)
    return json_response(response, status)

# قائمة مفاتيح الترجمات المستخدمة في API
TRANSLATION_KEYS = [
    'all_fields_required', 'password_min_length', 'email_exists', 'account_created',
    'login_success', 'invalid_credentials', 'unauthorized', 'user_not_found',
    'profile_loaded', 'social_connected', 'platform_not_supported', 'server_error'
]

# نماذج البيانات
class User:
    def __init__(self, user_id, username, email, password_hash=None, auth_method='email'):
        self.user_id = user_id
        self.username = username
        self.email = email
        self.password_hash = password_hash
        self.auth_method = auth_method
        self.created_at = datetime.utcnow()
        self.preferences = {
            "language": "en",
            "timezone": "UTC",
            "theme": "light"
        }
        self.social_logins = []
        self.is_active = True
    
    def to_dict(self, lang='en'):
        """تحويل الكائن إلى قاموس مع الترجمات"""
        return {
            "user_id": self.user_id,
            "username": self.username,
            "email": self.email,
            "auth_method": get_text(lang, self.auth_method) if self.auth_method in ['google', 'twitter', 'facebook', 'instagram', 'github'] else self.auth_method,
            "created_at": self.created_at.isoformat(),
            "preferences": self.preferences,
            "social_logins_count": len(self.social_logins),
            "is_active": self.is_active,
            "language": self.preferences.get('language', 'en')
        }
    
    def add_social_login(self, platform, social_id):
        """إضافة طريقة تسجيل دخول اجتماعية"""
        self.social_logins.append({
            "platform": platform,
            "social_id": social_id,
            "linked_at": datetime.utcnow()
        })

class SocialAccount:
    def __init__(self, account_id, platform, username, access_token, user_id):
        self.account_id = account_id
        self.platform = platform
        self.username = username
        self.access_token = access_token
        self.user_id = user_id
        self.connected_at = datetime.utcnow()
        self.stats = {"followers": 0, "posts": 0, "engagement": 0.0}
    
    def to_dict(self, lang='en'):
        """تحويل الكائن إلى قاموس مع الترجمات"""
        return {
            "account_id": self.account_id,
            "platform": get_text(lang, self.platform),
            "username": self.username,
            "connected_at": self.connected_at.isoformat(),
            "stats": self.stats
        }

# أدوات مساعدة
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def generate_session_id():
    return str(uuid.uuid4())

def get_current_user(session_id):
    user_id = sessions.get(session_id)
    return users_db.get(user_id) if user_id else None

def find_user_by_social_login(platform, social_id):
    """البحث عن مستخدم بواسطة حسابه الاجتماعي"""
    for user in users_db.values():
        for social_login in user.social_logins:
            if (social_login['platform'] == platform and 
                social_login['social_id'] == social_id):
                return user
    return None

def find_user_by_email(email):
    """البحث عن مستخدم بواسطة البريد الإلكتروني"""
    for user in users_db.values():
        if user.email.lower() == email.lower():
            return user
    return None

# المسارات الأساسية
@app.route('/')
def home():
    """الصفحة الرئيسية مع دعم اللغات"""
    lang = request.args.get('lang', 'en')
    if lang not in SUPPORTED_LANGUAGES:
        lang = 'en'
    
    return render_template('index.html', 
                         lang=lang,
                         languages=SUPPORTED_LANGUAGES,
                         translations=TRANSLATIONS.get(lang, {}))

@app.route('/api/')
def api_home():
    """الصفحة الرئيسية للـAPI مع دعم اللغات"""
    lang = get_user_language(request)
    data = {
        "message": get_text(lang, 'welcome'),
        "status": get_text(lang, 'active'),
        "version": "2.2.0",
        "language": lang,
        "supported_languages": SUPPORTED_LANGUAGES,
        "endpoints": {
            "auth": {
                "register": "/api/auth/register",
                "login": "/api/auth/login",
                "social_login": "/api/auth/social-login",
                "link_social": "/api/auth/link-social",
                "profile": "/api/auth/profile",
                "change_language": "/api/auth/change-language"
            },
            "social": {
                "connect": "/api/social/connect",
                "accounts": "/api/social/accounts"
            }
        }
    }
    return json_response(data)

# نظام المصادقة - التسجيل بالبريد الإلكتروني
@app.route('/api/auth/register', methods=['POST'])
def register():
    try:
        lang = get_user_language(request)
        data = request.get_json()
        if not data:
            return error_response('all_fields_required', 400, lang)
        
        username = data.get('username', '').strip()
        email = data.get('email', '').strip().lower()
        password = data.get('password', '').strip()
        preferred_lang = data.get('language', 'en')
        
        if not all([username, email, password]):
            return error_response('all_fields_required', 400, lang)
        
        if len(password) < 6:
            return error_response('password_min_length', 400, lang)
        
        # التحقق من وجود المستخدم
        existing_user = find_user_by_email(email)
        if existing_user:
            return error_response('email_exists', 400, lang)
        
        # إنشاء مستخدم جديد
        user_id = str(uuid.uuid4())
        new_user = User(
            user_id=user_id,
            username=username,
            email=email,
            password_hash=hash_password(password),
            auth_method='email'
        )
        new_user.preferences['language'] = preferred_lang if preferred_lang in SUPPORTED_LANGUAGES else 'en'
        
        users_db[user_id] = new_user
        
        # إنشاء جلسة
        session_id = generate_session_id()
        sessions[session_id] = user_id
        
        return success_response(
            'account_created',
            {
                "user": new_user.to_dict(preferred_lang),
                "session_id": session_id
            },
            201,
            preferred_lang
        )
    
    except Exception as e:
        lang = get_user_language(request)
        return error_response('server_error', 500, lang)

# نظام المصادقة - تسجيل الدخول بالبريد الإلكتروني
@app.route('/api/auth/login', methods=['POST'])
def login():
    try:
        lang = get_user_language(request)
        data = request.get_json()
        if not data:
            return error_response('all_fields_required', 400, lang)
        
        email = data.get('email', '').strip().lower()
        password = data.get('password', '').strip()
        
        if not all([email, password]):
            return error_response('all_fields_required', 400, lang)
        
        # البحث عن المستخدم
        user = find_user_by_email(email)
        if not user or user.password_hash != hash_password(password):
            return error_response('invalid_credentials', 401, lang)
        
        if not user.is_active:
            return error_response('unauthorized', 403, lang)
        
        # إنشاء جلسة
        session_id = generate_session_id()
        sessions[session_id] = user.user_id
        
        user_lang = user.preferences.get('language', 'en')
        
        return success_response(
            'login_success',
            {
                "user": user.to_dict(user_lang),
                "session_id": session_id
            },
            200,
            user_lang
        )
    
    except Exception as e:
        lang = get_user_language(request)
        return error_response('server_error', 500, lang)

# نظام المصادقة - التسجيل/الدخول عبر وسائل التواصل
@app.route('/api/auth/social-login', methods=['POST'])
def social_login():
    try:
        lang = get_user_language(request)
        data = request.get_json()
        if not data:
            return error_response('all_fields_required', 400, lang)
        
        platform = data.get('platform', '').strip().lower()
        social_id = data.get('social_id', '').strip()
        email = data.get('email', '').strip().lower()
        username = data.get('username', '').strip()
        preferred_lang = data.get('language', 'en')
        
        if not all([platform, social_id]):
            return error_response('all_fields_required', 400, lang)
        
        supported_platforms = ['google', 'twitter', 'facebook', 'instagram', 'github']
        if platform not in supported_platforms:
            return error_response('platform_not_supported', 400, lang)
        
        # البحث عن مستخدم موجود بنفس الحساب الاجتماعي
        existing_user = find_user_by_social_login(platform, social_id)
        
        if existing_user:
            # تسجيل دخول مستخدم موجود
            session_id = generate_session_id()
            sessions[session_id] = existing_user.user_id
            
            user_lang = existing_user.preferences.get('language', 'en')
            
            return success_response(
                'login_success',
                {
                    "user": existing_user.to_dict(user_lang),
                    "session_id": session_id,
                    "action": "login"
                },
                200,
                user_lang
            )
        else:
            # إنشاء حساب جديد
            user_id = str(uuid.uuid4())
            
            # إذا لم يتم提供 بريد إلكتروني، إنشاء بريد افتراضي
            if not email:
                email = f"{social_id}@{platform}.social"
            
            # إذا لم يتم提供 اسم مستخدم، إنشاء اسم افتراضي
            if not username:
                username = f"{platform}_user_{social_id[:8]}"
            
            new_user = User(
                user_id=user_id,
                username=username,
                email=email,
                auth_method=platform
            )
            new_user.preferences['language'] = preferred_lang if preferred_lang in SUPPORTED_LANGUAGES else 'en'
            
            # إضافة طريقة التسجيل الاجتماعي
            new_user.add_social_login(platform, social_id)
            
            users_db[user_id] = new_user
            
            # إنشاء جلسة
            session_id = generate_session_id()
            sessions[session_id] = user_id
            
            return success_response(
                'account_created',
                {
                    "user": new_user.to_dict(preferred_lang),
                    "session_id": session_id,
                    "action": "register"
                },
                201,
                preferred_lang
            )
    
    except Exception as e:
        lang = get_user_language(request)
        return error_response('server_error', 500, lang)

# تغيير لغة المستخدم
@app.route('/api/auth/change-language', methods=['POST'])
def change_language():
    try:
        session_id = request.headers.get('Authorization', '').replace('Bearer ', '')
        user = get_current_user(session_id)
        
        if not user:
            return error_response('unauthorized', 401, 'en')
        
        data = request.get_json()
        if not data:
            return error_response('all_fields_required', 400, user.preferences.get('language', 'en'))
        
        new_language = data.get('language', '').strip()
        if new_language not in SUPPORTED_LANGUAGES:
            return error_response('platform_not_supported', 400, user.preferences.get('language', 'en'))
        
        # تحديث لغة المستخدم
        user.preferences['language'] = new_language
        
        return success_response(
            'profile_loaded',
            {
                "user": user.to_dict(new_language),
                "language_changed": True,
                "new_language": new_language
            },
            200,
            new_language
        )
    
    except Exception as e:
        lang = get_user_language(request)
        return error_response('server_error', 500, lang)

# ربط حساب اجتماعي بحساب موجود
@app.route('/api/auth/link-social', methods=['POST'])
def link_social_account():
    try:
        session_id = request.headers.get('Authorization', '').replace('Bearer ', '')
        user = get_current_user(session_id)
        
        if not user:
            return error_response('unauthorized', 401, 'en')
        
        lang = user.preferences.get('language', 'en')
        data = request.get_json()
        if not data:
            return error_response('all_fields_required', 400, lang)
        
        platform = data.get('platform', '').strip().lower()
        social_id = data.get('social_id', '').strip()
        
        if not all([platform, social_id]):
            return error_response('all_fields_required', 400, lang)
        
        # التحقق إذا كان الحساب الاجتماعي مستخدماً مسبقاً
        existing_user = find_user_by_social_login(platform, social_id)
        if existing_user and existing_user.user_id != user.user_id:
            return error_response('email_exists', 400, lang)
        
        # إضافة طريقة التسجيل الاجتماعي
        user.add_social_login(platform, social_id)
        
        return success_response(
            'social_connected',
            {"user": user.to_dict(lang)},
            200,
            lang
        )
    
    except Exception as e:
        lang = get_user_language(request)
        return error_response('server_error', 500, lang)

@app.route('/api/auth/profile', methods=['GET'])
def get_profile():
    session_id = request.headers.get('Authorization', '').replace('Bearer ', '')
    user = get_current_user(session_id)
    
    if not user:
        return error_response('unauthorized', 401, 'en')
    
    lang = user.preferences.get('language', 'en')
    
    return success_response('profile_loaded', {"user": user.to_dict(lang)}, 200, lang)

# الحسابات الاجتماعية (لإدارة المحتوى)
@app.route('/api/social/connect', methods=['POST'])
def connect_social_account():
    try:
        session_id = request.headers.get('Authorization', '').replace('Bearer ', '')
        user = get_current_user(session_id)
        
        if not user:
            return error_response('unauthorized', 401, 'en')
        
        lang = user.preferences.get('language', 'en')
        data = request.get_json()
        if not data:
            return error_response('all_fields_required', 400, lang)
        
        platform = data.get('platform', '').strip().lower()
        username = data.get('username', '').strip()
        access_token = data.get('access_token', '').strip()
        
        if not all([platform, username, access_token]):
            return error_response('all_fields_required', 400, lang)
        
        supported_platforms = ['twitter', 'facebook', 'instagram', 'linkedin']
        if platform not in supported_platforms:
            return error_response('platform_not_supported', 400, lang)
        
        # إنشاء حساب اجتماعي
        account_id = str(uuid.uuid4())
        social_account = SocialAccount(account_id, platform, username, access_token, user.user_id)
        social_accounts_db[account_id] = social_account
        
        return success_response(
            'social_connected',
            {"account": social_account.to_dict(lang)},
            201,
            lang
        )
    
    except Exception as e:
        lang = get_user_language(request)
        return error_response('server_error', 500, lang)

@app.route('/api/social/accounts', methods=['GET'])
def get_social_accounts():
    try:
        session_id = request.headers.get('Authorization', '').replace('Bearer ', '')
        user = get_current_user(session_id)
        
        if not user:
            return error_response('unauthorized', 401, 'en')
        
        lang = user.preferences.get('language', 'en')
        
        # الحصول على حسابات المستخدم
        user_accounts = [acc for acc in social_accounts_db.values() if acc.user_id == user.user_id]
        accounts_data = [account.to_dict(lang) for account in user_accounts]
        
        return success_response(
            'profile_loaded',
            {
                "accounts": accounts_data,
                "total_accounts": len(accounts_data)
            },
            200,
            lang
        )
    
    except Exception as e:
        lang = get_user_language(request)
        return error_response('server_error', 500, lang)

# فحص صحة النظام
@app.route('/api/health')
def health():
    lang = get_user_language(request)
    data = {
        "status": get_text(lang, 'healthy'),
        "message": get_text(lang, 'service_normal'),
        "statistics": {
            "users_count": len(users_db),
            "active_sessions": len(sessions),
            "social_accounts": len(social_accounts_db)
        },
        "version": "2.2.0",
        "language": lang,
        "supported_languages": SUPPORTED_LANGUAGES,
        "auth_methods": ["email", "google", "twitter", "facebook", "instagram", "github"]
    }
    return json_response(data)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
