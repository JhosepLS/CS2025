<template>
  <div class="flex h-screen bg-gray-50">
    <AppSidebar :is-open="sidebarOpen" @close="sidebarOpen = false" />
    
    <div class="flex-1 flex flex-col overflow-hidden">
      <AppHeader @toggle-sidebar="sidebarOpen = !sidebarOpen" />
      
      <main class="flex-1 overflow-x-hidden overflow-y-auto bg-gray-50 p-6">
        <!-- Header Actions -->
        <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between mb-6">
          <div>
            <h1 class="text-2xl font-semibold text-gray-900">Cursos</h1>
            <p class="text-gray-600">Gestiona los cursos académicos</p>
          </div>
          <button
            @click="openCreateModal"
            class="mt-4 sm:mt-0 btn-primary flex items-center space-x-2"
          >
            <Plus class="w-5 h-5" />
            <span>Nuevo Curso</span>
          </button>
        </div>

        <!-- Error Alert -->
        <div v-if="coursesStore.error" class="mb-6 p-4 bg-red-50 border border-red-200 rounded-lg">
          <div class="flex">
            <AlertCircle class="w-5 h-5 text-red-400" />
            <div class="ml-3">
              <p class="text-sm text-red-800">{{ coursesStore.error }}</p>
            </div>
            <button @click="coursesStore.error = null" class="ml-auto text-red-400 hover:text-red-600">
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
                  placeholder="Nombre o código del curso..."
                  class="input-field pl-10"
                  @input="debouncedSearch"
                />
                <Search class="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400" />
              </div>
            </div>
            
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Plan de Estudio</label>
              <select v-model="filters.planEstudioId" class="input-field" @change="fetchCourses">
                <option value="">Todos los planes</option>
                <option v-for="plan in coursesStore.studyPlans" :key="plan.id" :value="plan.id">
                  {{ plan.nombre }}
                </option>
              </select>
            </div>
            
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Ciclo</label>
              <select v-model="filters.ciclo" class="input-field" @change="fetchCourses">
                <option value="">Todos los ciclos</option>
                <option v-for="i in 10" :key="i" :value="i">{{ i }}</option>
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

        <!-- Courses List -->
        <div class="card">
          <div v-if="coursesStore.loading" class="flex justify-center py-8">
            <LoadingSpinner size="medium" message="Cargando cursos..." />
          </div>
          
          <div v-else-if="coursesStore.courses.length === 0" class="text-center py-8">
            <BookOpen class="w-12 h-12 text-gray-400 mx-auto mb-4" />
            <p class="text-gray-600">No se encontraron cursos</p>
            <button @click="openCreateModal" class="mt-4 btn-primary">
              Crear primer curso
            </button>
          </div>
          
          <div v-else class="table-container">
            <table class="table">
              <thead class="table-header">
                <tr>
                  <th class="table-header-cell">Curso</th>
                  <th class="table-header-cell">Plan de Estudio</th>
                  <th class="table-header-cell">Ciclo</th>
                  <th class="table-header-cell">Créditos</th>
                  <th class="table-header-cell">Horas</th>
                  <th class="table-header-cell">Tipo</th>
                  <th class="table-header-cell">Acciones</th>
                </tr>
              </thead>
              <tbody class="table-body">
                <tr v-for="course in coursesStore.courses" :key="course.id">
                  <td class="table-cell">
                    <div>
                      <p class="font-medium text-gray-900">{{ course.nombre }}</p>
                      <p class="text-sm text-gray-600">{{ course.codigo }}</p>
                    </div>
                  </td>
                  <td class="table-cell">
                    <p>{{ course.planEstudio?.nombre }}</p>
                    <p class="text-sm text-gray-600">{{ course.planEstudio?.codigo }}</p>
                  </td>
                  <td class="table-cell">
                    <span class="font-medium">{{ course.ciclo }}</span>
                  </td>
                  <td class="table-cell">
                    <span class="font-medium">{{ course.creditos }}</span>
                  </td>
                  <td class="table-cell">
                    <div class="text-sm">
                      <div>Teoría: {{ course.horasTeoricas }}h</div>
                      <div>Práctica: {{ course.horasPracticas }}h</div>
                    </div>
                  </td>
                  <td class="table-cell">
                    <span 
                      :class="[
                        'px-2 py-1 text-xs font-medium rounded-full',
                        course.tipo === 'obligatorio' ? 'bg-blue-100 text-blue-800' : 'bg-green-100 text-green-800'
                      ]"
                    >
                      {{ course.tipo }}
                    </span>
                  </td>
                  <td class="table-cell">
                    <div class="flex space-x-2">
                      <button
                        @click="editCourse(course)"
                        class="text-blue-600 hover:text-blue-900"
                        title="Editar"
                      >
                        <Edit class="w-4 h-4" />
                      </button>
                      <button
                        @click="viewCourse(course)"
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
        <CourseModal
          v-if="showCreateModal || showEditModal"
          :is-open="showCreateModal || showEditModal"
          :course="selectedCourse"
          :study-plans="coursesStore.studyPlans"
          @close="closeModal"
          @save="handleSaveCourse"
        />
      </main>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useCoursesStore } from '@/stores/courses'
