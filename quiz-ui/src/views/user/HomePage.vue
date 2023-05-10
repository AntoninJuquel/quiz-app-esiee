<script lang="ts">
import quizApiService from '@/services/QuizApiService'
import type { QuizInfo } from '@/types/quiz'
export default {
  data() {
    return {
      loading: true,
      quizInfo: {} as QuizInfo
    }
  },
  async created() {
    await quizApiService
      .getQuizInfo()
      .then((response) => {
        this.quizInfo = response.data
        this.loading = false
      })
      .catch((error) => {
        console.log(error)
      })
  }
}
</script>

<template>
  <v-sheet class="d-flex flex-column align-center">
    <v-skeleton-loader
      v-if="loading"
      :elevation="4"
      max-width="800"
      width="100%"
    ></v-skeleton-loader>
    <v-sheet
      v-else-if="quizInfo.scores.length > 0"
      class="d-flex flex-column align-center flex-wrap text-center mx-auto mb-4 pa-4"
      elevation="4"
      height="fit-content"
      rounded
      max-width="800"
      width="100%"
    >
      <h1 class="text-h6 text-md-h5 text-lg-h4 mb-4">Scoreboard</h1>
      <p
        v-for="scoreEntry in quizInfo.scores"
        v-bind:key="scoreEntry.playerName"
        class="text-body-1"
      >
        {{ scoreEntry.playerName }} - {{ scoreEntry.score }} - {{ "💩".repeat(scoreEntry.difficulty) }}
      </p>
    </v-sheet>
    <v-btn to="/new-quiz" :disabled="quizInfo.size === 0">{{
      quizInfo.size === 0 ? 'Pas encore de question' : 'Démarrer le quiz !'
    }}</v-btn>

    <v-btn to="/admin" v-if="quizInfo.size === 0" class="mt-4">Créer des questions</v-btn>
  </v-sheet>
</template>
