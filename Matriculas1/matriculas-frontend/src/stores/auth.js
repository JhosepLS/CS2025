import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { authAPI } from '@/services/api'

export const useAuthStore = defineStore('auth', () => {
  const user = ref(null)
  const token = ref(localStorage.getItem('token'))
  const loading = ref(false)

  const isAuthenticated = computed(() => !!token.value)

  const login = async (credentials) => {
    loading.value = true
    try {
      const response = await authAPI.login(credentials)
      const { data } = response.data
      
      user.value = data
      token.value = data.token
      localStorage.setItem('token', data.token)
      
      return { success: true }
    } catch (error) {
      return { 
        success: false, 
        message: error.response?.data?.message || 'Error en el inicio de sesión' 
      }
    } finally {
      loading.value = false
    }
  }

  const logout = () => {
    user.value = null
    token.value = null
    localStorage.removeItem('token')
  }

  const getProfile = async () => {
    if (!token.value) return
    
    try {
      const response = await authAPI.profile()
      user.value = response.data.data
    } catch (error) {
      logout()
    }
  }

  // Initialize auth state
  if (token.value) {
    getProfile()
  }

  return {
    user,
    token,
    loading,
    isAuthenticated,
    login,
    logout,
    getProfile
  }
})