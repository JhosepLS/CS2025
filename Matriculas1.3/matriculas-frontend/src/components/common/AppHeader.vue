<template>
  <header class="bg-white shadow-sm border-b border-gray-200">
    <div class="px-6 py-4">
      <div class="flex items-center justify-between">
        <div class="flex items-center space-x-4">
          <button
            @click="$emit('toggleSidebar')"
            class="lg:hidden p-2 rounded-md text-gray-600 hover:text-gray-900 hover:bg-gray-100"
          >
            <Menu class="w-6 h-6" />
          </button>
          <div>
            <h1 class="text-xl font-semibold text-gray-900">{{ pageTitle }}</h1>
            <p v-if="pageSubtitle" class="text-sm text-gray-600">{{ pageSubtitle }}</p>
          </div>
        </div>

        <div class="flex items-center space-x-4">
          <!-- Notifications -->
          <button class="p-2 rounded-md text-gray-600 hover:text-gray-900 hover:bg-gray-100">
            <Bell class="w-5 h-5" />
          </button>

          <!-- User Menu -->
          <div class="relative" ref="userMenuRef">
            <button
              @click="showUserMenu = !showUserMenu"
              class="flex items-center space-x-2 p-2 rounded-md text-gray-600 hover:text-gray-900 hover:bg-gray-100"
            >
              <div class="w-8 h-8 bg-primary-500 rounded-full flex items-center justify-center">
                <span class="text-white text-sm font-medium">
                  {{ userInitials }}
                </span>
              </div>
              <ChevronDown class="w-4 h-4" />
            </button>

            <Transition name="dropdown">
              <div
                v-show="showUserMenu"
                class="absolute right-0 mt-2 w-48 bg-white rounded-md shadow-lg border border-gray-200 py-1 z-50"
              >
                <div class="px-4 py-2 border-b border-gray-100">
                  <p class="text-sm font-medium text-gray-900">{{ authStore.user?.nombre }} {{ authStore.user?.apellido }}</p>
                  <p class="text-xs text-gray-600">{{ authStore.user?.email }}</p>
                </div>
                <button
                  @click="logout"
                  class="w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 flex items-center space-x-2"
                >
                  <LogOut class="w-4 h-4" />
                  <span>Cerrar Sesión</span>
                </button>
              </div>
            </Transition>
          </div>
        </div>
      </div>
    </div>
  </header>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { Menu, Bell, ChevronDown, LogOut } from 'lucide-vue-next'

defineEmits(['toggleSidebar'])

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()

const showUserMenu = ref(false)
const userMenuRef = ref(null)

const pageTitle = computed(() => {
  const titles = {
    'Dashboard': 'Panel de Control',
    'Students': 'Estudiantes',
    'Courses': 'Cursos',
    'Enrollment': 'Matrículas',
    'Payments': 'Pagos'
  }
  return titles[route.name] || 'Sistema de Matrículas'
})

const pageSubtitle = computed(() => {
  const subtitles = {
    'Dashboard': 'Resumen general del sistema',
    'Students': 'Gestión de estudiantes',
    'Courses': 'Gestión de cursos académicos',
    'Enrollment': 'Proceso de matrícula',
    'Payments': 'Gestión de pagos y finanzas'
  }
  return subtitles[route.name]
})

const userInitials = computed(() => {
  const user = authStore.user
  if (!user) return '?'
  return `${user.nombre?.charAt(0) || ''}${user.apellido?.charAt(0) || ''}`.toUpperCase()
})

const logout = async () => {
  authStore.logout()
  router.push('/login')
  showUserMenu.value = false
}
</script>

<style scoped>
.dropdown-enter-active,
.dropdown-leave-active {
  transition: all 0.2s ease;
}

.dropdown-enter-from,
.dropdown-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}
</style>