import { createRouter, createWebHistory } from 'vue-router'
import QuizApiService from '@/services/QuizApiService'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'Home',
      component: () => import('../views/home/HomePage.vue')
    },
    {
      path: '/quiz',
      name: 'Quiz',
      component: () => import('../views/home/QuizPage.vue')
    },
    {
      path: '/results',
      name: 'Results',
      component: () => import('../views/home/ResultsPage.vue')
    },
    {
      path: '/admin',
      name: 'Admin',
      component: () => import('../views/admin/AdminPage.vue'),
      beforeEnter: (to, from, next) => {
        if (QuizApiService.authenticated()) {
          next()
        } else {
          next('/')
        }
      }
    }
  ]
})

export default router
