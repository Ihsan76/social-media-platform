'use client'

import { useTranslations } from '../contexts/TranslationsContext'
import LanguageSelector from './LanguageSelector'

export default function Header() {
  const { t } = useTranslations()

  return (
    <header className="fixed top-0 left-0 right-0 bg-white shadow-sm z-50 border-b border-gray-200">
      <nav className="container mx-auto px-4 py-3 flex items-center justify-between">
        {/* الشعار */}
        <div className="flex items-center space-x-3 space-x-reverse">
          <div className="w-10 h-10 bg-gradient-to-r from-blue-500 to-purple-500 rounded-lg flex items-center justify-center">
            <i className="fas fa-paper-plane text-white text-lg"></i>
          </div>
          <span className="text-xl font-bold text-gray-800">
            {t('platform_name', 'نشرتي')}
          </span>
        </div>

        {/* روابط التنقل */}
        <div className="hidden md:flex items-center space-x-8 space-x-reverse">
          <a href="/" className="text-gray-700 hover:text-blue-500 transition-colors font-medium">
            {t('home', 'الرئيسية')}
          </a>
          <a href="/login" className="text-gray-700 hover:text-blue-500 transition-colors font-medium">
            {t('login', 'تسجيل الدخول')}
          </a>
          <a href="/dashboard" className="text-gray-700 hover:text-blue-500 transition-colors font-medium">
            {t('dashboard', 'لوحة التحكم')}
          </a>
        </div>

        {/* قسم المستخدم واللغة */}
        <div className="flex items-center space-x-4 space-x-reverse">
          <LanguageSelector />
          <div className="text-sm text-gray-600">
            {t('welcome', 'مرحباً')}
          </div>
        </div>
      </nav>
    </header>
  )
}
