import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'HomePage',
      component: () => import('../views/HomePage.vue')
    },
    {
      path: '/new-quiz',
      name: 'NewQuizPage',
      component: () => import('../views/NewQuizPage.vue')
    },
    {
      path: '/quiz',
      name: 'QuizPage',
      component: () => import('../views/QuizPage.vue')
    },
    {
      path: '/quiz-results',
      name: 'QuizResultsPage',
      component: () => import('../views/QuizResultsPage.vue')
    },
    {
      path: '/admin',
      name: 'AdminPage',
      component: () => import('../views/AdminPage.vue')
    },
    {
      path: '/edit-quiz',
      name: 'EditQuizPage',
      component: () => import('../views/EditQuizPage.vue')
    }
  ]
})

export default router
