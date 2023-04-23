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
  saveParticipationScore(participationScore: number) {
    localStorage.setItem('participationScore', participationScore.toString())
  },
  getParticipationScore() {
    return localStorage.getItem('participationScore') || '0'
  }
}
