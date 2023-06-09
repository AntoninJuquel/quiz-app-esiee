<script lang="ts">
import { formatDuration, intervalToDuration } from 'date-fns'
import { fr } from 'date-fns/locale'
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
      loading: false,
      interval: 0,
      timeBeforeQuiz: '',

      snackbar: false,
      snackbarMessage: '',
      snackbarColor: ''
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
    async getQuizInfo() {
      try {
        this.loading = true
        const quizInfo = await QuizApiService.getQuizInfo()
        this.participations = quizInfo.data.scores
        this.numberOfQuestions = quizInfo.data.size
        this.loading = false

        if (this.hasQuestions) {
          this.snackbar = true
          this.snackbarMessage = 'Informations du quiz récupérées'
          this.snackbarColor = 'success'
        } else {
          this.snackbar = true
          this.snackbarMessage = 'Aucune question disponible'
          this.snackbarColor = 'warning'
        }
      } catch (error) {
        this.snackbar = true
        this.snackbarMessage = 'Impossible de récupérer les informations du quiz'
        this.snackbarColor = 'error'
        this.loading = false
      }
    },
    difficultyToEmoji,
    refreshTimer() {
      const now = new Date()
      const nextQuiz = new Date()
      nextQuiz.setHours(24, 0, 0, 0)
      if (now > nextQuiz) {
        nextQuiz.setDate(nextQuiz.getDate() + 1)
      }
      const duration = intervalToDuration({
        start: now,
        end: nextQuiz
      })
      this.timeBeforeQuiz = formatDuration(duration, {
        format: ['hours', 'minutes', 'seconds'],
        locale: fr,
        zero: true
      })
    }
  },
  created() {
    this.getQuizInfo()
    this.refreshTimer()
    this.interval = window.setInterval(() => {
      this.refreshTimer()
    }, 1000)
  },
  components: {
    EnterQuizDialog
  },
  unmounted() {
    clearInterval(this.interval)
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

    <p class="inline text-body-1" v-if="hasQuestions">
      Aujourd'hui, il y a <span class="text-primary">{{ numberOfQuestions }}</span> questions
    </p>
    <p class="inline text-body-1" v-else>Aucune question aujourd'hui, revenez <span class="text-primary">demain</span></p>
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
      @click="getQuizInfo"
      icon="mdi-refresh"
      v-if="!hasQuestions"
      :loading="loading"
    >
    </v-btn>
  </v-container>

  <v-container class="bg-surface mt-8 rounded-lg">
    <p class="inline text-body-1">
      Le Prochain quiz est dans <span class="text-primary">{{ timeBeforeQuiz }}</span>
    </p>
  </v-container>

  <EnterQuizDialog v-model="openQuiz"></EnterQuizDialog>

  <v-snackbar v-model="snackbar" :timeout="3000" :color="snackbarColor">
    {{ snackbarMessage }}
  </v-snackbar>
</template>
