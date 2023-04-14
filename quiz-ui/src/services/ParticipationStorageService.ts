export default {
    clear() {
        localStorage.clear();
    },
    savePlayerName(playerName: string) {
        localStorage.setItem("playerName", playerName);
    },
    getPlayerName() {
        localStorage.getItem("playerName");
    },
    saveParticipationScore(participationScore: number) {
        localStorage.setItem("participationScore", participationScore.toString());
    },
    getParticipationScore() {
        localStorage.getItem("participationScore");
    }
};