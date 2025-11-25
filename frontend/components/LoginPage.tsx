'use client'

import { useState } from 'react'
import { useTranslations } from '../contexts/TranslationsContext'

export default function LoginPage() {
  const { t } = useTranslations()
  const [activeTab, setActiveTab] = useState('register')

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-purple-50 py-8">
      <div className="container mx-auto px-4 max-w-4xl">
        
        {/* شريط اللغة أعلى الصفحة */}
        <div className="flex justify-end mb-6">
          <div className="bg-white rounded-lg shadow-sm p-4">
            <div className="flex items-center space-x-2 space-x-reverse">
              <span className="text-sm text-gray-600">{t('current_language', 'اللغة الحالية')}:</span>
              <span className="font-medium">🇸🇦 العربية</span>
            </div>
          </div>
        </div>

        {/* العنوان الرئيسي */}
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-gray-800 mb-4">
            🚀 {t('social_media_platform', 'منصة وسائل التواصل الاجتماعي')}
          </h1>
          <p className="text-xl text-gray-600">
            {t('login_with_email_social', 'سجل الدخول باستخدام بريدك الإلكتروني أو حساباتك الاجتماعية')}
          </p>
        </div>

        {/* نظام التبويب */}
        <div className="bg-white rounded-2xl shadow-xl overflow-hidden">
          {/* أزرار التبويب */}
          <div className="flex border-b border-gray-200">
            <button
              onClick={() => setActiveTab('register')}
              className={`flex-1 py-4 px-6 text-center font-medium transition-colors ${
                activeTab === 'register'
                  ? 'bg-blue-50 text-blue-600 border-b-2 border-blue-500'
                  : 'text-gray-600 hover:text-gray-800'
              }`}
            >
              {t('register', 'تسجيل جديد')}
            </button>
            <button
              onClick={() => setActiveTab('login')}
              className={`flex-1 py-4 px-6 text-center font-medium transition-colors ${
                activeTab === 'login'
                  ? 'bg-blue-50 text-blue-600 border-b-2 border-blue-500'
                  : 'text-gray-600 hover:text-gray-800'
              }`}
            >
              {t('login', 'تسجيل الدخول')}
            </button>
            <button
              onClick={() => setActiveTab('profile')}
              className={`flex-1 py-4 px-6 text-center font-medium transition-colors ${
                activeTab === 'profile'
                  ? 'bg-blue-50 text-blue-600 border-b-2 border-blue-500'
                  : 'text-gray-600 hover:text-gray-800'
              }`}
            >
              {t('profile', 'الملف الشخصي')}
            </button>
            <button
              onClick={() => setActiveTab('social')}
              className={`flex-1 py-4 px-6 text-center font-medium transition-colors ${
                activeTab === 'social'
                  ? 'bg-blue-50 text-blue-600 border-b-2 border-blue-500'
                  : 'text-gray-600 hover:text-gray-800'
              }`}
            >
              {t('social_accounts', 'الحسابات الاجتماعية')}
            </button>
          </div>

          {/* محتوى التبويب - التسجيل */}
          {activeTab === 'register' && (
            <div className="p-8">
              <h2 className="text-2xl font-bold text-gray-800 mb-6">{t('register', 'تسجيل جديد')}</h2>
              
              {/* التسجيل بالبريد الإلكتروني */}
              <div className="mb-8">
                <h3 className="text-lg font-semibold text-gray-700 mb-4">📧 {t('register_with_email', 'التسجيل بالبريد الإلكتروني')}</h3>
                <div className="space-y-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      {t('username', 'اسم المستخدم')}
                    </label>
                    <input
                      type="text"
                      placeholder={t('enter_username', 'أدخل اسم المستخدم')}
                      className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-colors"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      {t('email', 'البريد الإلكتروني')}
                    </label>
                    <input
                      type="email"
                      placeholder={t('enter_email', 'أدخل بريدك الإلكتروني')}
                      className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-colors"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      {t('password', 'كلمة المرور')}
                    </label>
                    <input
                      type="password"
                      placeholder={`${t('enter_password', 'أدخل كلمة المرور')} (6 ${t('characters_min', 'أحرف على الأقل')})`}
                      className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-colors"
                    />
                  </div>
                  <button className="w-full bg-blue-500 text-white py-3 px-6 rounded-lg font-semibold hover:bg-blue-600 transition-colors">
                    {t('register', 'تسجيل جديد')}
                  </button>
                </div>
              </div>

              {/* التسجيل بالحسابات الاجتماعية */}
              <div>
                <div className="relative mb-6">
                  <div className="absolute inset-0 flex items-center">
                    <div className="w-full border-t border-gray-300"></div>
                  </div>
                  <div className="relative flex justify-center text-sm">
                    <span className="px-2 bg-white text-gray-500">{t('or', 'أو')}</span>
                  </div>
                </div>

                <h3 className="text-lg font-semibold text-gray-700 mb-4">🔗 {t('register_with_social', 'التسجيل بالحسابات الاجتماعية')}</h3>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <button className="flex items-center justify-center space-x-2 space-x-reverse p-4 border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors">
                    <span className="text-xl">🔍</span>
                    <span>{t('register_google', 'التسجيل بجوجل')}</span>
                  </button>
                  <button className="flex items-center justify-center space-x-2 space-x-reverse p-4 border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors">
                    <span className="text-xl">🐦</span>
                    <span>{t('register_twitter', 'التسجيل بتويتر')}</span>
                  </button>
                  <button className="flex items-center justify-center space-x-2 space-x-reverse p-4 border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors">
                    <span className="text-xl">📘</span>
                    <span>{t('register_facebook', 'التسجيل بفيسبوك')}</span>
                  </button>
                  <button className="flex items-center justify-center space-x-2 space-x-reverse p-4 border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors">
                    <span className="text-xl">📷</span>
                    <span>{t('register_instagram', 'التسجيل بانستغرام')}</span>
                  </button>
                </div>
              </div>
            </div>
          )}

          {/* محتوى التبويب - تسجيل الدخول */}
          {activeTab === 'login' && (
            <div className="p-8">
              <h2 className="text-2xl font-bold text-gray-800 mb-6">{t('login', 'تسجيل الدخول')}</h2>
              {/* سيتم إضافة محتوى تسجيل الدخول هنا */}
              <p className="text-gray-600 text-center py-8">محتوى تسجيل الدخول قيد التطوير...</p>
            </div>
          )}

          {/* محتوى التبويب - الملف الشخصي */}
          {activeTab === 'profile' && (
            <div className="p-8">
              <h2 className="text-2xl font-bold text-gray-800 mb-6">{t('profile', 'الملف الشخصي')}</h2>
              {/* سيتم إضافة محتوى الملف الشخصي هنا */}
              <p className="text-gray-600 text-center py-8">محتوى الملف الشخصي قيد التطوير...</p>
            </div>
          )}

          {/* محتوى التبويب - الحسابات الاجتماعية */}
          {activeTab === 'social' && (
            <div className="p-8">
              <h2 className="text-2xl font-bold text-gray-800 mb-6">{t('manage_accounts', 'إدارة الحسابات')}</h2>
              {/* سيتم إضافة محتوى الحسابات الاجتماعية هنا */}
              <p className="text-gray-600 text-center py-8">محتوى إدارة الحسابات قيد التطوير...</p>
            </div>
          )}
        </div>

        {/* الفوتر */}
        <div className="text-center mt-8">
          <p className="text-gray-600">
            {t('version', 'الإصدار')} 2.2 - {t('multi_language_system', 'نظام متعدد اللغات')}
          </p>
        </div>
      </div>
    </div>
  )
}
