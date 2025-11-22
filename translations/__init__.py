# ملف تهيئة مجلد الترجمات
import os
import json

def load_translations():
    """تحميل جميع ملفات الترجمات"""
    translations = {}
    translations_dir = os.path.join(os.path.dirname(__file__))
    
    for filename in os.listdir(translations_dir):
        if filename.endswith('.json') and filename != '__init__.py':
            lang_code = filename.replace('.json', '')
            filepath = os.path.join(translations_dir, filename)
            
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    translations[lang_code] = json.load(f)
            except Exception as e:
                print(f"Error loading translation file {filename}: {e}")
    
    return translations

# تحميل الترجمات عند الاستيراد
TRANSLATIONS = load_translations()
SUPPORTED_LANGUAGES = {
    'ar': {'name': 'العربية', 'dir': 'rtl', 'flag': '🇸🇦'},
    'en': {'name': 'English', 'dir': 'ltr', 'flag': '🇺🇸'},
    'fr': {'name': 'Français', 'dir': 'ltr', 'flag': '🇫🇷'}
}

def get_translation(lang, key):
    """الحصول على ترجمة للنص"""
    if lang in TRANSLATIONS and key in TRANSLATIONS[lang]:
        return TRANSLATIONS[lang][key]
    elif 'en' in TRANSLATIONS and key in TRANSLATIONS['en']:
        return TRANSLATIONS['en'][key]  # Fallback to English
    return key  # Fallback to key itself

def get_supported_languages():
    """الحصول على اللغات المدعومة"""
    return SUPPORTED_LANGUAGES
