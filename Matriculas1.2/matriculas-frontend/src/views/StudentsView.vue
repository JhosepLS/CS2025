<template>
  <div class="flex h-screen bg-gray-50">
    <AppSidebar :is-open="sidebarOpen" @close="sidebarOpen = false" />
    
    <div class="flex-1 flex flex-col overflow-hidden">
      <AppHeader @toggle-sidebar="sidebarOpen = !sidebarOpen" />
      
      <main class="flex-1 overflow-x-hidden overflow-y-auto bg-gray-50 p-6">
        <!-- Header Actions -->
        <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between mb-6">
          <div>
            <h1 class="text-2xl font-semibold text-gray-900">Estudiantes</h1>
            <p class="text-gray-600">Gestiona los estudiantes del sistema</p>
          </div>
          <button
            @click="openCreateModal"
            class="mt-4 sm:mt-0 btn-primary flex items-center space-x-2"
          >
            <Plus class="w-5 h-5" />
            <span>Nuevo Estudiante</span>
          </button>
        </div>

        <!-- Error Alert -->
        <div v-if="studentsStore.error" class="mb-6 p-4 bg-red-50 border border-red-200 rounded-lg">
          <div class="flex">
            <AlertCircle class="w-5 h-5 text-red-400" />
            <div class="ml-3">
              <p class="text-sm text-red-800">{{ studentsStore.error }}</p>
            </div>
            <button @click="studentsStore.error = null" class="ml-auto text-red-400 hover:text-red-600">
              <X class="w-4 h-4" />
            </button>
          </div>
        </div>

        <!-- Filters -->
        <div class="card mb-6">
          <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Buscar</label>
              <div class="relative">
                <input
                  v-model="filters.search"
                  type="text"
                  placeholder="Nombre, código o DNI..."
                  class="input-field pl-10"
                  @input="debouncedSearch"
                />
                <Search class="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400" />
              </div>
            </div>
            
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Escuela</label>
              <select v-model="filters.escuelaId" class="input-field" @change="fetchStudents">
                <option value="">Todas las escuelas</option>
                <option v-for="school in studentsStore.schools" :key="school.id" :value="school.id">
                  {{ school.nombre }}
                </option>
              </select>
            </div>
            
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Estado</label>
              <select v-model="filters.estado" class="input-field" @change="fetchStudents">
                <option value="">Todos los estados</option>
                <option value="activo">Activo</option>
                <option value="egresado">Egresado</option>
                <option value="retirado">Retirado</option>
                <option value="suspendido">Suspendido</option>
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

        <!-- Students List -->
        <div class="card">
          <div v-if="studentsStore.loading" class="flex justify-center py-8">
            <LoadingSpinner size="medium" message="Cargando estudiantes..." />
          </div>
          
          <div v-else-if="studentsStore.students.length === 0" class="text-center py-8">
            <Users class="w-12 h-12 text-gray-400 mx-auto mb-4" />
            <p class="text-gray-600">No se encontraron estudiantes</p>
            <button @click="openCreateModal" class="mt-4 btn-primary">
              Crear primer estudiante
            </button>
          </div>
          
          <div v-else class="table-container">
            <table class="table">
              <thead class="table-header">
                <tr>
                  <th class="table-header-cell">Estudiante</th>
                  <th class="table-header-cell">Código/DNI</th>
                  <th class="table-header-cell">Escuela</th>
                  <th class="table-header-cell">Ciclo</th>
                  <th class="table-header-cell">Estado</th>
                  <th class="table-header-cell">Acciones</th>
                </tr>
              </thead>
              <tbody class="table-body">
                <tr v-for="student in studentsStore.students" :key="student.id">
                  <td class="table-cell">
                    <div class="flex items-center">
                      <div class="w-10 h-10 bg-primary-100 rounded-full flex items-center justify-center">
                        <User class="w-5 h-5 text-primary-600" />
                      </div>
                      <div class="ml-3">
                        <p class="font-medium text-gray-900">
                          {{ student.usuario?.nombre }} {{ student.usuario?.apellido }}
                        </p>
                        <p class="text-sm text-gray-600">{{ student.usuario?.email }}</p>
                      </div>
                    </div>
                  </td>
                  <td class="table-cell">
                    <div>
                      <p class="font-medium">{{ student.codigo }}</p>
                      <p class="text-sm text-gray-600">{{ student.dni }}</p>
                    </div>
                  </td>
                  <td class="table-cell">
                    <p>{{ student.escuela?.nombre }}</p>
                    <p class="text-sm text-gray-600">{{ student.escuela?.codigo }}</p>
                  </td>
                  <td class="table-cell">
                    <span class="font-medium">{{ student.cicloActual }}</span>
                  </td>
                  <td class="table-cell">
                    <span 
                      :class="[
                        'px-2 py-1 text-xs font-medium rounded-full',
                        {
                          'bg-green-100 text-green-800': student.estado === 'activo',
                          'bg-blue-100 text-blue-800': student.estado === 'egresado',
                          'bg-red-100 text-red-800': student.estado === 'retirado',
                          'bg-yellow-100 text-yellow-800': student.estado === 'suspendido'
                        }
                      ]"
                    >
                      {{ student.estado }}
                    </span>
                  </td>
                  <td class="table-cell">
                    <div class="flex space-x-2">
                      <button
                        @click="editStudent(student)"
                        class="text-blue-600 hover:text-blue-900"
                        title="Editar"
                      >
                        <Edit class="w-4 h-4" />
                      </button>
                      <button
                        @click="viewStudent(student)"
                        class="text-green-600 hover:text-green-900"
                        title="Ver detalles"
                      >
                        <Eye class="w-4 h-4" />
                      </button>
                    </div>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <!-- Create/Edit Modal -->
        <StudentModal
          v-if="showCreateModal || showEditModal"
          :is-open="showCreateModal || showEditModal"
          :student="selectedStudent"
          :schools="studentsStore.schools"
          :study-plans="studentsStore.studyPlans"
          @close="closeModal"
          @save="handleSaveStudent"
          @school-change="handleSchoolChange"
        />
      </main>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useStudentsStore } from '@/stores/students'
