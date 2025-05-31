import { defineStore } from 'pinia'
import { ref } from 'vue'
import { studentsAPI, schoolsAPI, studyPlansAPI } from '@/services/api'

export const useStudentsStore = defineStore('students', () => {
  const students = ref([])
  const schools = ref([])
  const studyPlans = ref([])
  const loading = ref(false)
  const error = ref(null)

  const fetchStudents = async (params = {}) => {
    loading.value = true
    error.value = null
    try {
      const response = await studentsAPI.getAll(params)
      students.value = response.data.data || []
      console.log('Estudiantes cargados:', students.value)
    } catch (err) {
      error.value = err.response?.data?.message || 'Error al cargar estudiantes'
      console.error('Error al cargar estudiantes:', err)
      window.notify?.('Error al cargar estudiantes', 'error')
    } finally {
      loading.value = false
    }
  }

  const createStudent = async (studentData) => {
    loading.value = true
    error.value = null
    try {
      console.log('Creando estudiante:', studentData)
      const response = await studentsAPI.create(studentData)
      const newStudent = response.data.data
      students.value.unshift(newStudent)
      console.log('Estudiante creado:', newStudent)
      return { success: true, data: newStudent }
    } catch (err) {
      error.value = err.response?.data?.message || 'Error al crear estudiante'
      console.error('Error al crear estudiante:', err)
      return { success: false, message: error.value }
    } finally {
      loading.value = false
    }
  }

  const updateStudent = async (id, studentData) => {
    loading.value = true
    error.value = null
    try {
      console.log('Actualizando estudiante:', id, studentData)
      const response = await studentsAPI.update(id, studentData)
      const updatedStudent = response.data.data
      const index = students.value.findIndex(s => s.id === id)
      if (index !== -1) {
        students.value[index] = updatedStudent
      }
      console.log('Estudiante actualizado:', updatedStudent)
      return { success: true, data: updatedStudent }
    } catch (err) {
      error.value = err.response?.data?.message || 'Error al actualizar estudiante'
      console.error('Error al actualizar estudiante:', err)
      return { success: false, message: error.value }
    } finally {
      loading.value = false
    }
  }

  const updateStudentStatus = async (id, status) => {
    try {
      console.log('Actualizando estado del estudiante:', id, status)
      await studentsAPI.updateStatus(id, status)
      const student = students.value.find(s => s.id === id)
      if (student) {
        student.estado = status
      }
      return { success: true }
    } catch (err) {
      const message = err.response?.data?.message || 'Error al actualizar estado'
      console.error('Error al actualizar estado:', err)
      return { success: false, message }
    }
  }

  const fetchSchools = async () => {
    try {
      console.log('Cargando escuelas...')
      const response = await schoolsAPI.getAll()
      schools.value = response.data.data || []
      console.log('Escuelas cargadas:', schools.value)
    } catch (err) {
      console.error('Error al cargar escuelas:', err)
      window.notify?.('Error al cargar escuelas', 'error')
    }
  }

  const fetchStudyPlans = async (schoolId) => {
    try {
      console.log('Cargando planes de estudio para escuela:', schoolId)
      const response = await studyPlansAPI.getBySchool(schoolId)
      studyPlans.value = response.data.data || []
      console.log('Planes de estudio cargados:', studyPlans.value)
    } catch (err) {
      console.error('Error al cargar planes de estudio:', err)
      window.notify?.('Error al cargar planes de estudio', 'error')
    }
  }

  return {
    students,
    schools,
    studyPlans,
    loading,
    error,
    fetchStudents,
    createStudent,
    updateStudent,
    updateStudentStatus,
    fetchSchools,
    fetchStudyPlans
  }
})