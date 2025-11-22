import json
import os

print("⚡ إصلاح سريع لملفات الترجمة...")

for lang in ['ar', 'en', 'fr']:
    file_path = f'translations/{lang}.json'
    
    if os.path.exists(file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # ببساطة نأخذ الجزء حتى آخر قوس }
            last_brace = content.rfind('}')
            if last_brace != -1:
                clean_content = content[:last_brace + 1]
                
                # التحقق
                data = json.loads(clean_content)
                
                # الحفظ
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(clean_content)
                
                print(f"✅ {lang}: تم الإصلاح - {len(data)} مفتاح")
            else:
                print(f"❌ {lang}: لم يتم العثور على قوس ختامي")
                
        except Exception as e:
            print(f"❌ {lang}: فشل الإصلاح - {e}")
