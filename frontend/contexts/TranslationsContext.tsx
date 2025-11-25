'use client'

import React, { createContext, useContext, useState, useEffect } from 'react'
import { translations, languages, getTranslation, LanguageCode, LanguageInfo } from '../lib/locales'

interface TranslationsContextType {
  lang: LanguageCode
  setLang: (lang: LanguageCode) => void
  t: (key: string, fallback?: string) => string
  textDirection: 'rtl' | 'ltr'
  availableLanguages: Record<LanguageCode, LanguageInfo>
}

const TranslationsContext = createContext<TranslationsContextType | undefined>(undefined)

export function TranslationsProvider({ children }: { children: React.ReactNode }) {
  const [lang, setLang] = useState<LanguageCode>('ar')

  const textDirection = languages[lang].direction

  const t = (key: string, fallback: string = key): string => {
    return getTranslation(key, lang, fallback)
  }

  useEffect(() => {
    // تحميل تفضيل اللغة المحفوظ
    const savedLang = localStorage.getItem('preferred_language') as LanguageCode
    if (savedLang && languages[savedLang]) {
      setLang(savedLang)
    }
  }, [])

  useEffect(() => {
    // تحديث إعدادات الصفحة عند تغيير اللغة
    document.documentElement.dir = textDirection
    document.documentElement.lang = lang
    
    // حفظ التفضيل
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
