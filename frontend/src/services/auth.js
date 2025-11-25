import api from './api'

class AuthService {
  constructor() {
    this.token = localStorage.getItem('authToken')
    if (this.token) {
      this.setAuthToken(this.token)
    }
  }

  setAuthToken(token) {
    this.token = token
    localStorage.setItem('authToken', token)
    if (api && api.defaults) {
      api.defaults.headers.common['Authorization'] = `Bearer ${token}`
    }
  }

  removeAuthToken() {
    this.token = null
    localStorage.removeItem('authToken')
    if (api && api.defaults && api.defaults.headers.common) {
      delete api.defaults.headers.common['Authorization']
    }
  }

  async login() {
    try {
      const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'https://social-media-platform-production.up.railway.app/api'
      const response = await fetch(`${API_BASE_URL}/auth/login`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        }
      })
      const data = await response.json()
      
      if (response.ok) {
        this.setAuthToken(data.access_token)
        return data
      } else {
        throw new Error(data.message || 'فشل تسجيل الدخول')
      }
    } catch (error) {
      this.removeAuthToken()
      throw error
    }
  }

  isAuthenticated() {
    return !!this.token
  }

  getToken() {
    return this.token
  }
}

export default new AuthService()
