export type Score = {
  playerName: string
  score: number
  date: Date
}

export type QuizInfo = Array<Score>

export type Question = {
  image?: string
  video?: string
  title: string
  text: string
  possibleAnswers: Array<string>
  correctAnswerIndex: number[]
  totalNumberOfQuestions: number
}

export type Answer = {
  answerIndex: number[]
}
