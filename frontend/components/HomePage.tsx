'use client'

import { useTranslations } from '../contexts/TranslationsContext'

export default function HomePage() {
  const { t } = useTranslations()

  return (
    <div className="min-h-screen">
      {/* القسم البطولي */}
      <section className="hero-section bg-gradient-to-br from-blue-600 via-blue-500 to-purple-500 text-white pt-20 pb-32">
        <div className="container mx-auto px-4">
          <div className="max-w-4xl mx-auto text-center">
            <h1 className="text-5xl md:text-6xl font-bold mb-6 leading-tight">
              {t('landing.hero.title', 'منصة الناشرين المحترفين')}
            </h1>
            <p className="text-xl md:text-2xl mb-8 opacity-90 leading-relaxed">
              {t('landing.hero.subtitle', 'واجهتك الذكية للتواصل مع جمهورك بطريقة أكثر فعالية وأناقة')}
            </p>

            {/* الإحصائيات */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mb-12 max-w-2xl mx-auto">
              <div className="text-center">
                <div className="text-3xl font-bold">+500</div>
                <div className="opacity-80">{t('landing.stats.publishers', 'ناشر')}</div>
              </div>
              <div className="text-center">
                <div className="text-3xl font-bold">+50K</div>
                <div className="opacity-80">{t('landing.stats.posts', 'منشور')}</div>
              </div>
              <div className="text-center">
                <div className="text-3xl font-bold">+1M</div>
                <div className="opacity-80">{t('landing.stats.engagement', 'تفاعل')}</div>
              </div>
            </div>

            {/* أزرار التحويل */}
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <a
                href="/login"
                className="bg-white text-blue-600 px-8 py-4 rounded-lg font-semibold text-lg hover:bg-gray-100 transition-colors flex items-center justify-center space-x-2 space-x-reverse"
              >
                <i className="fas fa-play-circle"></i>
                <span>{t('landing.hero.start_journey', 'ابدأ رحلتك الآن')}</span>
              </a>
              <button className="border-2 border-white text-white px-8 py-4 rounded-lg font-semibold text-lg hover:bg-white hover:text-blue-600 transition-colors flex items-center justify-center space-x-2 space-x-reverse">
                <i className="fas fa-info-circle"></i>
                <span>{t('landing.hero.watch_demo', 'شاهد العرض التوضيحي')}</span>
              </button>
            </div>
          </div>
        </div>
      </section>

      {/* قسم المميزات */}
      <section className="py-20 bg-white">
        <div className="container mx-auto px-4">
          <div className="text-center mb-16">
            <h2 className="text-4xl font-bold text-gray-800 mb-4">
              {t('landing.features.title', 'كل ما يحتاجه الناشر المحترف')}
            </h2>
            <p className="text-xl text-gray-600 max-w-2xl mx-auto">
              {t('landing.features.subtitle', 'أدوات متكاملة صممت خصيصاً لتلبية احتياجات الناشرين ورواد المحتوى')}
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {/* مميزة 1 */}
            <div className="bg-gray-50 rounded-xl p-8 text-center hover:shadow-lg transition-shadow">
              <div className="w-16 h-16 bg-blue-100 rounded-full flex items-center justify-center mx-auto mb-6">
                <i className="fas fa-chart-line text-blue-500 text-2xl"></i>
              </div>
              <h3 className="text-xl font-bold text-gray-800 mb-4">
                {t('landing.features.analytics.title', 'تحليلات متقدمة')}
              </h3>
              <p className="text-gray-600">
                {t('landing.features.analytics.desc', 'فهم جمهورك بشكل أعمق مع إحصائيات مفصلة وتحليلات ذكية')}
              </p>
            </div>

            {/* مميزة 2 */}
            <div className="bg-gray-50 rounded-xl p-8 text-center hover:shadow-lg transition-shadow">
              <div className="w-16 h-16 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-6">
                <i className="fas fa-bullseye text-green-500 text-2xl"></i>
              </div>
              <h3 className="text-xl font-bold text-gray-800 mb-4">
                {t('landing.features.targeting.title', 'استهداف دقيق')}
              </h3>
              <p className="text-gray-600">
                {t('landing.features.targeting.desc', 'وصل محتواك للجمهور المناسب في الوقت المناسب')}
              </p>
            </div>

            {/* مميزة 3 */}
            <div className="bg-gray-50 rounded-xl p-8 text-center hover:shadow-lg transition-shadow">
              <div className="w-16 h-16 bg-purple-100 rounded-full flex items-center justify-center mx-auto mb-6">
                <i className="fas fa-comments text-purple-500 text-2xl"></i>
              </div>
              <h3 className="text-xl font-bold text-gray-800 mb-4">
                {t('landing.features.engagement.title', 'تفاعل حقيقي')}
              </h3>
              <p className="text-gray-600">
                {t('landing.features.engagement.desc', 'حوّل متابعيك إلى مجتمع متفاعل مع أدوات حوار وتفاعل')}
              </p>
            </div>
          </div>
        </div>
      </section>
    </div>
  )
}
