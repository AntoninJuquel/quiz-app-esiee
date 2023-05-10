export type Score = {
  playerName: string
  score: number
  difficulty: number
  text: string
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
  image: string
  position: number
  title: string
  text: string
  possibleAnswers: Array<PossibleAnswer>
  date: string
  multipleAnswers: boolean
}

export type Answer = number[]

export type Token = {
  token: string
}

export enum Difficulty {
  EASY = 1,
  MEDIUM = 2,
  HARD = 3
}

export type Category = {
  id: number
  name: string
  emoji: string
}