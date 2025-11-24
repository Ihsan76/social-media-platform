FROM python:3.11-slim

WORKDIR /app

# نسخ المتطلبات أولاً
COPY backend/requirements.txt .

# تثبيت المتطلبات
RUN pip install --no-cache-dir -r requirements.txt

# نسخ كود التطبيق
COPY backend/ .

# التعريض - استخدام PORT الذي يوفره Railway
EXPOSE 8080

# استخدام PORT من متغير البيئة
CMD ["python", "app.py"]
