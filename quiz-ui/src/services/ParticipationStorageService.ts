import type { Difficulty } from '@/types/quiz'

export default {
  clear() {
    localStorage.clear()
  },
  savePlayerName(playerName: string) {
    localStorage.setItem('playerName', playerName)
  },
  saveDifficulty(difficulty: Difficulty) {
    localStorage.setItem('difficulty', difficulty)
  },
  getPlayerName() {
    return localStorage.getItem('playerName') || ''
  },
  getDifficulty() {
    return localStorage.getItem('difficulty') as Difficulty
  },
  saveParticipationScore(participationScore: number) {
    localStorage.setItem('participationScore', participationScore.toString())
  },
  getParticipationScore() {
    return localStorage.getItem('participationScore') || '0'
  }
}
