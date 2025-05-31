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
      students.value = response.data.data
    } catch (err) {
      error.value = err.response?.data?.message || 'Error al cargar estudiantes'
    } finally {
      loading.value = false
    }
  }

  const createStudent = async (studentData) => {
    loading.value = true
    error.value = null
    try {
      const response = await studentsAPI.create(studentData)
      students.value.push(response.data.data)
      return { success: true }
    } catch (err) {
      error.value = err.response?.data?.message || 'Error al crear estudiante'
      return { success: false, message: error.value }
    } finally {
      loading.value = false
    }
  }

  const updateStudent = async (id, studentData) => {
    loading.value = true
    error.value = null
    try {
      const response = await studentsAPI.update(id, studentData)
      const index = students.value.findIndex(s => s.id === id)
      if (index !== -1) {
        students.value[index] = response.data.data
      }
      return { success: true }
    } catch (err) {
      error.value = err.response?.data?.message || 'Error al actualizar estudiante'
      return { success: false, message: error.value }
    } finally {
      loading.value = false
    }
  }

  const updateStudentStatus = async (id, status) => {
    try {
      await studentsAPI.updateStatus(id, status)
      const student = students.value.find(s => s.id === id)
      if (student) {
        student.estado = status
      }
      return { success: true }
    } catch (err) {
      return { 
        success: false, 
        message: err.response?.data?.message || 'Error al actualizar estado' 
      }
    }
  }

  const fetchSchools = async () => {
    try {
      const response = await schoolsAPI.getAll()
      schools.value = response.data.data
    } catch (err) {
      console.error('Error al cargar escuelas:', err)
    }
  }

  const fetchStudyPlans = async (schoolId) => {
    try {
      const response = await studyPlansAPI.getBySchool(schoolId)
      studyPlans.value = response.data.data
    } catch (err) {
      console.error('Error al cargar planes de estudio:', err)
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