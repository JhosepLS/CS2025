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
    console.log('API Request:', config.method?.toUpperCase(), config.url, config.data)
    return config
  },
  (error) => {
    console.error('API Request Error:', error)
    return Promise.reject(error)
  }
)

// Response interceptor
api.interceptors.response.use(
  (response) => {
    console.log('API Response:', response.config.method?.toUpperCase(), response.config.url, response.status, response.data)
    return response
  },
  (error) => {
    console.error('API Response Error:', error.response?.status, error.response?.data)
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
  delete: (id) => api.delete(`/facultades/${id}`),
}

// Schools API
export const schoolsAPI = {
  getAll: (params) => api.get('/escuelas', { params }),
  getByFaculty: (facultyId) => api.get(`/escuelas/facultad/${facultyId}`),
  getById: (id) => api.get(`/escuelas/${id}`),
  create: (data) => api.post('/escuelas', data),
  update: (id, data) => api.put(`/escuelas/${id}`, data),
  delete: (id) => api.delete(`/escuelas/${id}`),
}

// Study Plans API
export const studyPlansAPI = {
  getAll: (params) => api.get('/planes-estudio', { params }),
  getBySchool: (schoolId) => api.get(`/planes-estudio/escuela/${schoolId}`),
  getById: (id) => api.get(`/planes-estudio/${id}`),
  create: (data) => api.post('/planes-estudio', data),
  update: (id, data) => api.put(`/planes-estudio/${id}`, data),
  delete: (id) => api.delete(`/planes-estudio/${id}`),
}

// Academic Periods API
export const academicPeriodsAPI = {
  getAll: (params) => api.get('/periodos-academicos', { params }),
  getCurrent: () => api.get('/periodos-academicos/actual'),
  getById: (id) => api.get(`/periodos-academicos/${id}`),
  create: (data) => api.post('/periodos-academicos', data),
  update: (id, data) => api.put(`/periodos-academicos/${id}`, data),
  updateStatus: (id, status) => api.patch(`/periodos-academicos/${id}/estado`, { estado: status }),
}

// Sections API
export const sectionsAPI = {
  getAll: (params) => api.get('/secciones', { params }),
  getByCourseAndPeriod: (courseId, periodId) => api.get(`/secciones/curso/${courseId}/periodo/${periodId}`),
  getByPeriod: (periodId) => api.get(`/secciones/periodo/${periodId}`),
  getById: (id) => api.get(`/secciones/${id}`),
  create: (data) => api.post('/secciones', data),
  update: (id, data) => api.put(`/secciones/${id}`, data),
  delete: (id) => api.delete(`/secciones/${id}`),
}

// Teachers API
export const teachersAPI = {
  getAll: (params) => api.get('/docentes', { params }),
  getById: (id) => api.get(`/docentes/${id}`),
  create: (data) => api.post('/docentes', data),
  update: (id, data) => api.put(`/docentes/${id}`, data),
  delete: (id) => api.delete(`/docentes/${id}`),
}

// Schedules API
export const schedulesAPI = {
  getAll: (params) => api.get('/horarios', { params }),
  getBySection: (sectionId) => api.get(`/horarios/seccion/${sectionId}`),
  getById: (id) => api.get(`/horarios/${id}`),
  create: (data) => api.post('/horarios', data),
  update: (id, data) => api.put(`/horarios/${id}`, data),
  delete: (id) => api.delete(`/horarios/${id}`),
}

// Prerequisites API
export const prerequisitesAPI = {
  getAll: () => api.get('/prerequisitos'),
  getByCourse: (courseId) => api.get(`/prerequisitos/curso/${courseId}`),
  getByPrerequisite: (prerequisiteId) => api.get(`/prerequisitos/prerequisito/${prerequisiteId}`),
  create: (data) => api.post('/prerequisitos', data),
  update: (id, data) => api.put(`/prerequisitos/${id}`, data),
  delete: (id) => api.delete(`/prerequisitos/${id}`),
}

// Configurations API
export const configurationsAPI = {
  getAll: () => api.get('/configuraciones'),
  getByName: (name) => api.get(`/configuraciones/${name}`),
  create: (data) => api.post('/configuraciones', data),
  update: (name, data) => api.put(`/configuraciones/${name}`, data),
  delete: (name) => api.delete(`/configuraciones/${name}`),
}