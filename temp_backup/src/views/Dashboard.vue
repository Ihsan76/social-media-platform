<template>
  <div class="dashboard container">
    <h1>مرحباً بك في نظام إدارة وسائل التواصل الاجتماعي</h1>
    
    <div class="connection-status">
      <div class="card">
        <h3>حالة الخادم</h3>
        <p>{{ apiMessage }}</p>
      </div>
    </div>

    <div class="quick-actions">
      <h2>الإجراءات السريعة</h2>
      <div class="actions-grid">
        <router-link to="/accounts" class="action-btn">
          <span class="icon">🔗</span>
          <span>إدارة الحسابات</span>
        </router-link>
        <button class="action-btn" @click="createPost">
          <span class="icon">✏️</span>
          <span>إنشاء منشور</span>
        </button>
        <button class="action-btn" @click="viewAnalytics">
          <span class="icon">📈</span>
          <span>عرض الإحصائيات</span>
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import { apiService } from '../services/api'

export default {
  name: 'Dashboard',
  data() {
    return {
      apiMessage: 'جاري التحقق من حالة الخادم...'
    }
  },
  async mounted() {
    await this.checkAPIStatus()
  },
  methods: {
    async checkAPIStatus() {
      try {
        const health = await apiService.healthCheck()
        this.apiMessage = `🟢 ${health.message} - قاعدة البيانات: ${health.database}`
      } catch (error) {
        this.apiMessage = '🔴 تعذر الاتصال بالخادم'
      }
    },
    createPost() {
      alert('سيتم فتح محرر المنشورات قريباً...')
    },
    viewAnalytics() {
      alert('سيتم فتح لوحة التحليلات قريباً...')
    }
  }
}
</script>

<style scoped>
.dashboard {
  padding: 2rem;
  max-width: 1200px;
  margin: 0 auto;
}

.connection-status {
  margin: 2rem 0;
}

.quick-actions {
  margin-top: 3rem;
}

.actions-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
  margin-top: 1rem;
}

.action-btn {
  background: white;
  border: 2px solid #667eea;
  color: #667eea;
  padding: 1.5rem;
  border-radius: 10px;
  cursor: pointer;
  font-size: 1rem;
  font-weight: bold;
  transition: all 0.3s ease;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.5rem;
  text-decoration: none;
}

.action-btn:hover {
  background: #667eea;
  color: white;
  transform: translateY(-3px);
}
</style>
