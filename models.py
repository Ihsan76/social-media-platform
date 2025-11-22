# -*- coding: utf-8 -*-
from datetime import datetime
import json

class User:
    def __init__(self, user_id, username, email, password_hash, created_at=None):
        self.user_id = user_id
        self.username = username
        self.email = email
        self.password_hash = password_hash
        self.created_at = created_at or datetime.utcnow()
        self.social_accounts = []
        self.preferences = {
            "language": "ar",
            "timezone": "Asia/Riyadh"
        }
    
    def to_dict(self):
        return {
            "user_id": self.user_id,
            "username": self.username,
            "email": self.email,
            "created_at": self.created_at.isoformat(),
            "preferences": self.preferences,
            "social_accounts_count": len(self.social_accounts)
        }

class SocialAccount:
    def __init__(self, platform, username, access_token, user_id):
        self.platform = platform  # 'twitter', 'facebook', 'instagram'
        self.username = username
        self.access_token = access_token
        self.user_id = user_id
        self.connected_at = datetime.utcnow()
