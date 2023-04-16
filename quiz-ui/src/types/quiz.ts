export type Score = {
  playerName: string
  score: number
  date: Date
}

export type QuizInfo = {
  registeredScores: Array<Score>
}

export type Question = {
  image?: string
  video?: string
  title: string
  text: string
  possibleAnswers: Array<string>
  correctAnswerIndex: number
}