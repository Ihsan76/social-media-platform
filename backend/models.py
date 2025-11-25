from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # العلاقات
    social_accounts = db.relationship('SocialAccount', backref='user', lazy=True)
    scheduled_posts = db.relationship('ScheduledPost', backref='user', lazy=True)

class SocialAccount(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    platform = db.Column(db.String(50), nullable=False)  # twitter, facebook, etc.
    account_name = db.Column(db.String(100), nullable=False)
    access_token = db.Column(db.Text, nullable=False)
    refresh_token = db.Column(db.Text)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class ScheduledPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    platforms = db.Column(db.Text)  # تخزين منصات النشر كـ JSON
    scheduled_time = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(20), default='scheduled')  # scheduled, posted, failed
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class PostAnalytics(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    scheduled_post_id = db.Column(db.Integer, db.ForeignKey('scheduled_post.id'))
    platform = db.Column(db.String(50))
    post_id = db.Column(db.String(100))  # المعرف من المنصة الاجتماعية
    likes = db.Column(db.Integer, default=0)
    shares = db.Column(db.Integer, default=0)
    comments = db.Column(db.Integer, default=0)
    impressions = db.Column(db.Integer, default=0)
    collected_at = db.Column(db.DateTime, default=datetime.utcnow)
