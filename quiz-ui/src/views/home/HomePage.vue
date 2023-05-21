<script lang="ts">
import QuizApiService from '@/services/QuizApiService'
import type { Participation } from '@/types/quiz'
import EnterQuizDialog from '@/components/EnterQuizDialog.vue'
import { difficultyToEmoji } from '@/utils/quiz'
export default {
  data() {
    return {
      numberOfQuestions: 0,
      participations: [] as Participation[],
      openQuiz: false,
      loading: false
    }
  },
  computed: {
    hasParticipations(): boolean {
      return this.participations.length > 0
    },
    hasQuestions(): boolean {
      return this.numberOfQuestions > 0
    }
  },
  methods: {
    async fetchQuizInfo() {
      this.loading = true
      const quizInfo = await QuizApiService.getQuizInfo()
      this.participations = quizInfo.data.scores
      this.numberOfQuestions = quizInfo.data.size
      this.loading = false
    },
    difficultyToEmoji
  },
  created() {
    this.fetchQuizInfo()
  },
  components: {
    EnterQuizDialog
  }
}
</script>

<template>
  <v-container class="bg-surface mt-8 rounded-lg">
    <v-table fixed-header height="300px" density="compact">
      <thead>
        <tr>
          <th class="text-left">Nom</th>
          <th class="text-left">Difficulté</th>
          <th class="text-left">Score</th>
        </tr>
      </thead>
      <tbody v-if="hasParticipations">
        <tr v-for="(participation, index) in participations" :key="index">
          <td>{{ participation.playerName }}</td>
          <td>{{ difficultyToEmoji(participation.difficulty) }}</td>
          <td>{{ participation.score }}</td>
        </tr>
      </tbody>
      <tbody v-else>
        <tr>
          <td colspan="3" class="text-center">Aucune participation</td>
        </tr>
      </tbody>
    </v-table>

    <p class="inline text-body-1">
      Aujourd'hui, il y a <span class="text-primary">{{ numberOfQuestions }}</span> questions
    </p>
    <v-btn
      color="primary"
      size="x-large"
      prepend-icon="mdi-brain"
      @click="openQuiz = true"
      :disabled="!hasQuestions"
    >
      Commencer le quiz
    </v-btn>

    <v-btn
      class="ml-4"
      color="primary"
      @click="fetchQuizInfo"
      icon="mdi-refresh"
      v-if="!hasQuestions"
      :loading="loading"
    >
    </v-btn>
  </v-container>

  <EnterQuizDialog v-model="openQuiz"></EnterQuizDialog>
</template>
