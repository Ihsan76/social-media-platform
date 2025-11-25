<template>
  <div id="app">
    <nav class="navbar">
      <div class="nav-brand">
        🚀 إدارة وسائل التواصل الاجتماعي
      </div>
      <div class="nav-links">
        <router-link to="/" class="nav-link">الرئيسية</router-link>
        <router-link to="/accounts" class="nav-link">الحسابات</router-link>
        <router-link to="/schedule" class="nav-link">الجدولة</router-link>
        <router-link to="/analytics" class="nav-link">الإحصائيات</router-link>
      </div>
      <div class="nav-actions">
        <button v-if="!isAuthenticated" class="btn btn-outline" @click="login">
          تسجيل الدخول
        </button>
        <div v-else class="user-info">
          <span>مرحباً، User</span>
          <button class="btn btn-outline" @click="logout">تسجيل الخروج</button>
        </div>
      </div>
    </nav>
    
    <main class="main-content">
      <router-view />
    </main>
  </div>
</template>

<script>
import authService from './services/auth'

export default {
  name: 'App',
  data() {
    return {
      isAuthenticated: false
    }
  },
  async mounted() {
    this.isAuthenticated = authService.isAuthenticated()
    if (!this.isAuthenticated) {
      await this.login()
    }
  },
  methods: {
    async login() {
      try {
        await authService.login()
        this.isAuthenticated = true
      } catch (error) {
        console.error('Login failed:', error)
        alert('فشل تسجيل الدخول')
      }
    },
    logout() {
      authService.removeAuthToken()
      this.isAuthenticated = false
      this.$router.push('/')
    }
  }
}
</script>

<style>
/* الأنماط الأساسية - سيتم استبدالها بملف CSS المنظم */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  background: #f5f5f5;
  direction: rtl;
}

.navbar {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 1rem 2rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}

.nav-brand {
  font-size: 1.5rem;
  font-weight: bold;
}

.nav-links {
  display: flex;
  gap: 2rem;
}

.nav-link {
  color: white;
  text-decoration: none;
  padding: 0.5rem 1rem;
  border-radius: 5px;
  transition: background 0.3s ease;
}

.nav-link:hover, .nav-link.router-link-active {
  background: rgba(255,255,255,0.2);
}

.nav-actions {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.btn {
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-size: 0.9rem;
  font-weight: bold;
  transition: all 0.3s ease;
}

.btn-outline {
  background: transparent;
  border: 2px solid white;
  color: white;
}

.btn-outline:hover {
  background: white;
  color: #667eea;
}

.main-content {
  min-height: calc(100vh - 80px);
}
</style>
