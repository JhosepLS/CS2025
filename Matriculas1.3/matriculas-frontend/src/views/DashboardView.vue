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
            
            <div v-else-if="recentEnrollments.length === 0" class="text-center py-8">
              <FileText class="w-12 h-12 text-gray-400 mx-auto mb-4" />
              <p class="text-gray-600">No hay matrículas recientes</p>
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
                  <span :class="getStatusClass(enrollment.estado)">
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

        <!-- Recent Students -->
        <div class="mt-8">
          <div class="card">
            <div class="flex items-center justify-between mb-4">
              <h3 class="text-lg font-semibold text-gray-900">Estudiantes Recientes</h3>
              <RouterLink to="/students" class="text-primary-600 hover:text-primary-700 text-sm font-medium">
                Ver todos
              </RouterLink>
            </div>
            
            <div v-if="studentsStore.loading" class="flex justify-center py-8">
              <LoadingSpinner size="medium" message="Cargando estudiantes..." />
            </div>
            
            <div v-else-if="studentsStore.students.length === 0" class="text-center py-8">
              <Users class="w-12 h-12 text-gray-400 mx-auto mb-4" />
              <p class="text-gray-600">No hay estudiantes registrados</p>
            </div>
            
            <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              <div 
                v-for="student in recentStudents" 
                :key="student.id"
                class="p-4 border border-gray-200 rounded-lg hover:shadow-md transition-shadow"
              >
                <div class="flex items-center space-x-3">
                  <div class="w-12 h-12 bg-primary-100 rounded-full flex items-center justify-center">
                    <User class="w-6 h-6 text-primary-600" />
                  </div>
                  <div class="flex-1">
                    <p class="font-medium text-gray-900">
                      {{ student.usuario?.nombre }} {{ student.usuario?.apellido }}
                    </p>
                    <p class="text-sm text-gray-600">{{ student.codigo }}</p>
                    <p class="text-xs text-gray-500">Ciclo {{ student.cicloActual }}</p>
                  </div>
                  <span :class="getStatusClass(student.estado)">
                    {{ student.estado }}
                  </span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { RouterLink } from 'vue-router'
import { useStudentsStore } from '@/stores/students'
import AppHeader from '@/components/common/AppHeader.vue'
import AppSidebar from '@/components/common/AppSidebar.vue'
import LoadingSpinner from '@/components/common/LoadingSpinner.vue'
import { 
  Users, BookOpen, FileText, CreditCard, User, UserPlus, 
  Plus, DollarSign 
} from 'lucide-vue-next'
import { enrollmentAPI } from '@/services/api'

const studentsStore = useStudentsStore()

const sidebarOpen = ref(false)
const loading = ref(true)

const stats = ref({
  totalStudents: 0,
  activeCourses: 0,
  pendingEnrollments: 0,
  todayPayments: 0
})

const recentEnrollments = ref([])

const recentStudents = computed(() => {
  return studentsStore.students.slice(0, 6)
})

const fetchDashboardData = async () => {
  try {
    // Fetch recent enrollments
    try {
      const enrollmentResponse = await enrollmentAPI.getAll({ limit: 5 })
      recentEnrollments.value = enrollmentResponse.data.data || []
    } catch (error) {
      console.log('No se pudieron cargar las matrículas:', error)
      recentEnrollments.value = []
    }
    
    // Fetch students for recent students section
    await studentsStore.fetchStudents({ limit: 10 })
    
    // Calculate stats from loaded data
    stats.value = {
      totalStudents: studentsStore.students.length,
      activeCourses: 24, // Mock data
      pendingEnrollments: recentEnrollments.value.filter(e => e.estado === 'pendiente').length,
      todayPayments: 2450 // Mock data
    }
  } catch (error) {
    console.error('Error fetching dashboard data:', error)
    window.notify?.('Error al cargar datos del dashboard', 'error')
  } finally {
    loading.value = false
  }
}

const formatDate = (dateString) => {
  if (!dateString) return ''
  return new Date(dateString).toLocaleDateString('es-ES', {
    day: '2-digit',
    month: '2-digit',
    year: 'numeric'
  })
}

const getStatusClass = (status) => {
  const classes = {
    'activo': 'px-2 py-1 text-xs font-medium rounded-full bg-green-100 text-green-800',
    'pagado': 'px-2 py-1 text-xs font-medium rounded-full bg-green-100 text-green-800',
    'pendiente': 'px-2 py-1 text-xs font-medium rounded-full bg-yellow-100 text-yellow-800',
    'anulado': 'px-2 py-1 text-xs font-medium rounded-full bg-red-100 text-red-800',
    'egresado': 'px-2 py-1 text-xs font-medium rounded-full bg-blue-100 text-blue-800',
    'retirado': 'px-2 py-1 text-xs font-medium rounded-full bg-gray-100 text-gray-800',
    'suspendido': 'px-2 py-1 text-xs font-medium rounded-full bg-red-100 text-red-800'
  }
  return classes[status] || 'px-2 py-1 text-xs font-medium rounded-full bg-gray-100 text-gray-800'
}

onMounted(() => {
  fetchDashboardData()
})
</script>