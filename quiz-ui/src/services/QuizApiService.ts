import axios, { AxiosError, AxiosHeaders } from 'axios'
import type { QuizInfo } from '@/types/quiz'

const instance = axios.create({
  baseURL: `${import.meta.env.VITE_API_URL}`,
  responseType: 'json'
})

export default {
  async call<T>(
    method: string,
    resource: string,
    data = null,
    token = null
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
  getQuizInfo() {
    return this.call<QuizInfo>('get', 'quiz-info')
  },
  getQuestion(position: number) {
    throw new Error(`Not implemented yet. Position: ${position}`)
  }
}
