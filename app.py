# -*- coding: utf-8 -*-
import os
from flask import Flask, jsonify, Response
import json

app = Flask(__name__)

# إعدادات شاملة للغة العربية
app.config['JSON_AS_ASCII'] = False
app.config['JSONIFY_MIMETYPE'] = 'application/json; charset=utf-8'
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

@app.route('/')
def hello():
    response_data = {
        "message": "مرحباً! منصة إدارة الوسائط الاجتماعية قيد التطوير!",
        "status": "نشط", 
        "version": "1.0.0"
    }
    
    response = jsonify(response_data)
    response.headers['Content-Type'] = 'application/json; charset=utf-8'
    return response

@app.route('/health')
def health():
    return jsonify({"status": "ok", "message": "الخدمة تعمل بشكل طبيعي"})

@app.route('/test')
def test_arabic():
    return jsonify({
        "test": "اختبار النص العربي",
        "welcome": "أهلاً وسهلاً في المنصة",
        "features": "ميزات المنصة قيد التطوير"
    })

# حل بدائي مضمون
@app.route('/simple')
def simple_arabic():
    arabic_text = '''
    {
        "message": "مرحباً! منصة إدارة الوسائط الاجتماعية قيد التطوير!",
        "status": "نشط"
    }
    '''
    return Response(arabic_text, mimetype='application/json; charset=utf-8')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
