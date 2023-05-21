import { createRouter, createWebHistory } from 'vue-router'

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
      component: () => import('../views/admin/AdminPage.vue')
    }
  ]
})

export default router
