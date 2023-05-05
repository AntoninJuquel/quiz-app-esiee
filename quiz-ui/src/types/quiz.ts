export type Score = {
  playerName: string
  score: number
  date: Date
}

export type QuizInfo = {
  scores: Array<Score>
  size: number
}

export type PossibleAnswer = {
  id: number
  text: string
  isCorrect: boolean
  question_id: number
}

export type Question = {
  id: number
  position: number
  title: string
  text: string
  possibleAnswers: Array<PossibleAnswer>
  multipleAnswers: boolean
  image?: string
  video?: string
}

export type Answer = number[]

export type Token = {
  token: string
}

export enum Difficulty {
  EASY = 'easy',
  MEDIUM = 'medium',
  HARD = 'hard'
}
