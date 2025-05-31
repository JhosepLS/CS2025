<template>
  <div class="flex h-screen bg-gray-50">
    <AppSidebar :is-open="sidebarOpen" @close="sidebarOpen = false" />
    
    <div class="flex-1 flex flex-col overflow-hidden">
      <AppHeader @toggle-sidebar="sidebarOpen = !sidebarOpen" />
      
      <main class="flex-1 overflow-x-hidden overflow-y-auto bg-gray-50 p-6">
        <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between mb-6">
          <div>
            <h1 class="text-2xl font-semibold text-gray-900">Matrículas</h1>
            <p class="text-gray-600">Proceso de matrícula de estudiantes</p>
          </div>
          <button
            @click="openCreateModal"
            class="mt-4 sm:mt-0 btn-primary flex items-center space-x-2"
          >
            <Plus class="w-5 h-5" />
            <span>Nueva Matrícula</span>
          </button>
        </div>

        <!-- Error Alert -->
        <div v-if="enrollmentStore.error" class="mb-6 p-4 bg-red-50 border border-red-200 rounded-lg">
          <div class="flex">
            <AlertCircle class="w-5 h-5 text-red-400" />
            <div class="ml-3">
              <p class="text-sm text-red-800">{{ enrollmentStore.error }}</p>
            </div>
            <button @click="enrollmentStore.error = null" class="ml-auto text-red-400 hover:text-red-600">
              <X class="w-4 h-4" />
            </button>
          </div>
        </div>

        <!-- Filters -->
        <div class="card mb-6">
          <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Periodo Académico</label>
              <select v-model="filters.periodoAcademicoId" class="input-field" @change="fetchEnrollments">
                <option value="">Todos los periodos</option>
                <option v-for="periodo in enrollmentStore.academicPeriods" :key="periodo.id" :value="periodo.id">
                  {{ periodo.nombre }}
                </option>
              </select>
            </div>
            
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Estado</label>
              <select v-model="filters.estado" class="input-field" @change="fetchEnrollments">
                <option value="">Todos los estados</option>
                <option value="pendiente">Pendiente</option>
                <option value="pagado">Pagado</option>
                <option value="anulado">Anulado</option>
              </select>
            </div>
            
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Tipo</label>
              <select v-model="filters.tipoMatricula" class="input-field" @change="fetchEnrollments">
                <option value="">Todos los tipos</option>
                <option value="regular">Regular</option>
                <option value="extemporanea">Extemporánea</option>
              </select>
            </div>
            
            <div class="flex items-end">
              <button @click="clearFilters" class="btn-secondary w-full">
                <Filter class="w-4 h-4 mr-2" />
                Limpiar Filtros
              </button>
            </div>
          </div>
        </div>

        <!-- Enrollments List -->
        <div class="card">
          <div v-if="enrollmentStore.loading" class="flex justify-center py-8">
            <LoadingSpinner size="medium" message="Cargando matrículas..." />
          </div>
          
          <div v-else-if="enrollmentStore.enrollments.length === 0" class="text-center py-8">
            <FileText class="w-12 h-12 text-gray-400 mx-auto mb-4" />
            <p class="text-gray-600">No se encontraron matrículas</p>
            <button @click="openCreateModal" class="mt-4 btn-primary">
              Crear primera matrícula
            </button>
          </div>
          
          <div v-else class="table-container">
            <table class="table">
              <thead class="table-header">
                <tr>
                  <th class="table-header-cell">Estudiante</th>
                  <th class="table-header-cell">Periodo</th>
                  <th class="table-header-cell">Fecha</th>
                  <th class="table-header-cell">Tipo</th>
                  <th class="table-header-cell">Créditos</th>
                  <th class="table-header-cell">Monto</th>
                  <th class="table-header-cell">Estado</th>
                  <th class="table-header-cell">Acciones</th>
                </tr>
              </thead>
              <tbody class="table-body">
                <tr v-for="enrollment in enrollmentStore.enrollments" :key="enrollment.id">
                  <td class="table-cell">
                    <div class="flex items-center">
                      <div class="w-10 h-10 bg-primary-100 rounded-full flex items-center justify-center">
                        <User class="w-5 h-5 text-primary-600" />
                      </div>
                      <div class="ml-3">
                        <p class="font-medium text-gray-900">
                          {{ enrollment.alumno?.usuario?.nombre }} {{ enrollment.alumno?.usuario?.apellido }}
                        </p>
                        <p class="text-sm text-gray-600">{{ enrollment.alumno?.codigo }}</p>
                      </div>
                    </div>
                  </td>
                  <td class="table-cell">
                    <p>{{ enrollment.periodoAcademico?.nombre }}</p>
                    <p class="text-sm text-gray-600">{{ enrollment.periodoAcademico?.codigo }}</p>
                  </td>
                  <td class="table-cell">
                    <p>{{ formatDate(enrollment.fechaMatricula) }}</p>
                  </td>
                  <td class="table-cell">
                    <span 
                      :class="[
                        'px-2 py-1 text-xs font-medium rounded-full',
                        enrollment.tipoMatricula === 'regular' ? 'bg-blue-100 text-blue-800' : 'bg-orange-100 text-orange-800'
                      ]"
                    >
                      {{ enrollment.tipoMatricula }}
                    </span>
                  </td>
                  <td class="table-cell">
                    <span class="font-medium">{{ enrollment.creditosInscritos }}</span>
                  </td>
                  <td class="table-cell">
                    <span class="font-medium">S/. {{ enrollment.montoTotal }}</span>
                  </td>
                  <td class="table-cell">
                    <span 
                      :class="[
                        'px-2 py-1 text-xs font-medium rounded-full',
                        {
                          'bg-yellow-100 text-yellow-800': enrollment.estado === 'pendiente',
                          'bg-green-100 text-green-800': enrollment.estado === 'pagado',
                          'bg-red-100 text-red-800': enrollment.estado === 'anulado'
                        }
                      ]"
                    >
                      {{ enrollment.estado }}
                    </span>
                  </td>
                  <td class="table-cell">
                    <div class="flex space-x-2">
                      <button
                        @click="viewEnrollment(enrollment)"
                        class="text-blue-600 hover:text-blue-900"
                        title="Ver detalles"
                      >
                        <Eye class="w-4 h-4" />
                      </button>
                      <button
                        v-if="enrollment.estado !== 'anulado'"
                        @click="updateStatus(enrollment)"
                        class="text-green-600 hover:text-green-900"
                        title="Cambiar estado"
                      >
                        <Edit class="w-4 h-4" />
                      </button>
                    </div>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <!-- Create Modal -->
        <EnrollmentModal
          v-if="showCreateModal"
          :is-open="showCreateModal"
          :students="enrollmentStore.students"
          :academic-periods="enrollmentStore.academicPeriods"
          @close="closeModal"
          @save="handleSaveEnrollment"
        />
      </main>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useEnrollmentStore } from '@/stores/enrollment'
