<script lang="ts">
import { format } from 'date-fns'
import ParticipationStorageService from '@/services/ParticipationStorageService'
import QuizApiService from '@/services/QuizApiService'
import { difficultyToString } from '@/utils/quiz'

export default {
  data() {
    return {
      numberOfQuestions: 0,
      numberOfParticipants: 0
    }
  },
  computed: {
    playerName() {
      return ParticipationStorageService.getPlayerName()
    },
    difficulty() {
      return difficultyToString(ParticipationStorageService.getDifficulty())
    },
    score() {
      return ParticipationStorageService.getScore()
    },
    emoji() {
      return ParticipationStorageService.getEmoji()
    },
    message() {
      return `J'ai fait un score de ${this.score} sur le quiz #Schooldle #${format(
        new Date(),
        'yyyy-MM-dd'
      )} !
${this.emoji}
${window.location.origin}`
    }
  },
  methods: {
    copyToClipboard() {
      navigator.clipboard.writeText(this.message)
    }
  },
  async created() {
    const quizInfo = await QuizApiService.getQuizInfo()
    this.numberOfParticipants = quizInfo.data.scores.length
    this.numberOfQuestions = quizInfo.data.size
  }
}
</script>

<template>
  <v-container class="bg-surface mt-8 rounded-lg">
    <v-row>
      <v-col cols="12">
        <h2 class="text-h2 text-center">Bravo</h2>
      </v-col>
    </v-row>

    <v-row>
      <v-col cols="12">
        <h3 class="text-h3 text-center">
          Tu as fait un score de <span class="text-primary">{{ score }}</span>
        </h3>
      </v-col>
    </v-row>

    <v-row>
      <v-col cols="12">
        <p class="text-body-1 text-center">
          Tu es le n°<span class="text-primary">{{ numberOfParticipants + 1 }}</span> à avoir
          participé au quiz aujourd'hui
        </p>
      </v-col>
    </v-row>

    <v-row>
      <v-col cols="12">
        <h4 class="text-h4 text-center">
          Difficulté :
          <span class="text-primary">{{ difficulty }}</span>
        </h4>
      </v-col>
    </v-row>

    <v-row>
      <v-col cols="12">
        <h4 class="text-h4 text-center">
          Nombre de questions : <span class="text-primary">{{ numberOfQuestions }}</span>
        </h4>
      </v-col>
    </v-row>
  </v-container>

  <v-container class="bg-surface mt-8 rounded-lg">
    <v-row>
      <v-col cols="12">
        <p class="text-body-1 text-center text-pre-wrap">{{ message }}</p>
      </v-col>
    </v-row>

    <v-row>
      <v-col cols="12" class="d-flex justify-center">
        <v-btn variant="outlined" color="primary" @click="copyToClipboard">Copier</v-btn>
      </v-col>
    </v-row>
  </v-container>
</template>
