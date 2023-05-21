import type { Difficulty } from '@/types/quiz'

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
  saveScore(score: number) {
    localStorage.setItem('score', score.toString())
  },
  getScore() {
    return parseInt(localStorage.getItem('score') || '0')
  },
  saveEmoji(emoji: string) {
    localStorage.setItem('emoji', emoji)
  },
  getEmoji() {
    return localStorage.getItem('emoji') || ''
  }
}
