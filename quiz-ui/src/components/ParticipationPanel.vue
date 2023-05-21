<script lang="ts">
import format from 'date-fns/format'
import QuizApiService from '@/services/QuizApiService'
import type { Participation } from '@/types/quiz'

export default {
  data() {
    return {
      participations: [] as Participation[],
      participationDate: format(new Date(), 'yyyy-MM-dd')
    }
  },
  methods: {
    async getQuizInfo() {
      const participations = await QuizApiService.getQuizInfo(this.participationDate)
      this.participations = participations.data.scores
    },
    async deleteAllParticipations() {
      await QuizApiService.deleteAllParticipations()
      await this.getQuizInfo()
    }
  },
  watch: {
    participationDate() {
      this.getQuizInfo()
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
      <input type="date" v-model="participationDate" />
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
            <td>
              <v-icon v-if="participation.difficulty === 1">mdi-emoticon-excited-outline</v-icon>
              <v-icon v-else-if="participation.difficulty === 2"
                >mdi-emoticon-neutral-outline</v-icon
              >
              <v-icon v-else-if="participation.difficulty === 3">mdi-emoticon-sad-outline</v-icon>
            </td>
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
</template>
