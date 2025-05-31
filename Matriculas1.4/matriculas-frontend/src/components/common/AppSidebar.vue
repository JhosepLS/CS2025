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
        <!-- Dashboard -->
        <li>
          <RouterLink
            to="/"
            :class="[
              'flex items-center px-3 py-2 text-sm font-medium rounded-lg transition-colors',
              $route.name === 'Dashboard'
                ? 'bg-primary-50 text-primary-700 border-r-2 border-primary-600'
                : 'text-gray-700 hover:bg-gray-50 hover:text-gray-900'
            ]"
            @click="$emit('close')"
          >
            <LayoutDashboard class="w-5 h-5 mr-3" />
            Panel de Control
          </RouterLink>
        </li>

        <!-- Gestión Académica -->
        <li class="mt-6">
          <div class="px-3 text-xs font-medium text-gray-500 uppercase tracking-wider">
            Gestión Académica
          </div>
        </li>

        <li>
          <RouterLink
            to="/faculties"
            :class="[
              'flex items-center px-3 py-2 text-sm font-medium rounded-lg transition-colors',
              $route.name === 'Faculties'
                ? 'bg-primary-50 text-primary-700 border-r-2 border-primary-600'
                : 'text-gray-700 hover:bg-gray-50 hover:text-gray-900'
            ]"
            @click="$emit('close')"
          >
            <Building class="w-5 h-5 mr-3" />
            Facultades
          </RouterLink>
        </li>

        <li>
          <RouterLink
            to="/schools"
            :class="[
              'flex items-center px-3 py-2 text-sm font-medium rounded-lg transition-colors',
              $route.name === 'Schools'
                ? 'bg-primary-50 text-primary-700 border-r-2 border-primary-600'
                : 'text-gray-700 hover:bg-gray-50 hover:text-gray-900'
            ]"
            @click="$emit('close')"
          >
            <Building2 class="w-5 h-5 mr-3" />
            Escuelas
          </RouterLink>
        </li>

        <li>
          <RouterLink
            to="/study-plans"
            :class="[
              'flex items-center px-3 py-2 text-sm font-medium rounded-lg transition-colors',
              $route.name === 'StudyPlans'
                ? 'bg-primary-50 text-primary-700 border-r-2 border-primary-600'
                : 'text-gray-700 hover:bg-gray-50 hover:text-gray-900'
            ]"
            @click="$emit('close')"
          >
            <BookOpenCheck class="w-5 h-5 mr-3" />
            Planes de Estudio
          </RouterLink>
        </li>

        <li>
          <RouterLink
            to="/courses"
            :class="[
              'flex items-center px-3 py-2 text-sm font-medium rounded-lg transition-colors',
              $route.name === 'Courses'
                ? 'bg-primary-50 text-primary-700 border-r-2 border-primary-600'
                : 'text-gray-700 hover:bg-gray-50 hover:text-gray-900'
            ]"
            @click="$emit('close')"
          >
            <BookOpen class="w-5 h-5 mr-3" />
            Cursos
          </RouterLink>
        </li>

        <li>
          <RouterLink
            to="/prerequisites"
            :class="[
              'flex items-center px-3 py-2 text-sm font-medium rounded-lg transition-colors',
              $route.name === 'Prerequisites'
                ? 'bg-primary-50 text-primary-700 border-r-2 border-primary-600'
                : 'text-gray-700 hover:bg-gray-50 hover:text-gray-900'
            ]"
            @click="$emit('close')"
          >
            <GitBranch class="w-5 h-5 mr-3" />
            Prerrequisitos
          </RouterLink>
        </li>

        <li>
          <RouterLink
            to="/academic-periods"
            :class="[
              'flex items-center px-3 py-2 text-sm font-medium rounded-lg transition-colors',
              $route.name === 'AcademicPeriods'
                ? 'bg-primary-50 text-primary-700 border-r-2 border-primary-600'
                : 'text-gray-700 hover:bg-gray-50 hover:text-gray-900'
            ]"
            @click="$emit('close')"
          >
            <Calendar class="w-5 h-5 mr-3" />
            Periodos Académicos
          </RouterLink>
        </li>

        <!-- Gestión de Personas -->
        <li class="mt-6">
          <div class="px-3 text-xs font-medium text-gray-500 uppercase tracking-wider">
            Gestión de Personas
          </div>
        </li>

        <li>
          <RouterLink
            to="/teachers"
            :class="[
              'flex items-center px-3 py-2 text-sm font-medium rounded-lg transition-colors',
              $route.name === 'Teachers'
                ? 'bg-primary-50 text-primary-700 border-r-2 border-primary-600'
                : 'text-gray-700 hover:bg-gray-50 hover:text-gray-900'
            ]"
            @click="$emit('close')"
          >
            <UserCheck class="w-5 h-5 mr-3" />
            Docentes
          </RouterLink>
        </li>

        <li>
          <RouterLink
            to="/students"
            :class="[
              'flex items-center px-3 py-2 text-sm font-medium rounded-lg transition-colors',
              $route.name === 'Students'
                ? 'bg-primary-50 text-primary-700 border-r-2 border-primary-600'
                : 'text-gray-700 hover:bg-gray-50 hover:text-gray-900'
            ]"
            @click="$emit('close')"
          >
            <Users class="w-5 h-5 mr-3" />
            Estudiantes
          </RouterLink>
        </li>

        <!-- Gestión de Clases -->
        <li class="mt-6">
          <div class="px-3 text-xs font-medium text-gray-500 uppercase tracking-wider">
            Gestión de Clases
          </div>
        </li>

        <li>
          <RouterLink
            to="/sections"
            :class="[
              'flex items-center px-3 py-2 text-sm font-medium rounded-lg transition-colors',
              $route.name === 'Sections'
                ? 'bg-primary-50 text-primary-700 border-r-2 border-primary-600'
                : 'text-gray-700 hover:bg-gray-50 hover:text-gray-900'
            ]"
            @click="$emit('close')"
          >
            <Layers class="w-5 h-5 mr-3" />
            Secciones
          </RouterLink>
        </li>

        <li>
          <RouterLink
            to="/schedules"
            :class="[
              'flex items-center px-3 py-2 text-sm font-medium rounded-lg transition-colors',
              $route.name === 'Schedules'
                ? 'bg-primary-50 text-primary-700 border-r-2 border-primary-600'
                : 'text-gray-700 hover:bg-gray-50 hover:text-gray-900'
            ]"
            @click="$emit('close')"
          >
            <Clock class="w-5 h-5 mr-3" />
            Horarios
          </RouterLink>
        </li>

        <!-- Procesos -->
        <li class="mt-6">
          <div class="px-3 text-xs font-medium text-gray-500 uppercase tracking-wider">
            Procesos
          </div>
        </li>

        <li>
          <RouterLink
            to="/enrollment"
            :class="[
              'flex items-center px-3 py-2 text-sm font-medium rounded-lg transition-colors',
              $route.name === 'Enrollment'
                ? 'bg-primary-50 text-primary-700 border-r-2 border-primary-600'
                : 'text-gray-700 hover:bg-gray-50 hover:text-gray-900'
            ]"
            @click="$emit('close')"
          >
            <FileText class="w-5 h-5 mr-3" />
            Matrículas
          </RouterLink>
        </li>

        <li>
          <RouterLink
            to="/payments"
            :class="[
              'flex items-center px-3 py-2 text-sm font-medium rounded-lg transition-colors',
              $route.name === 'Payments'
                ? 'bg-primary-50 text-primary-700 border-r-2 border-primary-600'
                : 'text-gray-700 hover:bg-gray-50 hover:text-gray-900'
            ]"
            @click="$emit('close')"
          >
            <CreditCard class="w-5 h-5 mr-3" />
            Pagos
          </RouterLink>
        </li>

        <!-- Configuración -->
        <li class="mt-6">
          <div class="px-3 text-xs font-medium text-gray-500 uppercase tracking-wider">
            Configuración
          </div>
        </li>

        <li>
          <RouterLink
            to="/configurations"
            :class="[
              'flex items-center px-3 py-2 text-sm font-medium rounded-lg transition-colors',
              $route.name === 'Configurations'
                ? 'bg-primary-50 text-primary-700 border-r-2 border-primary-600'
                : 'text-gray-700 hover:bg-gray-50 hover:text-gray-900'
            ]"
            @click="$emit('close')"
          >
            <Settings class="w-5 h-5 mr-3" />
            Configuraciones
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
  X,
  Building,
  Building2,
  BookOpenCheck,
  UserCheck,
  Calendar,
  Clock,
  Layers,
  GitBranch,
  Settings
} from 'lucide-vue-next'

defineProps({
  isOpen: {
    type: Boolean,
    default: false
  }
})

defineEmits(['close'])

const authStore = useAuthStore()

const userInitials = computed(() => {
  const user = authStore.user
  if (!user) return '?'
  return `${user.nombre?.charAt(0) || ''}${user.apellido?.charAt(0) || ''}`.toUpperCase()
})
</script>