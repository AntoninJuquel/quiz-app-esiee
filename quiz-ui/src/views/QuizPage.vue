<script lang="ts">
import quizApiService from '@/services/QuizApiService'
import participationStorageService from '@/services/ParticipationStorageService'
import QuestionDisplay from '@/components/QuestionDisplay.vue'
import type { Question, Answer } from '@/types/quiz'
export default {
  async created() {
    await quizApiService.getQuizInfo().then((response) => {
      this.totalNumberOfQuestions = response.data.size
    })

    this.getQuestionByPosition()
  },
  data() {
    return {
      currentQuestionPosition: 0,
      totalNumberOfQuestions: 0,
      answers: [] as Answer[],
      currentQuestion: {} as Question
    }
  },
  methods: {
    async getQuestionByPosition() {
      await quizApiService
        .getQuestion(this.currentQuestionPosition)
        .then((response) => {
          this.currentQuestion = response.data
        })
        .catch((error) => {
          console.log(error)
        })
    },
    answerQuestion(answer: Answer) {
      this.answers.push(answer)
      this.currentQuestionPosition++
      if (this.currentQuestionPosition < this.totalNumberOfQuestions) {
        this.getQuestionByPosition()
      } else {
        this.endQuiz()
      }
    },
    async endQuiz() {
      await quizApiService
        .postAnswers(participationStorageService.getPlayerName(), this.answers)
        .then((response) => {
          participationStorageService.saveParticipationScore(response.data.score)
          this.$router.push('/quiz-results')
        })
        .catch((error) => {
          console.log(error)
        })
    }
  },
  components: {
    QuestionDisplay
  }
}
</script>

<template>
  <QuestionDisplay :question="currentQuestion" @answer-question="answerQuestion" />
</template>
