<script lang="ts">
import format from 'date-fns/format'
import QuizApiService from '@/services/QuizApiService'
import type { Participation } from '@/types/quiz'
import { difficultyToEmoji } from '@/utils/quiz'
import type { AxiosError } from 'axios'

export default {
  data() {
    return {
      participations: [] as Participation[],
      participationDate: format(new Date(), 'yyyy-MM-dd'),
      snackbar: {
        show: false,
        text: '',
        color: '',
        timeout: 3000
      }
    }
  },
  methods: {
    async getQuizInfo() {
      try {
        const participations = await QuizApiService.getQuizInfo(this.participationDate)
        this.participations = participations.data.scores
      } catch (e) {
        const error = e as AxiosError
        this.snackbar = {
          show: true,
          text: error.message,
          color: 'error',
          timeout: 5000
        }
      }
    },
    async deleteAllParticipations() {
      await QuizApiService.deleteAllParticipations()
      await this.getQuizInfo()
    },
    difficultyToEmoji
  },
  watch: {
    async participationDate() {
      this.snackbar = {
        show: true,
        text: 'Chargement des participations...',
        color: 'info',
        timeout: 3000
      }

      await this.getQuizInfo()

      if (this.participations.length === 0) {
        this.snackbar = {
          show: true,
          text: 'Aucune participation pour cette date',
          color: 'warning',
          timeout: 3000
        }
      } else {
        this.snackbar = {
          show: true,
          text: 'Participations chargées',
          color: 'success',
          timeout: 3000
        }
      }
    }
  },
  async created() {
    await this.getQuizInfo()
  }
}
</script>

<template>
  <v-expansion-panel>
    <v-expansion-panel-title>
      <v-card-title>Participations</v-card-title>
    </v-expansion-panel-title>

    <v-expansion-panel-text>
      <v-card-actions>
        <v-spacer />
        <input type="date" v-model="participationDate" />
      </v-card-actions>
      <v-table fixed-header density="compact">
        <thead>
          <tr>
            <th class="text-left">Nom</th>
            <th class="text-left">Difficulté</th>
            <th class="text-left">Score</th>
          </tr>
        </thead>
        <tbody v-if="participations.length > 0">
          <tr v-for="(participation, index) in participations" :key="index">
            <td>{{ participation.playerName }}</td>
            <td>{{ difficultyToEmoji(participation.difficulty) }}</td>
            <td>{{ participation.score }}</td>
          </tr>
        </tbody>

        <tbody v-else>
          <tr>
            <td colspan="4" class="text-center">Aucune participation</td>
          </tr>
        </tbody>
      </v-table>

      <v-card-actions>
        <v-spacer />
        <v-btn color="error" @click="deleteAllParticipations">Tout supprimer</v-btn>
      </v-card-actions>
    </v-expansion-panel-text>
  </v-expansion-panel>

  <v-snackbar v-model="snackbar.show" :color="snackbar.color" :timeout="snackbar.timeout">
    {{ snackbar.text }}
  </v-snackbar>
</template>
