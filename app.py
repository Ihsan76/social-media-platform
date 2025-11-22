# -*- coding: utf-8 -*-
import os
from flask import Flask, jsonify, Response
import json

app = Flask(__name__)

# حل جذري للعربية - استخدام Response مباشرة
@app.route('/')
def home():
    data = {
        "message": "مرحباً! منصة إدارة الوسائط الاجتماعية تعمل بنجاح! 🚀",
        "status": "نشط",
        "version": "1.0.0",
        "endpoints": {
            "health": "/health",
            "test": "/test"
        }
    }
    response = Response(
        json.dumps(data, ensure_ascii=False, indent=2),
        mimetype='application/json; charset=utf-8'
    )
    return response

@app.route('/health')
def health():
    data = {"status": "صحي", "message": "الخدمة تعمل بشكل طبيعي"}
    return Response(
        json.dumps(data, ensure_ascii=False, indent=2),
        mimetype='application/json; charset=utf-8'
    )

@app.route('/test')
def test():
    data = {
        "arabic_test": "اختبار النص العربي ✅",
        "welcome": "أهلاً وسهلاً في منصتنا",
        "features": "ميزات المنصة قيد التطوير"
    }
    return Response(
        json.dumps(data, ensure_ascii=False, indent=2),
        mimetype='application/json; charset=utf-8'
    )

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
