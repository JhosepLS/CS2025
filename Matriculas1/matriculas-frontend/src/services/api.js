import axios from 'axios'
import { useAuthStore } from '@/stores/auth'

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:3000/api',
  timeout: 10000,
})

// Request interceptor
api.interceptors.request.use(
  (config) => {
    const authStore = useAuthStore()
    if (authStore.token) {
      config.headers.Authorization = `Bearer ${authStore.token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Response interceptor
api.interceptors.response.use(
  (response) => response,
  (error) => {
    const authStore = useAuthStore()
    if (error.response?.status === 401) {
      authStore.logout()
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

export default api

// Auth API
export const authAPI = {
  login: (credentials) => api.post('/auth/login', credentials),
  register: (userData) => api.post('/auth/register', userData),
  profile: () => api.get('/auth/profile'),
}

// Students API
export const studentsAPI = {
  getAll: (params) => api.get('/alumnos', { params }),
  getById: (id) => api.get(`/alumnos/${id}`),
  create: (data) => api.post('/alumnos', data),
  update: (id, data) => api.put(`/alumnos/${id}`, data),
  updateStatus: (id, status) => api.patch(`/alumnos/${id}/estado`, { estado: status }),
  getEnrollments: (id) => api.get(`/alumnos/${id}/matriculas`),
}

// Courses API
export const coursesAPI = {
  getAll: (params) => api.get('/cursos', { params }),
  getById: (id) => api.get(`/cursos/${id}`),
  create: (data) => api.post('/cursos', data),
  update: (id, data) => api.put(`/cursos/${id}`, data),
  delete: (id) => api.delete(`/cursos/${id}`),
  getByPlan: (planId) => api.get(`/cursos/plan-estudio/${planId}`),
}

// Enrollment API
export const enrollmentAPI = {
  getAll: (params) => api.get('/matriculas', { params }),
  getById: (id) => api.get(`/matriculas/${id}`),
  create: (data) => api.post('/matriculas', data),
  updateStatus: (id, status) => api.patch(`/matriculas/${id}/estado`, { estado: status }),
  cancel: (id) => api.patch(`/matriculas/${id}/anular`),
  getReport: (periodId) => api.get(`/matriculas/reporte/periodo/${periodId}`),
}

// Payments API
export const paymentsAPI = {
  getAll: (params) => api.get('/pagos', { params }),
  getById: (id) => api.get(`/pagos/${id}`),
  create: (data) => api.post('/pagos', data),
  getByEnrollment: (enrollmentId) => api.get(`/pagos/matricula/${enrollmentId}`),
  cancel: (id) => api.patch(`/pagos/${id}/anular`),
}

// Faculties API
export const facultiesAPI = {
  getAll: () => api.get('/facultades'),
  getById: (id) => api.get(`/facultades/${id}`),
  create: (data) => api.post('/facultades', data),
  update: (id, data) => api.put(`/facultades/${id}`, data),
}

// Schools API
export const schoolsAPI = {
  getAll: (params) => api.get('/escuelas', { params }),
  getByFaculty: (facultyId) => api.get(`/escuelas/facultad/${facultyId}`),
  create: (data) => api.post('/escuelas', data),
}

// Study Plans API
export const studyPlansAPI = {
  getAll: (params) => api.get('/planes-estudio', { params }),
  getBySchool: (schoolId) => api.get(`/planes-estudio/escuela/${schoolId}`),
  create: (data) => api.post('/planes-estudio', data),
}

// Academic Periods API
export const academicPeriodsAPI = {
  getAll: (params) => api.get('/periodos-academicos', { params }),
  getCurrent: () => api.get('/periodos-academicos/actual'),
  create: (data) => api.post('/periodos-academicos', data),
}

// Sections API
export const sectionsAPI = {
  getAll: (params) => api.get('/secciones', { params }),
  getByCourseAndPeriod: (courseId, periodId) => api.get(`/secciones/curso/${courseId}/periodo/${periodId}`),
  create: (data) => api.post('/secciones', data),
}