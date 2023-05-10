<script lang="ts">
import { format, subSeconds } from 'date-fns'
import quizApiService from '@/services/QuizApiService'
import participationStorageService from '@/services/ParticipationStorageService'
import QuestionDisplay from '@/components/QuestionDisplay.vue'
import { type Question, type Answer, Difficulty } from '@/types/quiz'
export default {
  data() {
    return {
      totalNumberOfQuestions: 0,
      remainingQuestions: [] as number[],
      answers: [] as Answer[],
      currentQuestion: {} as Question,
      timeRemaining: 0,
      interval: null as number | null,
      difficulty: Difficulty.EASY,
      step: 1
    }
  },
  computed: {
    currentQuestionPosition() {
      return this.remainingQuestions[0]
    },
    formatCountdown() {
      const date = new Date(0)
      date.setSeconds(this.timeRemaining)
      return format(subSeconds(date, 1), 'mm:ss')
    }
  },
  async created() {
    await quizApiService.getQuizInfo().then((response) => {
      this.totalNumberOfQuestions = response.data.size
      for (let i = 0; i < this.totalNumberOfQuestions; i++) {
        this.remainingQuestions.push(i + 1)
        this.answers.push([0] as Answer)
      }
      this.remainingQuestions.sort(() => Math.random() - 0.5)
    })

    this.difficulty = participationStorageService.getDifficulty()

    switch (this.difficulty) {
      case Difficulty.EASY:
        break
      case Difficulty.MEDIUM: {
        this.timeRemaining = this.totalNumberOfQuestions * 10 + 1
        this.interval = setInterval(() => {
          this.timeRemaining--
          if (this.timeRemaining <= 0) {
            this.endQuiz()
          }
        }, 1000)
        break
      }
      case Difficulty.HARD: {
        this.timeRemaining = 6
        this.interval = setInterval(() => {
          this.timeRemaining--
          if (this.timeRemaining <= 0) {
            this.answerQuestion([0] as Answer)
          }
        }, 1000)
        break
      }
      default:
        break
    }

    this.getQuestionByPosition()
  },
  unmounted() {
    if (this.interval) {
      clearInterval(this.interval)
    }
  },
  methods: {
    async getQuestionByPosition() {
      await quizApiService
        .getQuestion(this.currentQuestionPosition)
        .then((response) => {
          this.currentQuestion = response.data
          this.step = Math.min(
            this.totalNumberOfQuestions - this.remainingQuestions.length + 1,
            this.totalNumberOfQuestions
          )
        })
        .catch((error) => {
          console.log(error)
        })
    },
    answerQuestion(answer: Answer) {
      this.answers[this.currentQuestionPosition - 1] = answer
      this.remainingQuestions.shift()
      if (this.remainingQuestions.length > 0) {
        if (this.difficulty === Difficulty.HARD) {
          this.timeRemaining = 6
        }
        this.getQuestionByPosition()
      } else {
        this.endQuiz()
      }
    },
    async endQuiz() {
      if (this.interval) {
        clearInterval(this.interval)
      }
      await quizApiService
        .postAnswers(participationStorageService.getPlayerName(), this.answers, this.difficulty)
        .then((response) => {
          participationStorageService.saveParticipationScore(response.data.score)
          participationStorageService.saveParticipationText(response.data.text)
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
  <h3 class="text-h3 text-center">{{ step }} / {{ totalNumberOfQuestions }}</h3>
  <h3 v-if="interval" class="text-h3 text-center">{{ formatCountdown }}</h3>
  <QuestionDisplay :question="currentQuestion" @answer-question="answerQuestion" />
</template>
