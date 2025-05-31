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