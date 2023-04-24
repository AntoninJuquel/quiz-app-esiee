<script lang="ts">
import quizApiService from '@/services/QuizApiService'
import EditQuestionDisplay from '@/components/EditQuestionDisplay.vue'
import type { Question } from '@/types/quiz'
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
      currentQuestion: {} as Question,
      creation: false
    }
  },
  methods: {
    async getQuestionByPosition() {
      await quizApiService
        .getQuestion(this.currentQuestionPosition)
        .then((response) => {
          this.currentQuestion = response.data
          this.creation = false
        })
        .catch((error) => {
          console.log(error)
        })
    },
    saveQuestion(question: Question) {
      if (this.creation) {
        quizApiService
          .createQuestion(question)
          .then((response) => {
            this.currentQuestion = response.data
            this.creation = false
          })
          .catch((error) => {
            console.log(error)
          })
      } else {
        quizApiService
          .updateQuestion(question)
          .then((response) => {
            this.currentQuestion = response.data
          })
          .catch((error) => {
            console.log(error)
          })
      }
    },
    createQuestion() {
      this.creation = true
      this.currentQuestion = {
        id: '0',
        position: this.totalNumberOfQuestions,
        title: '',
        text: '',
        possibleAnswers: [],
        multipleAnswers: false
      }
    }
  },
  components: {
    EditQuestionDisplay
  }
}
</script>

<template>
  <EditQuestionDisplay :question="currentQuestion" @answer-question="saveQuestion" />
  <v-pagination
    v-model="currentQuestionPosition"
    @update:model-value="getQuestionByPosition"
    :length="totalNumberOfQuestions"
  ></v-pagination>
  <v-sheet class="d-flex flex-column align-center">
    <v-btn @click="createQuestion">Créer une question</v-btn>
  </v-sheet>
</template>
