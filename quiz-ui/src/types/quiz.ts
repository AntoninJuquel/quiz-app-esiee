export type Participation = {
  playerName: string
  score: number
  difficulty: number
  emoji: string
}

export type QuizInfo = {
  scores: Array<Participation>
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
}

export type Answer = number

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
