import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/login',
      name: 'Login',
      component: () => import('@/views/LoginView.vue'),
      meta: { requiresGuest: true }
    },
    {
      path: '/',
      name: 'Dashboard',
      component: () => import('@/views/DashboardView.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/students',
      name: 'Students',
      component: () => import('@/views/StudentsView.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/courses',
      name: 'Courses',
      component: () => import('@/views/CoursesView.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/enrollment',
      name: 'Enrollment',
      component: () => import('@/views/EnrollmentView.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/payments',
      name: 'Payments',
      component: () => import('@/views/PaymentsView.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/faculties',
      name: 'Faculties',
      component: () => import('@/views/FacultiesView.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/schools',
      name: 'Schools',
      component: () => import('@/views/SchoolsView.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/study-plans',
      name: 'StudyPlans',
      component: () => import('@/views/StudyPlansView.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/teachers',
      name: 'Teachers',
      component: () => import('@/views/TeachersView.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/academic-periods',
      name: 'AcademicPeriods',
      component: () => import('@/views/AcademicPeriodsView.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/sections',
      name: 'Sections',
      component: () => import('@/views/SectionsView.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/schedules',
      name: 'Schedules',
      component: () => import('@/views/SchedulesView.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/prerequisites',
      name: 'Prerequisites',
      component: () => import('@/views/PrerequisitesView.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/configurations',
      name: 'Configurations',
      component: () => import('@/views/ConfigurationsView.vue'),
      meta: { requiresAuth: true }
    }
  ]
})

router.beforeEach(async (to, from, next) => {
  const authStore = useAuthStore()
  
  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    next('/login')
  } else if (to.meta.requiresGuest && authStore.isAuthenticated) {
    next('/')
  } else {
    next()
  }
})

export default router