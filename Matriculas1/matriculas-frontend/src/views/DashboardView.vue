<template>
  <div class="flex h-screen bg-gray-50">
    <AppSidebar :is-open="sidebarOpen" @close="sidebarOpen = false" />
    
    <div class="flex-1 flex flex-col overflow-hidden">
      <AppHeader @toggle-sidebar="sidebarOpen = !sidebarOpen" />
      
      <main class="flex-1 overflow-x-hidden overflow-y-auto bg-gray-50 p-6">
        <!-- Stats Cards -->
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <div class="card">
            <div class="flex items-center">
              <div class="p-2 bg-blue-100 rounded-lg">
                <Users class="w-8 h-8 text-blue-600" />
              </div>
              <div class="ml-4">
                <p class="text-sm font-medium text-gray-600">Total Estudiantes</p>
                <p class="text-2xl font-semibold text-gray-900">{{ stats.totalStudents }}</p>
              </div>
            </div>
          </div>

          <div class="card">
            <div class="flex items-center">
              <div class="p-2 bg-green-100 rounded-lg">
                <BookOpen class="w-8 h-8 text-green-600" />
              </div>
              <div class="ml-4">
                <p class="text-sm font-medium text-gray-600">Cursos Activos</p>
                <p class="text-2xl font-semibold text-gray-900">{{ stats.activeCourses }}</p>
              </div>
            </div>
          </div>

          <div class="card">
            <div class="flex items-center">
              <div class="p-2 bg-yellow-100 rounded-lg">
                <FileText class="w-8 h-8 text-yellow-600" />
              </div>
              <div class="ml-4">
                <p class="text-sm font-medium text-gray-600">Matrículas Pendientes</p>
                <p class="text-2xl font-semibold text-gray-900">{{ stats.pendingEnrollments }}</p>
              </div>
            </div>
          </div>

          <div class="card">
            <div class="flex items-center">
              <div class="p-2 bg-purple-100 rounded-lg">
                <CreditCard class="w-8 h-8 text-purple-600" />
              </div>
              <div class="ml-4">
                <p class="text-sm font-medium text-gray-600">Pagos Hoy</p>
                <p class="text-2xl font-semibold text-gray-900">S/. {{ stats.todayPayments }}</p>
              </div>
            </div>
          </div>
        </div>

        <!-- Recent Activity & Quick Actions -->
        <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
          <!-- Recent Enrollments -->
          <div class="lg:col-span-2 card">
            <div class="flex items-center justify-between mb-4">
              <h3 class="text-lg font-semibold text-gray-900">Matrículas Recientes</h3>
              <RouterLink to="/enrollment" class="text-primary-600 hover:text-primary-700 text-sm font-medium">
                Ver todas
              </RouterLink>
            </div>
            
            <div v-if="loading" class="flex justify-center py-8">
              <LoadingSpinner size="medium" message="Cargando matrículas..." />
            </div>
            
            <div v-else class="space-y-4">
              <div 
                v-for="enrollment in recentEnrollments" 
                :key="enrollment.id"
                class="flex items-center justify-between p-4 bg-gray-50 rounded-lg"
              >
                <div class="flex items-center space-x-3">
                  <div class="w-10 h-10 bg-primary-100 rounded-full flex items-center justify-center">
                    <User class="w-5 h-5 text-primary-600" />
                  </div>
                  <div>
                    <p class="font-medium text-gray-900">
                      {{ enrollment.alumno?.usuario?.nombre }} {{ enrollment.alumno?.usuario?.apellido }}
                    </p>
                    <p class="text-sm text-gray-600">{{ enrollment.alumno?.codigo }}</p>
                  </div>
                </div>
                <div class="text-right">
                  <span :class="[
                    'px-2 py-1 text-xs font-medium rounded-full',
                    enrollment.estado === 'pagado' ? 'bg-green-100 text-green-800' :
                    enrollment.estado === 'pendiente' ? 'bg-yellow-100 text-yellow-800' :
                    'bg-red-100 text-red-800'
                  ]">
                    {{ enrollment.estado }}
                  </span>
                  <p class="text-sm text-gray-600 mt-1">
                    {{ formatDate(enrollment.fechaMatricula) }}
                  </p>
                </div>
              </div>
            </div>
          </div>

          <!-- Quick Actions -->
          <div class="card">
            <h3 class="text-lg font-semibold text-gray-900 mb-4">Acciones Rápidas</h3>
            <div class="space-y-3">
              <RouterLink 
                to="/students"
                class="block p-3 rounded-lg border border-gray-200 hover:bg-gray-50 transition-colors"
              >
                <div class="flex items-center space-x-3">
                  <UserPlus class="w-5 h-5 text-blue-600" />
                  <span class="font-medium text-gray-900">Nuevo Estudiante</span>
                </div>
              </RouterLink>

              <RouterLink 
                to="/courses"
                class="block p-3 rounded-lg border border-gray-200 hover:bg-gray-50 transition-colors"
              >
                <div class="flex items-center space-x-3">
                  <Plus class="w-5 h-5 text-green-600" />
                  <span class="font-medium text-gray-900">Nuevo Curso</span>
                </div>
              </RouterLink>

              <RouterLink 
                to="/enrollment"
                class="block p-3 rounded-lg border border-gray-200 hover:bg-gray-50 transition-colors"
              >
                <div class="flex items-center space-x-3">
                  <FileText class="w-5 h-5 text-yellow-600" />
                  <span class="font-medium text-gray-900">Nueva Matrícula</span>
                </div>
              </RouterLink>

              <RouterLink 
                to="/payments"
                class="block p-3 rounded-lg border border-gray-200 hover:bg-gray-50 transition-colors"
              >
                <div class="flex items-center space-x-3">
                  <DollarSign class="w-5 h-5 text-purple-600" />
                  <span class="font-medium text-gray-900">Registrar Pago</span>
                </div>
              </RouterLink>
            </div>
          </div>
        </div>
      </main>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { RouterLink } from 'vue-router'
import AppHeader from '@/components/common/AppHeader.vue'
import AppSidebar from '@/components/common/AppSidebar.vue'
import LoadingSpinner from '@/components/common/LoadingSpinner.vue'
import { 
  Users, BookOpen, FileText, CreditCard, User, UserPlus, 
  Plus, DollarSign 
} from 'lucide-vue-next'
import { enrollmentAPI } from '@/services/api'

const sidebarOpen = ref(false)
const loading = ref(true)

const stats = ref({
  totalStudents: 0,
  activeCourses: 0,
  pendingEnrollments: 0,
  todayPayments: 0
})

const recentEnrollments = ref([])

const fetchDashboardData = async () => {
  try {
    // Fetch recent enrollments
    const enrollmentResponse = await enrollmentAPI.getAll({ limit: 5 })
    recentEnrollments.value = enrollmentResponse.data.data || []
    
    // Mock stats for demo
    stats.value = {
      totalStudents: 156,
      activeCourses: 24,
      pendingEnrollments: 8,
      todayPayments: 2450
    }
  } catch (error) {
    console.error('Error fetching dashboard data:', error)
    window.notify?.('Error al cargar datos del dashboard', 'error')
  } finally {
    loading.value = false
  }
}

const formatDate = (dateString) => {
  return new Date(dateString).toLocaleDateString('es-ES', {
    day: '2-digit',
    month: '2-digit',
    year: 'numeric'
  })
}

onMounted(() => {
  fetchDashboardData()
})
</script>