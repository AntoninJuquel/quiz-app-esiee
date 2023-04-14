import { createRouter, createWebHistory } from 'vue-router'
import HomePage from '@/views/HomePage.vue'
import NewQuizPage from '@/views/NewQuizPage.vue'
import QuestionsPage from '@/views/QuestionsPage.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'HomePage',
      component: HomePage
    },
    {
      path: '/about',
      name: 'about',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import('../views/AboutView.vue')
    },
    {
      path: '/start-new-quiz-page',
      name: 'StartNewQuizPage',
      component: NewQuizPage
    },
    {
      path: '/questions',
      name: 'QuestionsPage',
      component: QuestionsPage
    }
  ]
})

export default router
