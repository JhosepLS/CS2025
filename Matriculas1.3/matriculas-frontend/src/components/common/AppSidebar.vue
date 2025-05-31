<template>
  <aside 
    :class="[
      'fixed inset-y-0 left-0 z-50 w-64 bg-white shadow-lg transform transition-transform duration-300 ease-in-out lg:translate-x-0 lg:static lg:inset-0',
      isOpen ? 'translate-x-0' : '-translate-x-full'
    ]"
  >
    <!-- Logo -->
    <div class="flex items-center justify-between h-16 px-6 border-b border-gray-200">
      <div class="flex items-center space-x-2">
        <div class="w-8 h-8 bg-primary-600 rounded-lg flex items-center justify-center">
          <GraduationCap class="w-5 h-5 text-white" />
        </div>
        <span class="text-lg font-semibold text-gray-900">Matrículas</span>
      </div>
      <button
        @click="$emit('close')"
        class="lg:hidden p-1 rounded-md text-gray-600 hover:text-gray-900 hover:bg-gray-100"
      >
        <X class="w-5 h-5" />
      </button>
    </div>

    <!-- Navigation -->
    <nav class="mt-6 px-3">
      <ul class="space-y-1">
        <li v-for="item in navigationItems" :key="item.name">
          <RouterLink
            :to="item.path"
            :class="[
              'flex items-center px-3 py-2 text-sm font-medium rounded-lg transition-colors',
              $route.name === item.name
                ? 'bg-primary-50 text-primary-700 border-r-2 border-primary-600'
                : 'text-gray-700 hover:bg-gray-50 hover:text-gray-900'
            ]"
            @click="$emit('close')"
          >
            <component :is="item.icon" class="w-5 h-5 mr-3" />
            {{ item.label }}
            <span 
              v-if="item.badge" 
              class="ml-auto bg-primary-100 text-primary-600 text-xs px-2 py-1 rounded-full"
            >
              {{ item.badge }}
            </span>
          </RouterLink>
        </li>
      </ul>
    </nav>

    <!-- User Info -->
    <div class="absolute bottom-0 left-0 right-0 p-4 border-t border-gray-200">
      <div class="flex items-center space-x-3">
        <div class="w-10 h-10 bg-primary-500 rounded-full flex items-center justify-center">
          <span class="text-white text-sm font-medium">
            {{ userInitials }}
          </span>
        </div>
        <div class="flex-1 min-w-0">
          <p class="text-sm font-medium text-gray-900 truncate">
            {{ authStore.user?.nombre }} {{ authStore.user?.apellido }}
          </p>
          <p class="text-xs text-gray-600 truncate">{{ authStore.user?.rol }}</p>
        </div>
      </div>
    </div>
  </aside>

  <!-- Overlay -->
  <div 
    v-if="isOpen"
    @click="$emit('close')"
    class="fixed inset-0 bg-gray-600 bg-opacity-75 z-40 lg:hidden"
  ></div>
</template>

<script setup>
import { computed } from 'vue'
import { RouterLink } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { 
  GraduationCap, 
  LayoutDashboard, 
  Users, 
  BookOpen, 
  FileText, 
  CreditCard,
  X 
} from 'lucide-vue-next'

defineProps({
  isOpen: {
    type: Boolean,
    default: false
  }
})

defineEmits(['close'])

const authStore = useAuthStore()

const navigationItems = [
  {
    name: 'Dashboard',
    label: 'Panel de Control',
    path: '/',
    icon: LayoutDashboard
  },
  {
    name: 'Students',
    label: 'Estudiantes',
    path: '/students',
    icon: Users
  },
  {
    name: 'Courses',
    label: 'Cursos',
    path: '/courses',
    icon: BookOpen
  },
  {
    name: 'Enrollment',
    label: 'Matrículas',
    path: '/enrollment',
    icon: FileText
  },
  {
    name: 'Payments',
    label: 'Pagos',
    path: '/payments',
    icon: CreditCard
  }
]

const userInitials = computed(() => {
  const user = authStore.user
  if (!user) return '?'
  return `${user.nombre?.charAt(0) || ''}${user.apellido?.charAt(0) || ''}`.toUpperCase()
})
</script>