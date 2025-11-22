@app.route('/')
def home():
    """الصفحة الرئيسية مع دعم اللغات"""
    lang = request.args.get('lang', 'en')
    if lang not in SUPPORTED_LANGUAGES:
        lang = 'en'
    
    # 🔥 استخدم الدالة الجديدة من translations
    from translations import get_language_direction
    text_direction = get_language_direction(lang)
    
    return render_template('index.html', 
        lang=lang,
        text_direction=text_direction,  # 🔥 أضف هذا
        languages=SUPPORTED_LANGUAGES,
        translations=TRANSLATIONS.get(lang, {}))
