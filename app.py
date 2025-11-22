from flask import Flask, render_template, session, redirect, url_for, request, jsonify
import json
import os
from datetime import datetime
import logging

app = Flask(__name__)
app.secret_key = 'diagnostic-secret-key-12345'

# إعداد التسجيل
logging.basicConfig(level=logging.DEBUG)

def load_translations(lang='en'):
    """دالة تحميل الترجمة"""
    try:
        file_path = f'translations/{lang}.json'
        if not os.path.exists(file_path):
            return {"error": "ملف الترجمة غير موجود"}
        
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        return {"error": f"خطأ في تحميل الترجمة: {str(e)}"}

@app.route('/')
def index():
    """الصفحة الرئيسية"""
    lang = session.get('language', 'en')
    translations = load_translations(lang)
    
    # تسجيل للتشخيص
    app.logger.info(f"اللغة الحالية: {lang}")
    app.logger.info(f"عدد مفاتيح الترجمة: {len(translations)}")
    
    return render_template('index.html', 
                         translations=translations,
                         current_language=lang)

@app.route('/switch_language/<lang>')
def switch_language(lang):
    """تبديل اللغة"""
    if lang in ['ar', 'en', 'fr']:
        session['language'] = lang
    return redirect(url_for('index'))

# 🔍 مسارات التشخيص
@app.route('/debug')
def debug():
    """فحص كامل للنظام"""
    results = {
        "timestamp": datetime.now().isoformat(),
        "session": dict(session),
        "translations": {}
    }
    
    # فحص كل اللغات
    for lang in ['ar', 'en', 'fr']:
        trans = load_translations(lang)
        
        # البحث عن AAAA في القيم
        aaaa_keys = []
        for key, value in trans.items():
            if isinstance(value, str) and 'AAAA' in value:
                aaaa_keys.append(key)
        
        results["translations"][lang] = {
            "total_keys": len(trans),
            "has_aaaa": len(aaaa_keys) > 0,
            "aaaa_keys": aaaa_keys[:10],  # أول 10 مفاتيح تحتوي على AAAA
            "sample_values": list(trans.items())[:3]  # عينة من القيم
        }
    
    return jsonify(results)

@app.route('/check_files')
def check_files():
    """فحص الملفات مباشرة"""
    results = {}
    for lang in ['ar', 'en', 'fr']:
        file_path = f'translations/{lang}.json'
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                results[lang] = {
                    "exists": True,
                    "size": len(content),
                    "first_100_chars": content[:100],
                    "has_aaaa": "AAAA" in content
                }
        except Exception as e:
            results[lang] = {
                "exists": False,
                "error": str(e)
            }
    
    return jsonify(results)

@app.route('/simple_test')
def simple_test():
    """اختبار بسيط"""
    lang = session.get('language', 'en')
    trans = load_translations(lang)
    
    # اختبار بعض المفاتيح الشائعة
    test_keys = ['welcome', 'login', 'email', 'password', 'error']
    test_results = {}
    
    for key in test_keys:
        value = trans.get(key, 'المفتاح غير موجود')
        test_results[key] = {
            "exists": key in trans,
            "value": value,
            "has_aaaa": "AAAA" in str(value)
        }
    
    return jsonify({
        "current_language": lang,
        "test_results": test_results
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
