import { createRouter, createWebHistory } from 'vue-router'
import HomePage from '@/views/HomePage.vue'
import NewQuizPage from '@/views/NewQuizPage.vue'
import QuestionsPage from '@/views/QuestionsPage.vue'
import ScorePage from '@/views/ScorePage.vue'

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
    ,
    {
      path: '/your-score',
      name: 'ScorePage',
      component: ScorePage
    }
  ]
})

export default router
