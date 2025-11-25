<template>
  <div class="accounts-page container">
    <div class="page-header d-flex justify-between align-center">
      <h1>👥 إدارة الحسابات الاجتماعية</h1>
      <button class="btn btn-primary" @click="showAddAccountModal = true">
        + إضافة حساب جديد
      </button>
    </div>

    <!-- إحصائيات سريعة -->
    <div class="stats-grid d-grid">
      <div class="card card-stat" v-for="platform in platformStats" :key="platform.id">
        <div class="icon">{{ platform.icon }}</div>
        <div class="content">
          <h3>{{ platform.name }}</h3>
          <p class="number">{{ platform.count }}</p>
        </div>
      </div>
    </div>

    <!-- قائمة الحسابات -->
    <div class="accounts-section">
      <div v-if="loading" class="loading text-center p-5">جاري تحميل الحسابات...</div>
      
      <div v-else-if="accounts.length === 0" class="empty-state card text-center">
        <div class="empty-icon">🔗</div>
        <h3>لا توجد حسابات متصلة</h3>
        <p class="text-muted">ابدأ بربط حسابك الأول لإدارة منشوراتك</p>
        <button class="btn btn-primary" @click="showAddAccountModal = true">
          ربط حساب جديد
        </button>
      </div>

      <div v-else class="accounts-grid d-grid">
        <div v-for="account in accounts" :key="account.id" class="card account-card">
          <div class="card-header d-flex justify-between align-center">
            <div class="platform-badge" :class="account.platform">
              {{ getPlatformIcon(account.platform) }}
            </div>
            <div class="account-actions d-flex">
              <button class="btn-icon" @click="toggleAccountStatus(account)" 
                      :title="account.is_active ? 'إيقاف' : 'تفعيل'">
                {{ account.is_active ? '⏸️' : '▶️' }}
              </button>
              <button class="btn-icon btn-danger" @click="deleteAccount(account)" title="حذف">
                🗑️
              </button>
            </div>
          </div>
          
          <div class="card-body">
            <h4 class="m-0">{{ account.account_name }}</h4>
            <p class="platform-name text-muted">{{ getPlatformName(account.platform) }}</p>
            <div class="account-meta d-flex justify-between align-center">
              <span class="status" :class="{ active: account.is_active }">
                {{ account.is_active ? '🟢 نشط' : '🔴 غير نشط' }}
              </span>
              <span class="date text-muted">{{ formatDate(account.created_at) }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- نافذة إضافة حساب -->
    <div v-if="showAddAccountModal" class="modal-overlay">
      <div class="modal card">
        <div class="card-header d-flex justify-between align-center">
          <h3 class="m-0">ربط حساب جديد</h3>
          <button class="btn-close" @click="showAddAccountModal = false">✕</button>
        </div>
        
        <div class="card-body">
          <div class="form-group">
            <label class="text-bold">اختر المنصة:</label>
            <div class="platform-options d-grid">
              <div v-for="platform in platforms" :key="platform.id" 
                   class="platform-option rounded" 
                   :class="{ selected: newAccount.platform === platform.id }"
                   @click="newAccount.platform = platform.id">
                <span class="platform-icon">{{ platform.icon }}</span>
                <span class="platform-text">{{ platform.name }}</span>
              </div>
            </div>
          </div>

          <div class="form-group">
            <label class="text-bold">اسم الحساب:</label>
            <input type="text" v-model="newAccount.account_name" 
                   class="form-control"
                   placeholder="مثال: my_twitter_account">
          </div>

          <div class="form-group">
            <label class="text-bold">رمز الوصول (Access Token):</label>
            <input type="password" v-model="newAccount.access_token" 
                   class="form-control"
                   placeholder="أدخل token الوصول">
          </div>
        </div>

        <div class="card-footer d-flex justify-end">
          <button class="btn btn-secondary m-1" @click="showAddAccountModal = false">
            إلغاء
          </button>
          <button class="btn btn-primary m-1" @click="addAccount" :disabled="!isFormValid">
            حفظ الحساب
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { apiService } from '../services/api'

export default {
  name: 'Accounts',
  data() {
    return {
      accounts: [],
      loading: false,
      showAddAccountModal: false,
      newAccount: {
        platform: '',
        account_name: '',
        access_token: ''
      },
      platforms: [
        { id: 'twitter', name: 'Twitter', icon: '🐦' },
        { id: 'facebook', name: 'Facebook', icon: '📘' },
        { id: 'instagram', name: 'Instagram', icon: '📷' },
        { id: 'linkedin', name: 'LinkedIn', icon: '💼' },
        { id: 'tiktok', name: 'TikTok', icon: '🎵' }
      ]
    }
  },
  computed: {
    platformStats() {
      const stats = {}
      this.accounts.forEach(account => {
        if (!stats[account.platform]) {
          const platform = this.platforms.find(p => p.id === account.platform)
          stats[account.platform] = {
            id: account.platform,
            name: platform ? platform.name : account.platform,
            icon: platform ? platform.icon : '🔗',
            count: 0
          }
        }
        stats[account.platform].count++
      })
      
      // إرجاع مصفوفة من الإحصائيات
      return Object.values(stats)
    },
    isFormValid() {
      return this.newAccount.platform && 
             this.newAccount.account_name && 
             this.newAccount.access_token
    }
  },
  async mounted() {
    await this.loadAccounts()
  },
  methods: {
    async loadAccounts() {
      this.loading = true
      try {
        const response = await apiService.getAccounts()
        this.accounts = response.accounts
      } catch (error) {
        console.error('Error loading accounts:', error)
        alert('فشل في تحميل الحسابات')
      } finally {
        this.loading = false
      }
    },

    async addAccount() {
      try {
        await apiService.addAccount(this.newAccount)
        this.showAddAccountModal = false
        this.resetForm()
        await this.loadAccounts()
        alert('تم إضافة الحساب بنجاح!')
      } catch (error) {
        console.error('Error adding account:', error)
        alert('فشل في إضافة الحساب')
      }
    },

    async toggleAccountStatus(account) {
      try {
        // TODO: تحديث حالة الحساب في الخادم
        account.is_active = !account.is_active
        alert(`تم ${account.is_active ? 'تفعيل' : 'إيقاف'} الحساب`)
      } catch (error) {
        console.error('Error updating account:', error)
      }
    },

    async deleteAccount(account) {
      if (confirm(`هل أنت متأكد من حذف حساب ${account.account_name}؟`)) {
        try {
          // TODO: حذف الحساب من الخادم
          this.accounts = this.accounts.filter(acc => acc.id !== account.id)
          alert('تم حذف الحساب بنجاح')
        } catch (error) {
          console.error('Error deleting account:', error)
        }
      }
    },

    resetForm() {
      this.newAccount = {
        platform: '',
        account_name: '',
        access_token: ''
      }
    },

    getPlatformIcon(platform) {
      const platformObj = this.platforms.find(p => p.id === platform)
      return platformObj ? platformObj.icon : '🔗'
    },

    getPlatformName(platform) {
      const platformObj = this.platforms.find(p => p.id === platform)
      return platformObj ? platformObj.name : platform
    },

    formatDate(dateString) {
      return new Date(dateString).toLocaleDateString('ar-EG')
    }
  }
}
</script>

<style scoped>
.accounts-page {
  padding: var(--spacing-xl) 0;
}

.page-header {
  margin-bottom: var(--spacing-xl);
}

.stats-grid {
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: var(--spacing-lg);
  margin-bottom: var(--spacing-xl);
}

.accounts-section {
  margin-top: var(--spacing-xl);
}

.accounts-grid {
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: var(--spacing-lg);
}

.account-card {
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.account-card:hover {
  transform: translateY(-5px);
}

.platform-badge {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
  background: white;
  box-shadow: var(--shadow-sm);
}

.account-actions {
  gap: var(--spacing-xs);
}

.platform-name {
  margin: var(--spacing-xs) 0 var(--spacing-md) 0;
  text-transform: capitalize;
}

.account-meta {
  font-size: var(--font-size-sm);
}

.status.active {
  color: var(--success-color);
  font-weight: bold;
}

.status:not(.active) {
  color: var(--danger-color);
  font-weight: bold;
}

.empty-state {
  padding: var(--spacing-xxl) var(--spacing-xl);
}

.empty-icon {
  font-size: 4rem;
  margin-bottom: var(--spacing-lg);
}

.loading {
  font-size: var(--font-size-lg);
  color: var(--text-muted);
}

/* Modal Styles */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0,0,0,0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal {
  width: 90%;
  max-width: 500px;
  max-height: 90vh;
  overflow-y: auto;
}

.platform-options {
  grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
  gap: var(--spacing-sm);
}

.platform-option {
  border: 2px solid #e9ecef;
  padding: var(--spacing-lg);
  text-align: center;
  cursor: pointer;
  transition: all 0.3s ease;
}

.platform-option:hover {
  border-color: var(--primary-color);
}

.platform-option.selected {
  border-color: var(--primary-color);
  background: var(--bg-secondary);
}

.platform-icon {
  font-size: 2rem;
  display: block;
  margin-bottom: var(--spacing-sm);
}

.platform-text {
  font-weight: bold;
  color: var(--text-primary);
}

/* Form Styles */
.form-group {
  margin-bottom: var(--spacing-lg);
}

.form-group label {
  display: block;
  margin-bottom: var(--spacing-sm);
}

.form-control {
  width: 100%;
  padding: var(--spacing-md);
  border: 1px solid #ddd;
  border-radius: var(--border-radius);
  font-size: var(--font-size-base);
  transition: border-color 0.3s ease;
}

.form-control:focus {
  outline: none;
  border-color: var(--primary-color);
  box-shadow: 0 0 0 2px rgba(102, 126, 234, 0.1);
}
</style>
