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
  text: string
  isCorrect?: boolean
}

export type Question = {
  id: string
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
