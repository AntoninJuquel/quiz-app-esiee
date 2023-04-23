<script lang="ts">
import quizApiService from '@/services/QuizApiService'
import participationStorageService from '@/services/ParticipationStorageService'
import QuestionDipslay from '@/components/QuestionDisplay.vue'
import type { Question, Answer } from '@/types/quiz'

export default {
  data() {
    return {
      currentQuestionPosition: 1,
      totalNumberOfQuestions: 0,
      currentQuestion: {} as Question,
      answers: [] as Answer[]
    }
  },
  methods: {
    async loadQuestionByPosition() {
      await quizApiService
        .getQuestion(this.currentQuestionPosition)
        .then((response) => {
          ;[this.currentQuestion] = response.data
          this.totalNumberOfQuestions = this.currentQuestion.totalNumberOfQuestions
        })
        .catch((error) => {
          console.log(error)
        })
    },
    answerClickedHandler(answers: Answer) {
      this.answers.push(answers)
      if (this.currentQuestionPosition < this.totalNumberOfQuestions) {
        this.currentQuestionPosition++
        this.loadQuestionByPosition()
      } else {
        this.endQuiz()
      }
    },
    async endQuiz() {
      await quizApiService
        .postAnswers(participationStorageService.getPlayerName(), this.answers)
        .then((response) => {
          participationStorageService.saveParticipationScore(response.data.score)
          this.$router.push('/your-score')
        })
        .catch((error) => {
          console.log(error)
        })
    }
  },
  created() {
    this.loadQuestionByPosition()
  },
  components: {
    QuestionDisplay: QuestionDipslay
  }
}
</script>

<template>
  <h1>Question {{ currentQuestionPosition }} / {{ totalNumberOfQuestions }}</h1>
  <QuestionDisplay :question="currentQuestion" @answer-selected="answerClickedHandler" />
</template>

<style scoped></style>
