import os
from flask import Flask, jsonify
import json

app = Flask(__name__)

# إعدادات لضمان عرض النص العربي بشكل صحيح
app.config['JSON_AS_ASCII'] = False
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

@app.route('/')
def hello():
    return jsonify({
        "message": "مرحباً! منصة إدارة الوسائط الاجتماعية قيد التطوير!",
        "status": "نشط",
        "version": "1.0.0"
    })

@app.route('/health')
def health():
    return jsonify({"status": "ok"})

@app.route('/test')
def test_arabic():
    return jsonify({
        "test": "اختبار النص العربي",
        "welcome": "أهلاً وسهلاً في المنصة"
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
