<template>
  <div class="dashboard">
    <h1>مرحباً بك في نظام إدارة وسائل التواصل الاجتماعي</h1>
    <p>التطبيق يعمل بنجاح! 🎉</p>
    <button @click="testAPI">اختبار الاتصال بالخادم</button>
    <p v-if="apiStatus">{{ apiStatus }}</p>
  </div>
</template>

<script>
import { apiService } from '../services/api'

export default {
  name: 'Dashboard',
  data() {
    return {
      apiStatus: ''
    }
  },
  methods: {
    async testAPI() {
      try {
        const health = await apiService.healthCheck()
        this.apiStatus = `✅ الخادم يعمل: ${health.message}`
      } catch (error) {
        this.apiStatus = '❌ فشل الاتصال بالخادم'
      }
    }
  }
}
</script>
