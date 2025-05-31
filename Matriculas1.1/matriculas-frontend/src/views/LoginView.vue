<template>
  <div class="min-h-screen flex items-center justify-center bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
    <div class="max-w-md w-full space-y-8">
      <!-- Header -->
      <div class="text-center">
        <div class="flex justify-center">
          <div class="w-16 h-16 bg-primary-600 rounded-full flex items-center justify-center">
            <GraduationCap class="w-8 h-8 text-white" />
          </div>
        </div>
        <h2 class="mt-6 text-3xl font-extrabold text-gray-900">
          Sistema de Matrículas
        </h2>
        <p class="mt-2 text-sm text-gray-600">
          Inicia sesión para acceder al sistema
        </p>
      </div>

      <!-- Login Form -->
      <form @submit.prevent="handleLogin" class="mt-8 space-y-6">
        <div class="space-y-4">
          <div>
            <label for="email" class="block text-sm font-medium text-gray-700">
              Correo electrónico
            </label>
            <div class="mt-1 relative">
              <input
                id="email"
                v-model="form.email"
                type="email"
                required
                class="input-field pl-10"
                placeholder="Ingresa tu correo"
                :disabled="loading"
              />
              <Mail class="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400" />
            </div>
          </div>

          <div>
            <label for="password" class="block text-sm font-medium text-gray-700">
              Contraseña
            </label>
            <div class="mt-1 relative">
              <input
                id="password"
                v-model="form.password"
                :type="showPassword ? 'text' : 'password'"
                required
                class="input-field pl-10 pr-10"
                placeholder="Ingresa tu contraseña"
                :disabled="loading"
              />
              <Lock class="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400" />
              <button
                type="button"
                @click="showPassword = !showPassword"
                class="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-400 hover:text-gray-600"
                :disabled="loading"
              >
                <Eye v-if="!showPassword" class="w-5 h-5" />
                <EyeOff v-else class="w-5 h-5" />
              </button>
            </div>
          </div>
        </div>

        <!-- Error Message -->
        <div v-if="error" class="rounded-md bg-red-50 p-4">
          <div class="flex">
            <AlertCircle class="w-5 h-5 text-red-400" />
            <div class="ml-3">
              <p class="text-sm text-red-800">{{ error }}</p>
            </div>
          </div>
        </div>

        <!-- Submit Button -->
        <button
          type="submit"
          :disabled="loading"
          class="w-full btn-primary flex items-center justify-center space-x-2 py-3"
        >
          <LoadingSpinner v-if="loading" size="small" />
          <LogIn v-else class="w-5 h-5" />
          <span>{{ loading ? 'Iniciando sesión...' : 'Iniciar Sesión' }}</span>
        </button>
      </form>

      <!-- Demo Credentials -->
      <div class="mt-6 p-4 bg-blue-50 rounded-lg">
        <h3 class="text-sm font-medium text-blue-800 mb-2">Credenciales de prueba:</h3>
        <div class="text-xs text-blue-700 space-y-1">
          <p><strong>Admin:</strong> admin@matriculas.com / admin123</p>
          <p><strong>Docente:</strong> juan.perez@matriculas.com / password123</p>
          <p><strong>Alumno:</strong> pedro.sanchez@matriculas.com / password123</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { GraduationCap, Mail, Lock, Eye, EyeOff, LogIn, AlertCircle } from 'lucide-vue-next'
import LoadingSpinner from '@/components/common/LoadingSpinner.vue'

const router = useRouter()
const authStore = useAuthStore()

const form = ref({
  email: '',
  password: ''
})

const showPassword = ref(false)
const loading = ref(false)
const error = ref('')

const handleLogin = async () => {
  loading.value = true
  error.value = ''

  const result = await authStore.login(form.value)

  if (result.success) {
    window.notify?.('Inicio de sesión exitoso', 'success')
    router.push('/')
  } else {
    error.value = result.message
  }

  loading.value = false
}
</script>