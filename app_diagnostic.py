from flask import Flask, render_template, session, redirect, url_for, request, jsonify
import json
import os
from datetime import datetime
import logging

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  # تأكد من تغيير هذا في الإنتاج

# إعداد التسجيل
logging.basicConfig(level=logging.DEBUG)

# تحميل الترجمة
def load_translations(lang='en'):
    """دالة تحميل الترجمة - هذه قد تكون مصدر المشكلة"""
    try:
        file_path = f'translations/{lang}.json'
        if not os.path.exists(file_path):
            logging.error(f"Translation file not found: {file_path}")
            return {"error": "Translation file not found"}
        
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            logging.debug(f"Loaded {len(data)} translations for {lang}")
            return data
    except Exception as e:
        logging.error(f"Error loading translations for {lang}: {str(e)}")
        return {"error": str(e)}

def get_translation(key, lang=None):
    """دالة جلب الترجمة - تحقق من هنا"""
    if lang is None:
        lang = session.get('language', 'en')
    
    translations = load_translations(lang)
    
    # 🔍 هذا قد يكون مصدر المشكلة - تحقق من القيمة الافتراضية
    result = translations.get(key, f"Translation missing: {key}")
    
    # تسجيل للتشخيص
    if "AAAA" in str(result):
        logging.warning(f"Found AAAA in translation for key: {key}")
    
    return result

# المسار الرئيسي
@app.route('/')
def index():
    """الصفحة الرئيسية - هنا يتم عرض البيانات"""
    lang = session.get('language', 'en')
    
    # 🔍 جلب البيانات التي قد تتحول إلى AAAA
    social_data = get_social_media_data()
    
    # تسجيل البيانات للتشخيص
    logging.debug(f"Social data type: {type(social_data)}")
    logging.debug(f"Social data length: {len(social_data) if isinstance(social_data, str) else 'N/A'}")
    
    return render_template('index.html', 
                         translations=load_translations(lang),
                         current_language=lang,
                         social_data=social_data)

def get_social_media_data():
    """دالة جلب بيانات الوسائط الاجتماعية - مصدر محتمل للمشكلة"""
    try:
        # 🔍 محاكاة جلب البيانات - هذه قد تكون المشكلة
        # إذا كانت هذه الدالة تعيد "A" * N
        test_data = "Real Social Media Data - " + datetime.now().strftime("%H:%M:%S")
        
        # محاكاة خطأ قد يسبب بيانات AAAA
        # if some_condition:
        #     return "A" * 1000  # ⚠️ هذا قد يكون موجوداً في كودك
        
        return test_data
    except Exception as e:
        logging.error(f"Error getting social media data: {str(e)}")
        return "Error loading data"

# تبديل اللغة
@app.route('/switch_language/<lang>')
def switch_language(lang):
    """تبديل اللغة - تحقق من تعيين الجلسة"""
    if lang in ['ar', 'en', 'fr']:
        session['language'] = lang
        logging.debug(f"Language switched to: {lang}")
    return redirect(request.referrer or url_for('index'))

# 🔧 مسارات التشخيص الجديدة
@app.route('/test_translations')
def test_translations():
    """فحص جميع ملفات الترجمة"""
    results = {}
    for lang in ['ar', 'en', 'fr']:
        try:
            translations = load_translations(lang)
            
            # البحث عن قيم AAAA في الترجمة
            aaaa_keys = []
            for key, value in translations.items():
                if isinstance(value, str) and "AAAA" in value:
                    aaaa_keys.append(key)
            
            results[lang] = {
                'status': 'success',
                'keys_count': len(translations),
                'has_aaaa': len(aaaa_keys) > 0,
                'aaaa_keys': aaaa_keys[:5],  # أول 5 مفاتيح تحتوي على AAAA
                'sample_data': str(list(translations.items())[:2])  # عينة صغيرة
            }
        except Exception as e:
            results[lang] = {
                'status': 'error',
                'error': str(e)
            }
    return jsonify(results)

@app.route('/debug_issue')
def debug_issue():
    """تشخيص كامل للمشكلة"""
    debug_info = {
        "timestamp": datetime.now().isoformat(),
        "session_language": session.get('language', 'en'),
        "debug_steps": []
    }
    
    # الخطوة 1: فحص الترجمة
    logging.debug("=== DEBUG TRANSLATIONS ===")
    for lang in ['ar', 'en', 'fr']:
        trans = load_translations(lang)
        step_info = {
            "language": lang,
            "keys_loaded": len(trans),
            "sample_keys": list(trans.keys())[:3] if trans else []
        }
        debug_info["debug_steps"].append(step_info)
        logging.debug(f"{lang}: {len(trans)} keys")
        
    # الخطوة 2: فحص سير البيانات
    logging.debug("=== DEBUG DATA FLOW ===")
    test_data = get_social_media_data()
    data_step = {
        "data_type": str(type(test_data)),
        "data_length": len(test_data) if isinstance(test_data, str) else 'N/A',
        "first_50_chars": test_data[:50] if isinstance(test_data, str) else str(test_data),
        "contains_aaaa": "AAAA" in str(test_data)
    }
    debug_info["debug_steps"].append(data_step)
    
    logging.debug(f"Data type: {type(test_data)}")
    logging.debug(f"Data length: {len(test_data) if isinstance(test_data, str) else 'N/A'}")
    logging.debug(f"First 100 chars: {test_data[:100] if isinstance(test_data, str) else test_data}")
    
    # الخطوة 3: فحص الترجمة لمفاتيح محددة
    test_keys = ['login', 'welcome', 'social_data', 'loading', 'error']
    translation_test = {}
    for key in test_keys:
        translation_test[key] = get_translation(key)
    debug_info["translation_test"] = translation_test
    
    return jsonify(debug_info)

@app.route('/test_data_flow')
def test_data_flow():
    """اختبار سير البيانات من البداية للنهاية"""
    test_steps = {}
    
    # 1. اختبر الترجمة
    test_steps['translation'] = get_translation('test_key')
    
    # 2. اختبر جلب البيانات
    test_steps['social_data'] = get_social_media_data()
    
    # 3. تحقق من وجود AAAA
    test_steps['contains_aaaa'] = any(
        "AAAA" in str(value) for value in test_steps.values()
    )
    
    # 4. فحص الجلسة
    test_steps['session'] = dict(session)
    
    return jsonify(test_steps)

@app.route('/check_translation_files')
def check_translation_files():
    """فحص محتوى ملفات الترجمة مباشرة"""
    results = {}
    for lang in ['ar', 'en', 'fr']:
        file_path = f'translations/{lang}.json'
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                results[lang] = {
                    'file_exists': True,
                    'file_size': len(content),
                    'first_200_chars': content[:200],
                    'has_aaaa': 'AAAA' in content
                }
        except Exception as e:
            results[lang] = {
                'file_exists': False,
                'error': str(e)
            }
    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
 