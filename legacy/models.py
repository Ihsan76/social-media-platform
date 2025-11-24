# -*- coding: utf-8 -*-
import json
import os
from datetime import datetime

class TranslationManager:
    def __init__(self):
        self.translations_dir = "translations"
        self.languages_file = os.path.join(self.translations_dir, "languages.json")
        self.ensure_directories()
    
    def ensure_directories(self):
        """إنشاء المجلدات الضرورية"""
        if not os.path.exists(self.translations_dir):
            os.makedirs(self.translations_dir)
    
    def get_all_languages(self):
        """الحصول على جميع اللغات المدعومة"""
        try:
            with open(self.languages_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            # اللغات الافتراضية
            return {
                "ar": {"name": "العربية", "native_name": "العربية", "direction": "rtl", "enabled": True},
                "en": {"name": "English", "native_name": "English", "direction": "ltr", "enabled": True},
                "fr": {"name": "French", "native_name": "Français", "direction": "ltr", "enabled": True}
            }
    
    def save_languages(self, languages):
        """حفظ إعدادات اللغات"""
        with open(self.languages_file, 'w', encoding='utf-8') as f:
            json.dump(languages, f, ensure_ascii=False, indent=2)
    
    def get_translation_keys(self):
        """استخراج جميع مفاتيح الترجمة من الملفات"""
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
        """استخراج المفاتيح بشكل متكرر"""
        for key, value in data.items():
            new_path = f"{current_path}.{key}" if current_path else key
            if isinstance(value, dict):
                self._extract_keys(value, new_path, keys_set)
            else:
                keys_set.add(new_path)
    
    def get_translation_file(self, lang):
        """الحصول على ملف ترجمة لغة معينة"""
        file_path = os.path.join(self.translations_dir, f"{lang}.json")
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {}
    
    def save_translation_file(self, lang, data):
        """حفظ ملف الترجمة"""
        file_path = os.path.join(self.translations_dir, f"{lang}.json")
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def update_translation(self, lang, key, value):
        """تحديث ترجمة محددة"""
        data = self.get_translation_file(lang)
        keys = key.split('.')
        
        # التنقل في الهيكل المتداخل
        current = data
        for k in keys[:-1]:
            if k not in current:
                current[k] = {}
            current = current[k]
        
        # تعيين القيمة
        current[keys[-1]] = value
        self.save_translation_file(lang, data)
    
    def add_new_key(self, key, default_values):
        """إضافة مفتاح جديد لجميع اللغات"""
        for lang in self.get_all_languages():
            if lang not in default_values:
                default_values[lang] = key  # استخدام المفتاح كقيمة افتراضية
            self.update_translation(lang, key, default_values[lang])