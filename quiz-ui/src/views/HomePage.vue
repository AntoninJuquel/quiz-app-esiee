<script lang="ts">
import quizApiService from '@/services/QuizApiService'
import type { QuizInfo } from '@/types/quiz'
export default {
  data() {
    return {
      registeredScores: {} as QuizInfo
    }
  },
  async created() {
    await quizApiService
      .getQuizInfo()
      .then((response) => {
        this.registeredScores = response.data
      })
      .catch((error) => {
        console.log(error)
      })
  }
}
</script>

<template>
  <v-sheet class="d-flex flex-column align-center">
    <v-sheet
      class="d-flex flex-column align-center flex-wrap text-center mx-auto mb-4 pa-4"
      elevation="4"
      height="fit-content"
      rounded
      max-width="800"
      width="100%"
    >
      <h1 class="text-h6 text-md-h5 text-lg-h4 mb-4">Scoreboard</h1>
      <p
        v-for="scoreEntry in registeredScores.scores"
        v-bind:key="scoreEntry.playerName"
        class="text-body-1"
      >
        {{ scoreEntry.playerName }} - {{ scoreEntry.score }}
      </p>
    </v-sheet>
    <v-btn to="/new-quiz">Démarrer le quiz !</v-btn>
  </v-sheet>
</template>
