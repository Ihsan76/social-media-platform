import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'https://social-media-platform-production.up.railway.app/api'

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json'
  }
})

// interceptor لإضافة token تلقائياً
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('authToken')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// interceptor للتعامل مع أخطاء المصادقة
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('authToken')
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

export const apiService = {
  async healthCheck() {
    const response = await api.get('/health')
    return response.data
  },

  async getVersion() {
    const response = await api.get('/version')
    return response.data
  },

  async getAccounts() {
    const response = await api.get('/accounts')
    return response.data
  },

  async addAccount(accountData) {
    const response = await api.post('/accounts', accountData)
    return response.data
  },

  async getScheduledPosts() {
    const response = await api.get('/schedule')
    return response.data
  },

  async schedulePost(postData) {
    const response = await api.post('/schedule', postData)
    return response.data
  }
}

export default api
