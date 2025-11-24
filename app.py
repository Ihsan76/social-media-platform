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

# نظام إدارة الترجمة
class TranslationManager:
    def __init__(self):
        self.translations_dir = "translations"
        self.languages_file = os.path.join(self.translations_dir, "languages.json")
        self.ensure_directories()
    
    def ensure_directories(self):
        """إنشاء المجلدات الضرورية"""
        if not os.path.exists(self.translations_dir):
            os.makedirs(self.translations_dir)
        if not os.path.exists('templates/admin'):
            os.makedirs('templates/admin')
    
    def get_all_languages(self):
        """الحصول على جميع اللغات المدعومة"""
        try:
            with open(self.languages_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {
                "ar": {"name": "العربية", "native_name": "العربية", "direction": "rtl", "enabled": True},
                "en": {"name": "English", "native_name": "English", "direction": "ltr", "enabled": True},
                "fr": {"name": "French", "native_name": "Français", "direction": "ltr", "enabled": True}
            }
    
    def save_languages(self, languages):
        with open(self.languages_file, 'w', encoding='utf-8') as f:
            json.dump(languages, f, ensure_ascii=False, indent=2)
    
    def get_translation_keys(self):
        all_keys = set()
        for lang_file in os.listdir(self.translations_dir):
            if lang_file.endswith('.json') and lang_file != 'languages.json':
                try:
                    with open(os.path.join(self.translations_dir, lang_file), 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        self._extract_keys(data, '', all_keys)
                except Exception as e:
                    print(f"Error reading {lang_file}: {e}")
        return sorted(list(all_keys))
    
    def _extract_keys(self, data, current_path, keys_set):
        for key, value in data.items():
            new_path = f"{current_path}.{key}" if current_path else key
            if isinstance(value, dict):
                self._extract_keys(value, new_path, keys_set)
            else:
                keys_set.add(new_path)
    
    def get_translation_file(self, lang):
        file_path = os.path.join(self.translations_dir, f"{lang}.json")
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {}
    
    def save_translation_file(self, lang, data):
        file_path = os.path.join(self.translations_dir, f"{lang}.json")
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def update_translation(self, lang, key, value):
        data = self.get_translation_file(lang)
        keys = key.split('.')
        
        current = data
        for k in keys[:-1]:
            if k not in current:
                current[k] = {}
            current = current[k]
        
        current[keys[-1]] = value
        self.save_translation_file(lang, data)
        return True
    
    def add_new_key(self, key, translations):
        for lang, value in translations.items():
            self.update_translation(lang, key, value)
        return True
    
    def delete_key(self, key):
        for lang_file in os.listdir(self.translations_dir):
            if lang_file.endswith('.json') and lang_file != 'languages.json':
                lang = lang_file.replace('.json', '')
                data = self.get_translation_file(lang)
                self._delete_key_from_data(data, key.split('.'))
                self.save_translation_file(lang, data)
        return True
    
    def _delete_key_from_data(self, data, keys):
        if len(keys) == 1:
            if keys[0] in data:
                del data[keys[0]]
        else:
            if keys[0] in data:
                self._delete_key_from_data(data[keys[0]], keys[1:])
                if not data[keys[0]]:
                    del data[keys[0]]

# تهيئة مدير الترجمة
translation_manager = TranslationManager()

# دالة تحميل الترجمات
def load_translations(lang='en'):
    """دالة تحميل الترجمة"""
    try:
        return translation_manager.get_translation_file(lang)
    except Exception as e:
        print(f"Error loading translation for {lang}: {e}")
        return {}

# تحميل الترجمات
TRANSLATIONS = {
    'ar': load_translations('ar'),
    'en': load_translations('en'), 
    'fr': load_translations('fr')
}

# الحصول على اللغات المدعومة
SUPPORTED_LANGUAGES = ['ar', 'en', 'fr']

def get_language_direction(lang):
    """الحصول على اتجاه اللغة"""
    languages = translation_manager.get_all_languages()
    return languages.get(lang, {}).get('direction', 'ltr')

def get_translation(lang, key):
    """دالة احتياطية للحصول على الترجمة"""
    return TRANSLATIONS.get(lang, {}).get(key, key)

def get_supported_languages():
    """دالة احتياطية للحصول على اللغات المدعومة"""
    return SUPPORTED_LANGUAGES

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

def is_translation_key(key):
    """التحقق ديناميكياً إذا كان المفتاح موجوداً في أي لغة"""
    def search_in_dict(data, search_key):
        """بحث متكرر في القاموس"""
        if isinstance(data, dict):
            if search_key in data:
                return True
            for value in data.values():
                if search_in_dict(value, search_key):
                    return True
        return False
    
    # البحث في جميع اللغات
    for lang_data in TRANSLATIONS.values():
        if search_in_dict(lang_data, key):
            return True
    return False

def get_text(lang, key):
    """دالة مساعدة للحصول على النص المترجم - محسنة للهياكل المتداخلة"""
    try:
        # إذا كان المفتاح يحتوي على نقاط (هيكل متداخل)
        if '.' in key:
            # الحصول على بيانات الترجمة للغة المطلوبة
            translations_data = TRANSLATIONS.get(lang, TRANSLATIONS.get('en', {}))
            
            # البحث عن المفتاح في الهيكل المتداخل
            keys = key.split('.')
            value = translations_data
            
            for k in keys:
                if isinstance(value, dict) and k in value:
                    value = value[k]
                else:
                    # إذا لم يتم العثور على الترجمة، حاول الإنجليزية
                    if lang != 'en':
                        return get_text('en', key)
                    return key  # إرجاع المفتاح نفسه إذا لم توجد ترجمة
            
            return value
        else:
            # للمفاتيح البسيطة
            return TRANSLATIONS.get(lang, {}).get(key, 
                   TRANSLATIONS.get('en', {}).get(key, key))
    except Exception as e:
        print(f"Translation error for key '{key}' in language '{lang}': {e}")
        # حاول الإنجليزية كبديل
        if lang != 'en':
            return get_text('en', key)
        return key

# إضافة دالة مساعدة للقوالب - آمنة ولا تؤثر على النظام الحالي
@app.context_processor
def utility_processor():
    def get_translation_template(key, default=None):
        """دالة مساعدة للقوالب للحصول على الترجمة"""
        lang = request.args.get('lang', 'en')
        result = get_text(lang, key)
        # إذا كانت النتيجة هي المفتاح نفسه (لم توجد ترجمة)، استخدم القيمة الافتراضية
        return result if result != key else (default if default else key)
    
    return dict(get_text=get_text, get_translation=get_translation_template)

def json_response(data, status=200):
    return Response(
        json.dumps(data, ensure_ascii=False, indent=2),
        mimetype='application/json; charset=utf-8',
        status=status
    )

def error_response(message, status=400, lang='en'):
    """إنشاء استجابة خطأ مترجمة"""
    translated_message = get_text(lang, message) if is_translation_key(message) else message
    return json_response({"error": translated_message}, status)

def success_response(message, data=None, status=200, lang='en'):
    """إنشاء استجابة نجاح مترجمة"""
    translated_message = get_text(lang, message) if is_translation_key(message) else message
    response = {"message": translated_message}
    if data:
        response.update(data)
    return json_response(response, status)

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
    """البحق عن مستخدم بواسطة البريد الإلكتروني"""
    for user in users_db.values():
        if user.email.lower() == email.lower():
            return user
    return None

# المسارات الأساسية
@app.route('/')
def index():
    """الصفحة الرئيسية الجديدة"""
    lang = request.args.get('lang', 'en')
    if lang not in SUPPORTED_LANGUAGES:
        lang = 'en'
    
    text_direction = get_language_direction(lang)
    languages_data = translation_manager.get_all_languages()
    current_language_name = languages_data.get(lang, {}).get('native_name', lang)
    
    return render_template('index.html', 
                         lang=lang,
                         text_direction=text_direction,
                         languages=languages_data,
                         current_language_name=current_language_name,
                         translations=TRANSLATIONS.get(lang, {}))

@app.route('/login')
def login_page():
    """صفحة تسجيل الدخول"""
    lang = request.args.get('lang', 'en')
    if lang not in SUPPORTED_LANGUAGES:
        lang = 'en'
    
    text_direction = get_language_direction(lang)
    languages_data = translation_manager.get_all_languages()
    current_language_name = languages_data.get(lang, {}).get('native_name', lang)
    
    return render_template('login.html', 
                         lang=lang,
                         text_direction=text_direction,
                         languages=languages_data,
                         current_language_name=current_language_name,
                         translations=TRANSLATIONS.get(lang, {}))

# إضافة alias للتوافق مع القوالب
@app.route('/login')
def login():
    """Alias for login_page for template compatibility"""
    return login_page()

@app.route('/dashboard')
def dashboard():
    """لوحة التحكم بعد تسجيل الدخول"""
    lang = request.args.get('lang', 'en')
    if lang not in SUPPORTED_LANGUAGES:
        lang = 'en'
    
    text_direction = get_language_direction(lang)
    languages_data = translation_manager.get_all_languages()
    current_language_name = languages_data.get(lang, {}).get('native_name', lang)
    
    return render_template('dashboard.html', 
                         lang=lang,
                         text_direction=text_direction,
                         languages=languages_data,
                         current_language_name=current_language_name,
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
def api_login():
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

# ===== مسارات إدارة الترجمة الجديدة =====

@app.route('/admin/translation-manager')
def translation_manager_page():
    """صفحة إدارة الترجمة"""
    lang = request.args.get('lang', 'ar')
    
    languages = translation_manager.get_all_languages()
    translation_keys = translation_manager.get_translation_keys()
    enabled_languages = sum(1 for info in languages.values() if info.get('enabled', True))
    
    def get_translation_value(key, lang_code):
        """دالة مساعدة للحصول على قيمة ترجمة محددة"""
        data = translation_manager.get_translation_file(lang_code)
        keys = key.split('.')
        value = data
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return ""
        return value if isinstance(value, str) else ""
    
    return render_template('admin/translation_manager.html',
                         lang=lang,
                         languages=languages,
                         translation_keys=translation_keys,
                         enabled_languages=enabled_languages,
                         get_translation_value=get_translation_value)

# مسارات API للإدارة
@app.route('/admin/toggle-language', methods=['POST'])
def toggle_language():
    """تفعيل/تعطيل لغة"""
    data = request.get_json()
    lang = data.get('lang')
    enabled = data.get('enabled')
    
    languages = translation_manager.get_all_languages()
    if lang in languages:
        languages[lang]['enabled'] = enabled
        translation_manager.save_languages(languages)
        return json_response({"success": True})
    
    return json_response({"success": False, "message": "اللغة غير موجودة"})

@app.route('/admin/add-language', methods=['POST'])
def add_language():
    """إضافة لغة جديدة"""
    data = request.get_json()
    code = data.get('code')
    name = data.get('name')
    native_name = data.get('native_name')
    direction = data.get('direction')
    
    if not code or not name or not native_name:
        return json_response({"success": False, "message": "جميع الحقول مطلوبة"})
    
    languages = translation_manager.get_all_languages()
    if code in languages:
        return json_response({"success": False, "message": "اللغة موجودة مسبقاً"})
    
    languages[code] = {
        "name": name,
        "native_name": native_name,
        "direction": direction,
        "enabled": True
    }
    
    translation_manager.save_languages(languages)
    
    # إنشاء ملف ترجمة فارغ للغة الجديدة
    translation_manager.save_translation_file(code, {})
    
    return json_response({"success": True})

@app.route('/admin/update-translation', methods=['POST'])
def update_translation():
    """تحديث ترجمة محددة"""
    data = request.get_json()
    key = data.get('key')
    lang = data.get('lang')
    value = data.get('value')
    
    if translation_manager.update_translation(lang, key, value):
        return json_response({"success": True})
    
    return json_response({"success": False})

@app.route('/admin/add-translation-key', methods=['POST'])
def add_translation_key():
    """إضافة مفتاح ترجمة جديد"""
    data = request.get_json()
    key = data.get('key')
    translations = data.get('translations', {})
    
    if not key:
        return json_response({"success": False, "message": "مفتاح الترجمة مطلوب"})
    
    if translation_manager.add_new_key(key, translations):
        return json_response({"success": True})
    
    return json_response({"success": False})

@app.route('/admin/delete-translation-key', methods=['POST'])
def delete_translation_key():
    """حذف مفتاح ترجمة"""
    data = request.get_json()
    key = data.get('key')
    
    if translation_manager.delete_key(key):
        return json_response({"success": True})
    
    return json_response({"success": False})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)