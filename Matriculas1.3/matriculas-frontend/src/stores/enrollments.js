import { defineStore } from 'pinia'
import { ref } from 'vue'
import { enrollmentAPI, studentsAPI, academicPeriodsAPI } from '@/services/api'

export const useEnrollmentStore = defineStore('enrollment', () => {
  const enrollments = ref([])
  const students = ref([])
  const academicPeriods = ref([])
  const loading = ref(false)
  const error = ref(null)

  const fetchEnrollments = async (params = {}) => {
    loading.value = true
    error.value = null
    try {
      const response = await enrollmentAPI.getAll(params)
      enrollments.value = response.data.data || []
      console.log('Matrículas cargadas:', enrollments.value)
    } catch (err) {
      error.value = err.response?.data?.message || 'Error al cargar matrículas'
      console.error('Error al cargar matrículas:', err)
      window.notify?.('Error al cargar matrículas', 'error')
    } finally {
      loading.value = false
    }
  }

  const fetchStudents = async () => {
    try {
      console.log('Cargando estudiantes...')
      const response = await studentsAPI.getAll()
      students.value = response.data.data || []
      console.log('Estudiantes cargados:', students.value)
    } catch (err) {
      console.error('Error al cargar estudiantes:', err)
      window.notify?.('Error al cargar estudiantes', 'error')
    }
  }

  const fetchAcademicPeriods = async () => {
    try {
      console.log('Cargando periodos académicos...')
      const response = await academicPeriodsAPI.getAll()
      academicPeriods.value = response.data.data || []
      console.log('Periodos académicos cargados:', academicPeriods.value)
    } catch (err) {
      console.error('Error al cargar periodos académicos:', err)
      window.notify?.('Error al cargar periodos académicos', 'error')
    }
  }

  const createEnrollment = async (enrollmentData) => {
    loading.value = true
    error.value = null
    try {
      console.log('Creando matrícula:', enrollmentData)
      const response = await enrollmentAPI.create(enrollmentData)
      const newEnrollment = response.data.data
      enrollments.value.unshift(newEnrollment.matricula)
      console.log('Matrícula creada:', newEnrollment)
      return { success: true, data: newEnrollment }
    } catch (err) {
      error.value = err.response?.data?.message || 'Error al crear matrícula'
      console.error('Error al crear matrícula:', err)
      return { success: false, message: error.value }
    } finally {
      loading.value = false
    }
  }

  const updateEnrollmentStatus = async (id, status) => {
    try {
      console.log('Actualizando estado de matrícula:', id, status)
      await enrollmentAPI.updateStatus(id, status)
      const enrollment = enrollments.value.find(e => e.id === id)
      if (enrollment) {
        enrollment.estado = status
      }
      return { success: true }
    } catch (err) {
      const message = err.response?.data?.message || 'Error al actualizar estado'
      console.error('Error al actualizar estado:', err)
      return { success: false, message }
    }
  }

  const cancelEnrollment = async (id) => {
    try {
      console.log('Anulando matrícula:', id)
      await enrollmentAPI.cancel(id)
      const enrollment = enrollments.value.find(e => e.id === id)
      if (enrollment) {
        enrollment.estado = 'anulado'
      }
      return { success: true }
    } catch (err) {
      const message = err.response?.data?.message || 'Error al anular matrícula'
      console.error('Error al anular matrícula:', err)
      return { success: false, message }
    }
  }

  return {
    enrollments,
    students,
    academicPeriods,
    loading,
    error,
    fetchEnrollments,
    fetchStudents,
    fetchAcademicPeriods,
    createEnrollment,
    updateEnrollmentStatus,
    cancelEnrollment
  }
})