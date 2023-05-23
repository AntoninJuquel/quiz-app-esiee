import axios, { AxiosHeaders } from 'axios'
import { format } from 'date-fns'
import type {
  Question,
  QuizInfo,
  Answer,
  Token,
  Difficulty,
  Category,
  Participation
} from '@/types/quiz'

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
  async postParticipation(playerName: string, difficulty: Difficulty, answers: Answer[]) {
    return this.call<Participation>('post', 'participations', {
      playerName,
      answers,
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
  async deleteAllQuestions(date: string = format(new Date(), 'yyyy-MM-dd')) {
    return this.call<Question>('delete', `questions/all?date=${date}`)
  },
  async autoGenerateQuestions() {
    return this.call<Question[]>('post', `create-question-auto`)
  },
  //#endregion
  //#region Participations
  async deleteAllParticipations(date: string = format(new Date(), 'yyyy-MM-dd')) {
    return this.call<Question>('delete', `participations/all?date=${date}`)
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
