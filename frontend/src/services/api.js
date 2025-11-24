import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:5000/api'

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json'
  }
})

export const apiService = {
  // اختبار الاتصال بالـ API
  async healthCheck() {
    const response = await api.get('/health')
    return response.data
  },

  async getVersion() {
    const response = await api.get('/version')
    return response.data
  }
}

export default api
