'use client'

import { useState, useRef, useEffect } from 'react'
import { useTranslations } from '../contexts/TranslationsContext'
import { LanguageCode } from '../lib/locales/types'

export default function LanguageSelector() {
  const { lang, setLang, t, availableLanguages } = useTranslations()
  const [isOpen, setIsOpen] = useState(false)
  const dropdownRef = useRef<HTMLDivElement>(null)

  const currentLanguage = availableLanguages[lang]

  const handleLanguageChange = (newLang: LanguageCode) => {
    setLang(newLang)
    setIsOpen(false)
  }

  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target as Node)) {
        setIsOpen(false)
      }
    }

    document.addEventListener('mousedown', handleClickOutside)
    return () => document.removeEventListener('mousedown', handleClickOutside)
  }, [])

  return (
    <div className="relative" ref={dropdownRef}>
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="flex items-center space-x-2 space-x-reverse px-3 py-2 rounded-lg border border-gray-300 hover:border-gray-400 transition-colors bg-white"
      >
        <span>{currentLanguage.flag}</span>
        <span className="text-sm font-medium">{currentLanguage.nativeName}</span>
        <i className={`fas fa-chevron-${isOpen ? 'up' : 'down'} text-xs text-gray-500`}></i>
      </button>

      {isOpen && (
        <div className="absolute top-full left-0 mt-2 w-48 bg-white rounded-lg shadow-lg border border-gray-200 py-2 z-50">
          {Object.values(availableLanguages).map((language) => (
            <button
              key={language.code}
              onClick={() => handleLanguageChange(language.code)}
              className={`w-full text-right px-4 py-2 hover:bg-gray-50 transition-colors flex items-center space-x-2 space-x-reverse ${
                lang === language.code ? 'bg-primary-50 text-primary-600' : 'text-gray-700'
              }`}
            >
              <span className="text-lg">{language.flag}</span>
              <span className="flex-1">{language.nativeName}</span>
              {lang === language.code && (
                <i className="fas fa-check text-primary-500 text-sm"></i>
              )}
            </button>
          ))}
        </div>
      )}
    </div>
  )
}
