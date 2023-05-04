<script lang="ts">
import quizApiService from '@/services/QuizApiService'
import participationStorageService from '@/services/ParticipationStorageService'
import QuestionDisplay from '@/components/QuestionDisplay.vue'
import type { Question, Answer } from '@/types/quiz'
export default {
  data() {
    return {
      totalNumberOfQuestions: 0,
      remainingQuestions: [] as number[],
      answers: [] as Answer[],
      currentQuestion: {} as Question
    }
  },
  computed: {
    currentQuestionPosition() {
      return this.remainingQuestions[0]
    },
    currentQuestionNumber() {
      return this.totalNumberOfQuestions - this.remainingQuestions.length
    }
  },
  async created() {
    await quizApiService.getQuizInfo().then((response) => {
      this.totalNumberOfQuestions = response.data.size
      for (let i = 0; i < this.totalNumberOfQuestions; i++) {
        this.remainingQuestions.push(i)
        this.answers.push([-1] as Answer)
      }
      this.remainingQuestions.sort(() => Math.random() - 0.5)
    })

    this.getQuestionByPosition()
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
      this.answers[this.currentQuestionPosition] = answer
      this.remainingQuestions.shift()
      if (this.remainingQuestions.length > 0) {
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
