'use client'

import { useState, useEffect } from 'react'
import Header from './Header'
import { TranslationsProvider } from '../contexts/TranslationsContext'

interface MainLayoutProps {
  children: React.ReactNode
}

export default function MainLayout({ children }: MainLayoutProps) {
  const [isLoading, setIsLoading] = useState(true)

  useEffect(() => {
    setIsLoading(false)
  }, [])

  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-blue-500"></div>
      </div>
    )
  }

  return (
    <TranslationsProvider>
      <div className="min-h-screen bg-gray-50">
        <Header />
        <main className="pt-16">
          {children}
        </main>
      </div>
    </TranslationsProvider>
  )
}
