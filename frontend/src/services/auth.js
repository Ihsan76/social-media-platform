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
    api.defaults.headers.common['Authorization'] = `Bearer ${token}`
  }

  removeAuthToken() {
    this.token = null
    localStorage.removeItem('authToken')
    delete api.defaults.headers.common['Authorization']
  }

  async login() {
    try {
      const response = await api.post('/auth/login')
      this.setAuthToken(response.data.access_token)
      return response.data
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
