export type Score = {
  playerName: string
  score: number
  date: Date
}

export type QuizInfo = {
  registeredScores: Array<Score>
}
