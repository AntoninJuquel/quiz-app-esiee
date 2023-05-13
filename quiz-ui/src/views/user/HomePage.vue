<script lang="ts">
import ScoreboardDisplay from '@/components/ScoreboardDisplay.vue'
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
  },
  components: {
    ScoreboardDisplay
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
    
    <ScoreboardDisplay v-if="!loading" :scores="quizInfo.scores" />
    <v-btn to="/new-quiz" :disabled="quizInfo.size === 0">{{
      quizInfo.size === 0 ? 'Pas encore de question' : 'Démarrer le quiz !'
    }}</v-btn>
    <v-btn to="/admin" v-if="quizInfo.size === 0" class="mt-4">Créer des questions</v-btn>
  </v-sheet>
</template>
