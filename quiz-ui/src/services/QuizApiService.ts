import axios, { AxiosError, AxiosHeaders } from 'axios'
import { format } from 'date-fns'
import type { Question, QuizInfo, Answer, Token, Difficulty, Category, Score } from '@/types/quiz'

const MULTIPLE_ANSWERS_ENABLED = false

const instance = axios.create({
  baseURL: `${import.meta.env.VITE_API_URL}`,
  responseType: 'json'
})

export default {
  async call<T>(
    method: string,
    resource: string,
    data?: Record<string, unknown>,
    token?: string
  ): Promise<{ status: number; data: T }> {
    const headers = new AxiosHeaders({
      'Content-Type': 'application/json'
    })

    if (token) {
      headers.set('Authorization', `Bearer ${token}`)
    }

    return instance<T>({
      method,
      headers,
      url: resource,
      data
    })
      .then((response) => {
        return { status: response.status, data: response.data }
      })
      .catch((err: AxiosError) => {
        const error = new Error(err.message)
        error.name = err.name
        throw error
      })
  },
  async getQuizInfo(date: string = format(new Date(), 'yyyy-MM-dd')) {
    return this.call<QuizInfo>('get', `quiz-info?date=${date}`)
  },
  async getQuestions(date: string = format(new Date(), 'yyyy-MM-dd')) {
    return this.call<Question[]>('get', `questions?date=${date}`)
  },
  async getQuestionById(id: number) {
    return this.call<Question>('get', `questions/${id}`)
  },
  async getQuestion(position: number, date: string = format(new Date(), 'yyyy-MM-dd')) {
    return this.call<Question>('get', `questions?position=${position}&date=${date}`)
  },
  async postAnswers(playerName: string, answers: Answer[], difficulty: Difficulty) {
    let computedAnswers: Answer[] | number[] = answers
    if (!MULTIPLE_ANSWERS_ENABLED) {
      computedAnswers = answers.flat()
    }
    return this.call<Score>('post', 'participations', {
      playerName,
      answers: computedAnswers,
      difficulty
    })
  },
  //#region Auth
  async login(password: string) {
    const { data } = await this.call<Token>('post', 'login', { password })
    instance.defaults.headers.common.Authorization = `Bearer ${data.token}`
  },
  authenticated() {
    return !!instance.defaults.headers.common.Authorization
  },
  logout() {
    delete instance.defaults.headers.common.Authorization
  },
  //#endregion
  //#region Questions
  async createQuestion(question: Question) {
    return this.call<Question>('post', 'questions', question)
  },
  async updateQuestion(question: Question) {
    return this.call<Question>('put', `questions/${question.id}`, question)
  },
  async deleteQuestion(question: Question) {
    return this.call<Question>('delete', `questions/${question.id}`)
  },
  async deleteAllQuestions() {
    return this.call<Question>('delete', `questions/all`)
  },
  async autoGenerateQuestions() {
    return this.call<Question[]>('post', `create-question-auto`)
  },
  //#endregion
  //#region Participations
  async deleteAllParticipations() {
    return this.call<Question>('delete', `participations/all`)
  },
  //#endregion
  //#region Categories
  async getCategories() {
    return this.call<Category[]>('get', `categories`)
  },
  async createCategory(category: Category) {
    return this.call<Category>('post', `categories`, category)
  },
  async updateCategory(category: Category) {
    return this.call<Category>('put', `categories/${category.id}`, category)
  },
  async deleteCategory(category: Category) {
    return this.call<Category>('delete', `categories/${category.id}`)
  },
  //#endregion
  //#region Danger Zone
  async rebuildDatabase() {
    return this.call('post', `rebuild-db`)
  }
  //#endregion
}
