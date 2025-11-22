# -*- coding: utf-8 -*-
from .auth import auth_bp
from .social import social_bp

# جمع جميع الـBlueprints في قائمة واحدة
all_blueprints = [auth_bp, social_bp]