import AppHeader from '@/components/common/AppHeader.vue'
import AppSidebar from '@/components/common/AppSidebar.vue'
import LoadingSpinner from '@/components/common/LoadingSpinner.vue'
import StudentModal from '@/components/students/StudentModal.vue'
import { 
  Plus, Search, Filter, Users, User, Edit, Eye, AlertCircle, X 
} from 'lucide-vue-next'

const studentsStore = useStudentsStore()

const sidebarOpen = ref(false)
const showCreateModal = ref(false)
const showEditModal = ref(false)
const selectedStudent = ref(null)

const filters = ref({
  search: '',
  escuelaId: '',
  estado: ''
})

let searchTimeout = null

const debouncedSearch = () => {
  clearTimeout(searchTimeout)
  searchTimeout = setTimeout(() => {
    fetchStudents()
  }, 500)
}

const fetchStudents = async () => {
  const params = {}
  if (filters.value.search) params.search = filters.value.search
  if (filters.value.escuelaId) params.escuelaId = filters.value.escuelaId
  if (filters.value.estado) params.estado = filters.value.estado
  
  await studentsStore.fetchStudents(params)
}

const clearFilters = () => {
  filters.value = {
    search: '',
    escuelaId: '',
    estado: ''
  }
  fetchStudents()
}

const openCreateModal = async () => {
  selectedStudent.value = null
  showCreateModal.value = true
  // Asegurar que las escuelas están cargadas
  if (studentsStore.schools.length === 0) {
    await studentsStore.fetchSchools()
  }
}

const editStudent = async (student) => {
  selectedStudent.value = student
  showEditModal.value = true
  // Cargar escuelas y planes de estudio si es necesario
  if (studentsStore.schools.length === 0) {
    await studentsStore.fetchSchools()
  }
  if (student.escuelaId) {
    await studentsStore.fetchStudyPlans(student.escuelaId)
  }
}

const viewStudent = (student) => {
  console.log('Ver estudiante:', student)
  // Aquí podrías abrir un modal de detalles o navegar a una página de detalles
  window.notify?.(`Viendo detalles de ${student.usuario?.nombre} ${student.usuario?.apellido}`, 'info')
}

const closeModal = () => {
  showCreateModal.value = false
  showEditModal.value = false
  selectedStudent.value = null
}

const handleSaveStudent = async (studentData) => {
  try {
    let result
    if (selectedStudent.value) {
      // Editar estudiante existente
      result = await studentsStore.updateStudent(selectedStudent.value.id, studentData)
    } else {
      // Crear nuevo estudiante
      result = await studentsStore.createStudent(studentData)
    }

    if (result.success) {
      window.notify?.(
        selectedStudent.value ? 'Estudiante actualizado exitosamente' : 'Estudiante creado exitosamente', 
        'success'
      )
      closeModal()
      // Recargar la lista
      await fetchStudents()
    } else {
      window.notify?.(result.message || 'Error al guardar estudiante', 'error')
    }
  } catch (error) {
    console.error('Error al guardar estudiante:', error)
    window.notify?.('Error al guardar estudiante', 'error')
  }
}

const handleSchoolChange = async (schoolId) => {
  if (schoolId) {
    await studentsStore.fetchStudyPlans(schoolId)
  }
}

onMounted(async () => {
  console.log('Iniciando carga de datos...')
  await studentsStore.fetchSchools()
  await fetchStudents()
})
</script>