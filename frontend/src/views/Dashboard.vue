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
        <p class="number">0</p>
        <button class="connect-btn">+ إضافة حساب</button>
      </div>
      <div class="stat-card">
        <h3>المنشورات المجدولة</h3>
        <p class="number">0</p>
        <button class="schedule-btn">📅 جدولة منشور</button>
      </div>
      <div class="stat-card">
        <h3>التفاعلات</h3>
        <p class="number">0</p>
        <button class="analytics-btn">📊 عرض التحليلات</button>
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
  </div>
</template>

<script>
import { apiService } from '../services/api'

export default {
  name: 'Dashboard',
  data() {
    return {
      apiStatus: 'checking',
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
        const version = await apiService.getVersion()
        
        this.apiStatus = 'connected'
        this.apiMessage = `🟢 ${health.message} - ${version.platform} ${version.version}`
      } catch (error) {
        this.apiStatus = 'error'
        this.apiMessage = '🔴 تعذر الاتصال بالخادم'
      }
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
.dashboard {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
}

h1 {
  text-align: center;
  margin-bottom: 2rem;
  color: #333;
  font-size: 2.5rem;
}

.connection-status {
  margin-bottom: 2rem;
}

.status-card {
  background: white;
  padding: 1.5rem;
  border-radius: 10px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
  border-left: 5px solid #ccc;
  position: relative;
}

.status-card.connected {
  border-left-color: #4CAF50;
}

.status-card.error {
  border-left-color: #f44336;
}

.status-card.checking {
  border-left-color: #FFC107;
}

.status-indicator {
  position: absolute;
  top: 1.5rem;
  right: 1.5rem;
  width: 12px;
  height: 12px;
  border-radius: 50%;
}

.connected .status-indicator {
  background: #4CAF50;
}

.error .status-indicator {
  background: #f44336;
}

.checking .status-indicator {
  background: #FFC107;
  animation: pulse 1.5s infinite;
}

@keyframes pulse {
  0% { opacity: 1; }
  50% { opacity: 0.5; }
  100% { opacity: 1; }
}

.stats {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
  margin-bottom: 3rem;
}

.stat-card {
  background: white;
  padding: 2rem;
  border-radius: 15px;
  box-shadow: 0 4px 15px rgba(0,0,0,0.1);
  text-align: center;
  transition: transform 0.3s ease;
}

.stat-card:hover {
  transform: translateY(-5px);
}

.stat-card h3 {
  color: #666;
  margin-bottom: 1rem;
  font-size: 1.1rem;
}

.number {
  font-size: 3rem;
  font-weight: bold;
  color: #667eea;
  margin: 1rem 0;
}

.connect-btn, .schedule-btn, .analytics-btn {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 25px;
  cursor: pointer;
  font-size: 0.9rem;
  margin-top: 1rem;
  transition: all 0.3s ease;
}

.connect-btn:hover, .schedule-btn:hover, .analytics-btn:hover {
  transform: scale(1.05);
  box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
}

.quick-actions {
  background: white;
  padding: 2rem;
  border-radius: 15px;
  box-shadow: 0 4px 15px rgba(0,0,0,0.1);
}

.quick-actions h2 {
  color: #333;
  margin-bottom: 1.5rem;
  text-align: center;
}

.actions-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
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
}

.action-btn:hover {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  transform: translateY(-3px);
  box-shadow: 0 8px 25px rgba(102, 126, 234, 0.3);
}

.icon {
  font-size: 2rem;
}
</style>
