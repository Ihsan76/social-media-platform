# -*- coding: utf-8 -*-
import os
from flask import Flask, jsonify

app = Flask(__name__)

# إعدادات للغة العربية
app.config['JSON_AS_ASCII'] = False

@app.route('/')
def home():
    return jsonify({
        "message": "مرحباً! منصة إدارة الوسائط الاجتماعية تعمل بنجاح! 🚀",
        "status": "نشط",
        "version": "1.0.0",
        "endpoints": {
            "health": "/health",
            "test": "/test"
        }
    })

@app.route('/health')
def health():
    return jsonify({"status": "صحي", "message": "الخدمة تعمل بشكل طبيعي"})

@app.route('/test')
def test():
    return jsonify({
        "arabic_test": "اختبار النص العربي ✅",
        "welcome": "أهلاً وسهلاً في منصتنا"
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
