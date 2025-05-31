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
      console.log('Intentando iniciar sesión:', credentials.email)
      const response = await authAPI.login(credentials)
      const { data } = response.data
      
      user.value = data
      token.value = data.token
      localStorage.setItem('token', data.token)
      
      console.log('Inicio de sesión exitoso:', data)
      return { success: true }
    } catch (error) {
      console.error('Error en login:', error)
      const message = error.response?.data?.message || 'Error en el inicio de sesión'
      return { success: false, message }
    } finally {
      loading.value = false
    }
  }

  const logout = () => {
    console.log('Cerrando sesión')
    user.value = null
    token.value = null
    localStorage.removeItem('token')
  }

  const getProfile = async () => {
    if (!token.value) return
    
    try {
      console.log('Obteniendo perfil de usuario')
      const response = await authAPI.profile()
      user.value = response.data.data
      console.log('Perfil obtenido:', user.value)
    } catch (error) {
      console.error('Error al obtener perfil:', error)
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