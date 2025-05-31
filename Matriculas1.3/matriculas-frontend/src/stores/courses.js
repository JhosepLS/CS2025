import { defineStore } from 'pinia'
import { ref } from 'vue'
import { coursesAPI, studyPlansAPI } from '@/services/api'

export const useCoursesStore = defineStore('courses', () => {
  const courses = ref([])
  const studyPlans = ref([])
  const loading = ref(false)
  const error = ref(null)

  const fetchCourses = async (params = {}) => {
    loading.value = true
    error.value = null
    try {
      const response = await coursesAPI.getAll(params)
      courses.value = response.data.data || []
      console.log('Cursos cargados:', courses.value)
    } catch (err) {
      error.value = err.response?.data?.message || 'Error al cargar cursos'
      console.error('Error al cargar cursos:', err)
      window.notify?.('Error al cargar cursos', 'error')
    } finally {
      loading.value = false
    }
  }

  const fetchStudyPlans = async () => {
    try {
      console.log('Cargando planes de estudio...')
      const response = await studyPlansAPI.getAll()
      studyPlans.value = response.data.data || []
      console.log('Planes de estudio cargados:', studyPlans.value)
    } catch (err) {
      console.error('Error al cargar planes de estudio:', err)
      window.notify?.('Error al cargar planes de estudio', 'error')
    }
  }

  const createCourse = async (courseData) => {
    loading.value = true
    error.value = null
    try {
      console.log('Creando curso:', courseData)
      const response = await coursesAPI.create(courseData)
      const newCourse = response.data.data
      courses.value.unshift(newCourse)
      console.log('Curso creado:', newCourse)
      return { success: true, data: newCourse }
    } catch (err) {
      error.value = err.response?.data?.message || 'Error al crear curso'
      console.error('Error al crear curso:', err)
      return { success: false, message: error.value }
    } finally {
      loading.value = false
    }
  }

  const updateCourse = async (id, courseData) => {
    loading.value = true
    error.value = null
    try {
      console.log('Actualizando curso:', id, courseData)
      const response = await coursesAPI.update(id, courseData)
      const updatedCourse = response.data.data
      const index = courses.value.findIndex(c => c.id === id)
      if (index !== -1) {
        courses.value[index] = updatedCourse
      }
      console.log('Curso actualizado:', updatedCourse)
      return { success: true, data: updatedCourse }
    } catch (err) {
      error.value = err.response?.data?.message || 'Error al actualizar curso'
      console.error('Error al actualizar curso:', err)
      return { success: false, message: error.value }
    } finally {
      loading.value = false
    }
  }

  const deleteCourse = async (id) => {
    try {
      console.log('Eliminando curso:', id)
      await coursesAPI.delete(id)
      const index = courses.value.findIndex(c => c.id === id)
      if (index !== -1) {
        courses.value[index].activo = false
      }
      return { success: true }
    } catch (err) {
      const message = err.response?.data?.message || 'Error al eliminar curso'
      console.error('Error al eliminar curso:', err)
      return { success: false, message }
    }
  }

  return {
    courses,
    studyPlans,
    loading,
    error,
    fetchCourses,
    fetchStudyPlans,
    createCourse,
    updateCourse,
    deleteCourse
  }
})