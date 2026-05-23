import { createRouter, createWebHistory } from 'vue-router'
import { useUserStore } from '../stores/user'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: () => import('../views/Home.vue'),
    },
    {
      path: '/market',
      name: 'market',
      component: () => import('../views/Market.vue'),
    },
    {
      path: '/ride/:id',
      name: 'ride-detail',
      component: () => import('../views/RideDetail.vue'),
    },
    {
      path: '/create',
      name: 'create-ride',
      component: () => import('../views/CreateRide.vue'),
      meta: { requiresAuth: true },
    },
    {
      path: '/profile',
      name: 'profile',
      component: () => import('../views/Profile.vue'),
      meta: { requiresAuth: true },
    },
    {
      path: '/products',
      name: 'products',
      component: () => import('../views/ProductAdmin.vue'),
      meta: { requiresAuth: true, requiresAdmin: true },
    },
    {
      path: '/login',
      name: 'login',
      component: () => import('../views/Login.vue'),
    },
  ],
})

router.beforeEach(async (to, from, next) => {
  const userStore = useUserStore()
  
  // Try to load user profile on startup if token is available
  if (userStore.token && !userStore.user) {
    await userStore.init()
  }
  
  if (to.meta.requiresAuth && !userStore.isLoggedIn) {
    next({ path: '/login', query: { redirect: to.fullPath } })
  } else if (to.meta.requiresAdmin && !userStore.isAdmin) {
    next('/')
  } else if (to.name === 'login' && userStore.isLoggedIn) {
    next('/')
  } else {
    next()
  }
})

export default router
