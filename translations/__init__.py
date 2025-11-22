import json
import os

# إعدادات اللغات المدعومة
SUPPORTED_LANGUAGES = {
    'ar': {'name': 'العربية', 'dir': 'rtl', 'flag': '🇸🇦'},
    'en': {'name': 'English', 'dir': 'ltr', 'flag': '🇺🇸'},
    'fr': {'name': 'Français', 'dir': 'ltr', 'flag': '🇫🇷'}
}

def get_supported_languages():
    """الحصول على اللغات المدعومة"""
    return SUPPORTED_LANGUAGES

def load_translation_file(lang):
    """تحميل ملف الترجمة"""
    try:
        file_path = f'translations/{lang}.json'
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        return {}

def get_translation(lang, key):
    """الحصول على ترجمة محددة"""
    translations = load_translation_file(lang)
    return translations.get(key, key)

# 🔥 أضف هذه الدالة المفقودة
def get_language_direction(lang):
    """الحصول على اتجاه اللغة"""
    return SUPPORTED_LANGUAGES.get(lang, {}).get('dir', 'ltr')

def get_language_name(lang):
    """الحصول على اسم اللغة"""
    return SUPPORTED_LANGUAGES.get(lang, {}).get('name', 'Unknown')
