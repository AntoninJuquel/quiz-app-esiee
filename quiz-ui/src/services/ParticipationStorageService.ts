import type { Difficulty } from "@/types/quiz"

export default {
  clear() {
    localStorage.clear()
  },
  savePlayerName(playerName: string) {
    localStorage.setItem('playerName', playerName)
  },
  getPlayerName() {
    return localStorage.getItem('playerName') || ''
  },
  saveDifficulty(difficulty: Difficulty) {
    localStorage.setItem('difficulty', difficulty.toString())
  },
  getDifficulty() {
    return parseInt(localStorage.getItem('difficulty') || '1') as Difficulty
  },
  saveParticipationScore(participationScore: number) {
    localStorage.setItem('participationScore', participationScore.toString())
  },
  getParticipationScore() {
    return parseInt(localStorage.getItem('participationScore') || '0')
  },
  saveParticipationEmoji(participationEmoji: string) {
    localStorage.setItem('participationEmoji', participationEmoji)
  },
  getParticipationEmoji() {
    return localStorage.getItem('participationEmoji') || ''
  }
}