import AppHeader from '@/components/common/AppHeader.vue'
import AppSidebar from '@/components/common/AppSidebar.vue'
import LoadingSpinner from '@/components/common/LoadingSpinner.vue'
import CourseModal from '@/components/courses/CourseModal.vue'
import { 
  Plus, Search, Filter, BookOpen, Edit, Eye, AlertCircle, X 
} from 'lucide-vue-next'

const coursesStore = useCoursesStore()

const sidebarOpen = ref(false)
const showCreateModal = ref(false)
const showEditModal = ref(false)
const selectedCourse = ref(null)

const filters = ref({
  search: '',
  planEstudioId: '',
  ciclo: ''
})

let searchTimeout = null

const debouncedSearch = () => {
  clearTimeout(searchTimeout)
  searchTimeout = setTimeout(() => {
    fetchCourses()
  }, 500)
}

const fetchCourses = async () => {
  const params = {}
  if (filters.value.search) params.search = filters.value.search
  if (filters.value.planEstudioId) params.planEstudioId = filters.value.planEstudioId
  if (filters.value.ciclo) params.ciclo = filters.value.ciclo
  
  await coursesStore.fetchCourses(params)
}

const clearFilters = () => {
  filters.value = {
    search: '',
    planEstudioId: '',
    ciclo: ''
  }
  fetchCourses()
}

const openCreateModal = async () => {
  selectedCourse.value = null
  showCreateModal.value = true
  if (coursesStore.studyPlans.length === 0) {
    await coursesStore.fetchStudyPlans()
  }
}

const editCourse = async (course) => {
  selectedCourse.value = course
  showEditModal.value = true
  if (coursesStore.studyPlans.length === 0) {
    await coursesStore.fetchStudyPlans()
  }
}

const viewCourse = (course) => {
  console.log('Ver curso:', course)
  window.notify?.(`Viendo detalles de ${course.nombre}`, 'info')
}

const closeModal = () => {
  showCreateModal.value = false
  showEditModal.value = false
  selectedCourse.value = null
}

const handleSaveCourse = async (courseData) => {
  try {
    let result
    if (selectedCourse.value) {
      result = await coursesStore.updateCourse(selectedCourse.value.id, courseData)
    } else {
      result = await coursesStore.createCourse(courseData)
    }

    if (result.success) {
      window.notify?.(
        selectedCourse.value ? 'Curso actualizado exitosamente' : 'Curso creado exitosamente', 
        'success'
      )
      closeModal()
      await fetchCourses()
    } else {
      window.notify?.(result.message || 'Error al guardar curso', 'error')
    }
  } catch (error) {
    console.error('Error al guardar curso:', error)
    window.notify?.('Error al guardar curso', 'error')
  }
}

onMounted(async () => {
  await coursesStore.fetchStudyPlans()
  await fetchCourses()
})
</script>