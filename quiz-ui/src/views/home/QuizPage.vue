<script lang="ts">
import { format, subSeconds } from 'date-fns'
import ParticipationStorageService from '@/services/ParticipationStorageService'
import QuizApiService from '@/services/QuizApiService'
import type { Answer, Question } from '@/types/quiz'
import { startDifficultyTimer } from '@/utils/quiz'
export default {
  data() {
    return {
      loading: false,
      questions: [] as Question[],
      answers: [] as Answer[],
      remainingQuestionIndexes: [] as number[],
      selectedAnswer: 0,
      dialog: false,
      timer: {
        value: 0,
        clear: () => {},
        refresh: () => {}
      }
    }
  },
  computed: {
    hasQuestions() {
      return this.questions.length > 0
    },
    currentQuestionIndex() {
      return this.remainingQuestionIndexes[0]
    },
    currentQuestion() {
      return this.questions[this.currentQuestionIndex]
    },
    isLastQuestion() {
      return this.remainingQuestionIndexes.length === 1
    },
    questionNumber() {
      return this.questions.length - this.remainingQuestionIndexes.length + 1
    },
    playerName() {
      return ParticipationStorageService.getPlayerName()
    },
    difficulty() {
      return ParticipationStorageService.getDifficulty()
    },
    formatedCountdown() {
      const date = new Date(0)
      date.setSeconds(this.timer.value)
      return format(subSeconds(date, 1), 'mm:ss')
    }
  },
  methods: {
    async getQuestions() {
      this.loading = true
      const questions = await QuizApiService.getQuestions()
      this.questions = questions.data
      this.remainingQuestionIndexes = [...Array(this.questions.length).keys()]
      this.remainingQuestionIndexes.sort(() => Math.random() - 0.5)
      this.answers = new Array(this.questions.length).fill(0 as Answer)
      this.loading = false
    },
    async submitAnswers() {
      this.loading = true
      const participation = await QuizApiService.postParticipation(
        this.playerName,
        this.difficulty,
        this.answers
      )

      ParticipationStorageService.saveScore(participation.data.score)
      ParticipationStorageService.saveEmoji(participation.data.emoji)

      this.$router.push('/results')
    },
    answerQuestion() {
      this.answers[this.currentQuestionIndex] = this.selectedAnswer
      this.selectedAnswer = 0

      this.timer.refresh()

      if (this.isLastQuestion) {
        this.submitAnswers()
      } else {
        this.remainingQuestionIndexes.shift()
      }
    }
  },
  async created() {
    await this.getQuestions()

    const { clear, refresh } = startDifficultyTimer(
      this.difficulty,
      this.questions.length,
      (time) => (this.timer.value = time),
      () => {
        this.answerQuestion()
        return this.isLastQuestion
      },
      this.submitAnswers
    )

    this.timer.clear = clear
    this.timer.refresh = refresh
  },
  unmounted() {
    this.timer.clear()
  }
}
</script>

<template>
  <div v-if="hasQuestions">
    <v-container class="bg-surface mt-8 rounded-lg" v-if="difficulty > 1">
      <v-card-title class="text-center">
        <h1 class="text-h2 font-weight-bold">🕒{{ formatedCountdown }}🕒</h1>
      </v-card-title>
    </v-container>

    <v-container class="bg-surface mt-8 rounded-lg">
      <v-card-title class="text-center">
        <h1 class="text-h5">Question {{ questionNumber }} of {{ questions.length }}</h1>
      </v-card-title>
    </v-container>

    <v-container class="bg-surface mt-8 rounded-lg">
      <v-card-text class="text-center">
        <h2 class="text-h6">{{ currentQuestion.title }}</h2>

        <v-img
          v-if="currentQuestion.image"
          :src="currentQuestion.image"
          height="120"
          style="cursor: zoom-in"
          @click="dialog = true"
        >
          <v-dialog v-model="dialog" width="auto">
            <v-img
              :src="currentQuestion.image"
              width="90vw"
              height="90vh"
              @click="dialog = false"
              style="cursor: zoom-out"
            ></v-img>
          </v-dialog>
        </v-img>

        <p class="text-body-1">{{ currentQuestion.text }}</p>
      </v-card-text>

      <v-card-text class="text-center">
        <v-radio-group v-model="selectedAnswer" row>
          <v-radio
            v-for="(answer, index) in currentQuestion.possibleAnswers"
            :key="index"
            :label="answer.text"
            :value="index + 1"
          ></v-radio>
        </v-radio-group>
      </v-card-text>

      <v-card-actions>
        <v-btn color="primary" @click="answerQuestion" :loading="loading">Answer</v-btn>
      </v-card-actions>
    </v-container>
  </div>

  <div v-else-if="loading">Loading...</div>

  <v-container v-else class="bg-surface mt-8 rounded-lg">
    <v-card-title class="text-center">
      <h1 class="text-h5">No questions found</h1>
    </v-card-title>

    <v-card-text class="text-center">
      <p class="text-body-1">Please contact the quiz master.</p>
    </v-card-text>
  </v-container>
</template>
