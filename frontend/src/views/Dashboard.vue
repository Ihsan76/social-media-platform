<template>
  <div class="dashboard">
    <h1>مرحباً بك في نظام إدارة وسائل التواصل الاجتماعي</h1>
    
    <div class="connection-status">
      <div class="status-card" :class="apiStatus">
        <h3>حالة الخادم</h3>
        <p>{{ apiMessage }}</p>
        <span class="status-indicator"></span>
      </div>
    </div>

    <div class="stats">
      <div class="stat-card">
        <h3>الحسابات المتصلة</h3>
        <p class="number">{{ accountsCount }}</p>
        <button class="connect-btn" @click="connectAccount">+ إضافة حساب</button>
      </div>
      <div class="stat-card">
        <h3>المنشورات المجدولة</h3>
        <p class="number">{{ scheduledPostsCount }}</p>
        <button class="schedule-btn" @click="createPost">📅 جدولة منشور</button>
      </div>
      <div class="stat-card">
        <h3>حالة قاعدة البيانات</h3>
        <p class="number">{{ databaseStatus }}</p>
        <button class="analytics-btn" @click="refreshData">🔄 تحديث</button>
      </div>
    </div>

    <div class="quick-actions">
      <h2>الإجراءات السريعة</h2>
      <div class="actions-grid">
        <button class="action-btn" @click="connectAccount">
          <span class="icon">🔗</span>
          <span>ربط حساب جديد</span>
        </button>
        <button class="action-btn" @click="createPost">
          <span class="icon">✏️</span>
          <span>إنشاء منشور</span>
        </button>
        <button class="action-btn" @click="viewAnalytics">
          <span class="icon">📈</span>
          <span>عرض الإحصائيات</span>
        </button>
        <button class="action-btn" @click="scheduleContent">
          <span class="icon">⏰</span>
          <span>جدولة محتوى</span>
        </button>
      </div>
    </div>

    <!-- قسم الحسابات المتصلة -->
    <div class="connected-accounts" v-if="accounts.length > 0">
      <h2>الحسابات المتصلة</h2>
      <div class="accounts-grid">
        <div v-for="account in accounts" :key="account.id" class="account-card">
          <div class="platform-icon">{{ getPlatformIcon(account.platform) }}</div>
          <div class="account-info">
            <h4>{{ account.account_name }}</h4>
            <p>{{ account.platform }}</p>
          </div>
          <div class="account-status" :class="{ active: account.is_active }">
            {{ account.is_active ? 'نشط' : 'غير نشط' }}
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { apiService } from '../services/api'
import authService from '../services/auth'

export default {
  name: 'Dashboard',
  data() {
    return {
      apiStatus: 'checking',
      apiMessage: 'جاري التحقق من حالة الخادم...',
      accountsCount: 0,
      scheduledPostsCount: 0,
      databaseStatus: 'جاري التحقق...',
      accounts: []
    }
  },
  async mounted() {
    await this.initializeApp()
  },
  methods: {
    async initializeApp() {
      try {
        // تسجيل الدخول أولاً
        if (!authService.isAuthenticated()) {
          await authService.login()
        }

        // جلب بيانات النظام
        await this.checkAPIStatus()
        await this.loadAccounts()
        await this.loadScheduledPosts()
        
      } catch (error) {
        console.error('خطأ في تهيئة التطبيق:', error)
        this.apiStatus = 'error'
        this.apiMessage = '🔴 تعذر الاتصال بالخادم'
      }
    },

    async checkAPIStatus() {
      try {
        const health = await apiService.healthCheck()
        this.apiStatus = 'connected'
        this.apiMessage = `🟢 ${health.message} - قاعدة البيانات: ${health.database}`
        this.databaseStatus = health.database === 'connected' ? '🟢 متصل' : '🔴 غير متصل'
      } catch (error) {
        this.apiStatus = 'error'
        this.apiMessage = '🔴 تعذر الاتصال بالخادم'
        this.databaseStatus = '🔴 غير معروف'
      }
    },

    async loadAccounts() {
      try {
        const data = await apiService.getAccounts()
        this.accounts = data.accounts
        this.accountsCount = data.total
      } catch (error) {
        console.error('خطأ في جلب الحسابات:', error)
      }
    },

    async loadScheduledPosts() {
      try {
        const data = await apiService.getScheduledPosts()
        this.scheduledPostsCount = data.scheduled_posts.length
      } catch (error) {
        console.error('خطأ في جلب المنشورات المجدولة:', error)
      }
    },

    async refreshData() {
      await this.checkAPIStatus()
      await this.loadAccounts()
      await this.loadScheduledPosts()
    },

    getPlatformIcon(platform) {
      const icons = {
        twitter: '🐦',
        facebook: '📘',
        instagram: '📷',
        linkedin: '💼',
        tiktok: '🎵'
      }
      return icons[platform] || '🔗'
    },

    connectAccount() {
      alert('سيتم فتح نافذة ربط الحسابات قريباً...')
    },

    createPost() {
      alert('سيتم فتح محرر المنشورات قريباً...')
    },

    viewAnalytics() {
      alert('سيتم فتح لوحة التحليلات قريباً...')
    },

    scheduleContent() {
      alert('سيتم فتح جدولة المحتوى قريباً...')
    }
  }
}
</script>

<style scoped>
/* إضافة أنماط للحسابات المتصلة */
.connected-accounts {
  margin-top: 3rem;
  background: white;
  padding: 2rem;
  border-radius: 15px;
  box-shadow: 0 4px 15px rgba(0,0,0,0.1);
}

.accounts-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 1rem;
  margin-top: 1rem;
}

.account-card {
  display: flex;
  align-items: center;
  padding: 1rem;
  background: #f8f9fa;
  border-radius: 10px;
  border-left: 4px solid #667eea;
}

.platform-icon {
  font-size: 2rem;
  margin-right: 1rem;
}

.account-info {
  flex: 1;
}

.account-info h4 {
  margin: 0;
  color: #333;
}

.account-info p {
  margin: 0;
  color: #666;
  text-transform: capitalize;
}

.account-status {
  padding: 0.25rem 0.75rem;
  border-radius: 15px;
  font-size: 0.8rem;
  font-weight: bold;
}

.account-status.active {
  background: #4CAF50;
  color: white;
}

.account-status:not(.active) {
  background: #ff9800;
  color: white;
}
</style>