import AppHeader from '@/components/common/AppHeader.vue'
import AppSidebar from '@/components/common/AppSidebar.vue'
import LoadingSpinner from '@/components/common/LoadingSpinner.vue'
import EnrollmentModal from '@/components/enrollment/EnrollmentModal.vue'
import { 
  Plus, Filter, FileText, User, Eye, Edit, AlertCircle, X 
} from 'lucide-vue-next'

const enrollmentStore = useEnrollmentStore()

const sidebarOpen = ref(false)
const showCreateModal = ref(false)

const filters = ref({
  periodoAcademicoId: '',
  estado: '',
  tipoMatricula: ''
})

const fetchEnrollments = async () => {
  const params = {}
  if (filters.value.periodoAcademicoId) params.periodoAcademicoId = filters.value.periodoAcademicoId
  if (filters.value.estado) params.estado = filters.value.estado
  if (filters.value.tipoMatricula) params.tipoMatricula = filters.value.tipoMatricula
  
  await enrollmentStore.fetchEnrollments(params)
}

const clearFilters = () => {
  filters.value = {
    periodoAcademicoId: '',
    estado: '',
    tipoMatricula: ''
  }
  fetchEnrollments()
}

const openCreateModal = async () => {
  showCreateModal.value = true
  await enrollmentStore.fetchStudents()
  await enrollmentStore.fetchAcademicPeriods()
}

const closeModal = () => {
  showCreateModal.value = false
}

const handleSaveEnrollment = async (enrollmentData) => {
  try {
    const result = await enrollmentStore.createEnrollment(enrollmentData)

    if (result.success) {
      window.notify?.('Matrícula creada exitosamente', 'success')
      closeModal()
      await fetchEnrollments()
    } else {
      window.notify?.(result.message || 'Error al crear matrícula', 'error')
    }
  } catch (error) {
    console.error('Error al crear matrícula:', error)
    window.notify?.('Error al crear matrícula', 'error')
  }
}

const viewEnrollment = (enrollment) => {
  console.log('Ver matrícula:', enrollment)
  window.notify?.(`Viendo detalles de matrícula ${enrollment.id}`, 'info')
}

const updateStatus = async (enrollment) => {
  const newStatus = enrollment.estado === 'pendiente' ? 'pagado' : 'pendiente'
  try {
    const result = await enrollmentStore.updateEnrollmentStatus(enrollment.id, newStatus)
    if (result.success) {
      window.notify?.(`Estado actualizado a ${newStatus}`, 'success')
      await fetchEnrollments()
    } else {
      window.notify?.(result.message || 'Error al actualizar estado', 'error')
    }
  } catch (error) {
    console.error('Error al actualizar estado:', error)
    window.notify?.('Error al actualizar estado', 'error')
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

onMounted(async () => {
  await enrollmentStore.fetchAcademicPeriods()
  await fetchEnrollments()
})
</script>