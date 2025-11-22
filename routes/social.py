# -*- coding: utf-8 -*-
from flask import Blueprint, request
from models.social_account import SocialAccount, SocialAccountManager
from routes.auth import get_current_user
from utils.helpers import success_response, error_response

# إنشاء Blueprint للحسابات الاجتماعية
social_bp = Blueprint('social', __name__)

# إدارة الحسابات الاجتماعية
social_manager = SocialAccountManager()

@social_bp.route('/connect', methods=['POST'])
def connect_social_account():
    """ربط حساب اجتماعي جديد"""
    try:
        session_id = request.headers.get('Authorization', '').replace('Bearer ', '')
        user = get_current_user(session_id)
        
        if not user:
            return error_response("غير مصرح بالوصول", 401)
        
        data = request.get_json()
        if not data:
            return error_response("يجب إرسال بيانات JSON")
        
        platform = data.get('platform', '').strip().lower()
        username = data.get('username', '').strip()
        access_token = data.get('access_token', '').strip()
        
        # التحقق من البيانات
        if not all([platform, username, access_token]):
            return error_response("جميع الحقول مطلوبة")
        
        # التحقق من المنصات المدعومة
        supported_platforms = ['twitter', 'facebook', 'instagram', 'linkedin']
        if platform not in supported_platforms:
            return error_response(f"المنصة غير مدعومة. المنصات المدعومة: {', '.join(supported_platforms)}")
        
        # إنشاء حساب اجتماعي جديد
        social_account = SocialAccount(
            platform=platform,
            username=username,
            access_token=access_token,
            user_id=user.user_id
        )
        
        # إضافة الحساب إلى المدير
        social_manager.add_account(social_account)
        
        # إضافة الحساب إلى المستخدم
        user.add_social_account(social_account)
        
        return success_response(
            f"تم ربط حساب {platform} بنجاح!",
            {"account": social_account.to_dict()},
            201
        )
    
    except Exception as e:
        return error_response("حدث خطأ في السيرفر", 500)

@social_bp.route('/accounts', methods=['GET'])
def get_social_accounts():
    """الحصول على جميع الحسابات الاجتماعية للمستخدم"""
    try:
        session_id = request.headers.get('Authorization', '').replace('Bearer ', '')
        user = get_current_user(session_id)
        
        if not user:
            return error_response("غير مصرح بالوصول", 401)
        
        # الحصول على حسابات المستخدم
        accounts = social_manager.get_user_accounts(user.user_id)
        accounts_data = [account.to_dict() for account in accounts]
        
        return success_response(
            "تم تحميل الحسابات الاجتماعية",
            {
                "accounts": accounts_data,
                "total_accounts": len(accounts_data)
            }
        )
    
    except Exception as e:
        return error_response("حدث خطأ في السيرفر", 500)

@social_bp.route('/accounts/<platform>', methods=['GET'])
def get_platform_accounts(platform):
    """الحصول على حسابات منصة محددة"""
    try:
        session_id = request.headers.get('Authorization', '').replace('Bearer ', '')
        user = get_current_user(session_id)
        
        if not user:
            return error_response("غير مصرح بالوصول", 401)
        
        # الحصول على جميع حسابات المستخدم
        all_accounts = social_manager.get_user_accounts(user.user_id)
        
        # تصفية حسب المنصة
        platform_accounts = [acc for acc in all_accounts if acc.platform == platform.lower()]
        accounts_data = [account.to_dict() for account in platform_accounts]
        
        return success_response(
            f"تم تحميل حسابات {platform}",
            {
                "platform": platform,
                "accounts": accounts_data,
                "count": len(accounts_data)
            }
        )
    
    except Exception as e:
        return error_response("حدث خطأ في السيرفر", 500)
