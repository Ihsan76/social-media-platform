# -*- coding: utf-8 -*-
from datetime import datetime
import uuid

class SocialAccount:
    """نموذج الحساب الاجتماعي"""
    
    def __init__(self, platform, username, access_token, user_id, account_id=None):
        self.account_id = account_id or str(uuid.uuid4())
        self.platform = platform  # 'twitter', 'facebook', 'instagram', 'linkedin'
        self.username = username
        self.access_token = access_token
        self.user_id = user_id
        self.connected_at = datetime.utcnow()
        self.is_active = True
        self.stats = {
            "followers": 0,
            "posts": 0,
            "engagement": 0.0
        }
    
    def to_dict(self):
        """تحويل الكائن إلى قاموس"""
        return {
            "account_id": self.account_id,
            "platform": self.platform,
            "username": self.username,
            "connected_at": self.connected_at.isoformat(),
            "is_active": self.is_active,
            "stats": self.stats
        }
    
    def update_stats(self, new_stats):
        """تحديث إحصائيات الحساب"""
        self.stats.update(new_stats)

class SocialAccountManager:
    """مدير الحسابات الاجتماعية"""
    
    def __init__(self):
        self.accounts = {}  # account_id -> SocialAccount
        self.user_accounts = {}  # user_id -> list[account_id]
    
    def add_account(self, social_account):
        """إضافة حساب اجتماعي"""
        self.accounts[social_account.account_id] = social_account
        
        # إضافة إلى فهرس المستخدم
        if social_account.user_id not in self.user_accounts:
            self.user_accounts[social_account.user_id] = []
        self.user_accounts[social_account.user_id].append(social_account.account_id)
    
    def get_user_accounts(self, user_id):
        """الحصول على حسابات مستخدم معين"""
        account_ids = self.user_accounts.get(user_id, [])
        return [self.accounts[aid] for aid in account_ids if aid in self.accounts]
    
    def get_account_by_id(self, account_id):
        """الحصول على حساب بواسطة المعرّف"""
        return self.accounts.get(account_id)
