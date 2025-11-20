# Gunicorn configuration file
import os

bind = "0.0.0.0:" + os.environ.get("PORT", "5000")
workers = 1
worker_class = "sync"
timeout = 120

# إعدادات للغة العربية
charset = 'utf-8'
