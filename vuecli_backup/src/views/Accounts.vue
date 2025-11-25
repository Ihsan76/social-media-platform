<template>
  <div class="accounts">
    <h1>إدارة الحسابات</h1>
    <p>هذه صفحة إدارة الحسابات</p>
    <button @click="loadAccounts">تحميل الحسابات</button>
    <div v-if="accounts.length">
      <h3>الحسابات المتصلة:</h3>
      <ul>
        <li v-for="account in accounts" :key="account.id">
          {{ account.account_name }} - {{ account.platform }}
        </li>
      </ul>
    </div>
  </div>
</template>

<script>
import { apiService } from '../services/api'

export default {
  name: 'Accounts',
  data() {
    return {
      accounts: []
    }
  },
  methods: {
    async loadAccounts() {
      try {
        const data = await apiService.getAccounts()
        this.accounts = data.accounts
      } catch (error) {
        console.error('Error loading accounts:', error)
        alert('فشل في تحميل الحسابات')
      }
    }
  }
}
</script>
