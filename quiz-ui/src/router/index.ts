import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'HomePage',
      component: () => import('../views/user/HomePage.vue')
    },
    {
      path: '/new-quiz',
      name: 'NewQuizPage',
      component: () => import('../views/user/NewQuizPage.vue')
    },
    {
      path: '/quiz',
      name: 'QuizPage',
      component: () => import('../views/user/QuizPage.vue')
    },
    {
      path: '/quiz-results',
      name: 'QuizResultsPage',
      component: () => import('../views/user/QuizResultsPage.vue')
    },
    {
      path: '/admin',
      name: 'AdminPage',
      component: () => import('../views/admin/AdminPage.vue')
    },
    {
      path: '/edit-quiz',
      name: 'EditQuizPage',
      component: () => import('../views/admin/EditQuizPage.vue')
    }
  ]
})

export default router
