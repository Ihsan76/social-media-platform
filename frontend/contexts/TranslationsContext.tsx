'use client'

import React, { createContext, useContext, useState, useEffect } from 'react'

// تعريف الأنواع محلياً
type LanguageCode = 'ar' | 'en' | 'fr'

interface LanguageInfo {
  code: LanguageCode
  name: string
  nativeName: string
  flag: string
  direction: 'rtl' | 'ltr'
}

// ترجمات مبسطة مباشرة في الملف
const translations = {
  ar: {
    platform_name: 'نشرتي',
    home: 'الرئيسية',
    login: 'تسجيل الدخول',
    dashboard: 'لوحة التحكم',
    welcome: 'مرحباً',
    current_language: 'اللغة الحالية',
    social_media_platform: 'منصة وسائل التواصل الاجتماعي',
    version: 'الإصدار',
    register: 'تسجيل جديد',
    profile: 'الملف الشخصي',
    social_accounts: 'الحسابات الاجتماعية',
    manage_accounts: 'إدارة الحسابات',
    connect_new_account: 'ربط حساب جديد',
    platform: 'المنصة',
    choose_platform: 'اختر المنصة',
    twitter: 'تويتر',
    facebook: 'فيسبوك',
    instagram: 'إنستغرام',
    linkedin: 'لينكدإن',
    social_username: 'اسم المستخدم على المنصة',
    enter_username: 'أدخل اسم المستخدم',
    access_token: 'رمز الوصول',
    enter_access_token: 'أدخل رمز الوصول',
    connect_account: 'ربط الحساب',
    connected_accounts: 'الحسابات المرتبطة',
    refresh_list: 'تحديث القائمة',
    no_accounts: 'لا توجد حسابات مرتبطة بعد',
    landing: {
      hero: {
        title: 'منصة الناشرين المحترفين',
        subtitle: 'واجهتك الذكية للتواصل مع جمهورك بطريقة أكثر فعالية وأناقة',
        start_journey: 'ابدأ رحلتك الآن',
        watch_demo: 'شاهد العرض التوضيحي'
      },
      stats: {
        publishers: 'ناشر',
        posts: 'منشور',
        engagement: 'تفاعل'
      }
    }
  },
  en: {
    platform_name: 'Nashrati',
    home: 'Home',
    login: 'Login',
    dashboard: 'Dashboard',
    welcome: 'Welcome',
    current_language: 'Current Language',
    social_media_platform: 'Social Media Platform',
    version: 'Version',
    register: 'Register',
    profile: 'Profile',
    social_accounts: 'Social Accounts',
    manage_accounts: 'Manage Accounts',
    connect_new_account: 'Connect New Account',
    platform: 'Platform',
    choose_platform: 'Choose Platform',
    twitter: 'Twitter',
    facebook: 'Facebook',
    instagram: 'Instagram',
    linkedin: 'LinkedIn',
    social_username: 'Username on platform',
    enter_username: 'Enter username',
    access_token: 'Access Token',
    enter_access_token: 'Enter access token',
    connect_account: 'Connect Account',
    connected_accounts: 'Connected Accounts',
    refresh_list: 'Refresh List',
    no_accounts: 'No accounts connected yet',
    landing: {
      hero: {
        title: 'Professional Publishers Platform',
        subtitle: 'Your smart interface to communicate with your audience more effectively and elegantly',
        start_journey: 'Start Your Journey Now',
        watch_demo: 'Watch Demo'
      },
      stats: {
        publishers: 'Publishers',
        posts: 'Posts',
        engagement: 'Engagement'
      }
    }
  },
  fr: {
    platform_name: 'Nashrati',
    home: 'Accueil',
    login: 'Connexion',
    dashboard: 'Tableau de bord',
    welcome: 'Bienvenue',
    current_language: 'Langue actuelle',
    social_media_platform: 'Plateforme de médias sociaux',
    version: 'Version',
    register: 'S\'inscrire',
    profile: 'Profil',
    social_accounts: 'Comptes sociaux',
    manage_accounts: 'Gérer les comptes',
    connect_new_account: 'Connecter un nouveau compte',
    platform: 'Plateforme',
    choose_platform: 'Choisir la plateforme',
    twitter: 'Twitter',
    facebook: 'Facebook',
    instagram: 'Instagram',
    linkedin: 'LinkedIn',
    social_username: 'Nom d\'utilisateur sur la plateforme',
    enter_username: 'Entrer le nom d\'utilisateur',
    access_token: 'Jeton d\'accès',
    enter_access_token: 'Entrer le jeton d\'accès',
    connect_account: 'Connecter le compte',
    connected_accounts: 'Comptes connectés',
    refresh_list: 'Actualiser la liste',
    no_accounts: 'Aucun compte connecté pour le moment',
    landing: {
      hero: {
        title: 'Plateforme des éditeurs professionnels',
        subtitle: 'Votre interface intelligente pour communiquer avec votre public de manière plus efficace et élégante',
        start_journey: 'Commencez votre voyage maintenant',
        watch_demo: 'Regarder la démo'
      },
      stats: {
        publishers: 'Éditeurs',
        posts: 'Publications',
        engagement: 'Engagement'
      }
    }
  }
}

const languages: Record<LanguageCode, LanguageInfo> = {
  ar: { code: 'ar', name: 'Arabic', nativeName: 'العربية', flag: '🇸🇦', direction: 'rtl' },
  en: { code: 'en', name: 'English', nativeName: 'English', flag: '🇺🇸', direction: 'ltr' },
  fr: { code: 'fr', name: 'French', nativeName: 'Français', flag: '🇫🇷', direction: 'ltr' }
}

interface TranslationsContextType {
  lang: LanguageCode
  setLang: (lang: LanguageCode) => void
  t: (key: string, fallback?: string) => string
  textDirection: 'rtl' | 'ltr'
  availableLanguages: typeof languages
}

const TranslationsContext = createContext<TranslationsContextType | undefined>(undefined)

export function TranslationsProvider({ children }: { children: React.ReactNode }) {
  const [lang, setLang] = useState<LanguageCode>('ar')

  const textDirection = languages[lang].direction

  const t = (key: string, fallback: string = key): string => {
    try {
      const keys = key.split('.')
      let value: any = translations[lang]
      
      for (const k of keys) {
        value = value?.[k]
        if (value === undefined) break
      }
      
      return value !== undefined ? value : fallback
    } catch {
      return fallback
    }
  }

  useEffect(() => {
    document.documentElement.dir = textDirection
    document.documentElement.lang = lang
    localStorage.setItem('preferred_language', lang)
  }, [lang, textDirection])

  return (
    <TranslationsContext.Provider value={{
      lang,
      setLang,
      t,
      textDirection,
      availableLanguages: languages
    }}>
      {children}
    </TranslationsContext.Provider>
  )
}

export function useTranslations() {
  const context = useContext(TranslationsContext)
  if (context === undefined) {
    throw new Error('useTranslations must be used within a TranslationsProvider')
  }
  return context
}
