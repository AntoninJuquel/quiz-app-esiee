import { createRouter, createWebHistory } from 'vue-router'
import QuizApiService from '@/services/QuizApiService'

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
      component: () => import('../views/admin/AdminPage.vue'),
      beforeEnter: (to, from, next) => {
        if (!QuizApiService.authenticated() && to.name !== 'AdminLoginPage') {
          next({ name: 'AdminLoginPage' })
        } else {
          next()
        }
      },
      children: [
        {
          path: 'login',
          name: 'AdminLoginPage',
          component: () => import('../views/admin/AdminLoginPage.vue'),
        },
        {
          path: 'questions/:id',
          name: 'AdminEditQuestionPage',
          component: () => import('../views/admin/AdminEditQuestionPage.vue'),
          props: true
        },
        {
          path: 'questions/new',
          name: 'AdminQuestionsNewPage',
          component: () => import('../views/admin/AdminNewQuestionPage.vue'),
        },
        {
          path: 'scoreboard',
          name: 'AdminScoreboardPage',
          component: () => import('../views/admin/AdminScoreboardPage.vue'),
        },
      ]
    }
  ]
})

export default router
