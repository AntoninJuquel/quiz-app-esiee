<script lang="ts">
import quizApiService from '@/services/QuizApiService'
import EditQuestionDisplay from '@/components/EditQuestionDisplay.vue'
import type { Question } from '@/types/quiz'
export default {
  data() {
    return {
      totalNumberOfQuestions: 0,
      currentQuestionPosition: 1,
      currentQuestion: {} as Question,
      creation: false,
      dialog: false,
      dialogActionsEnabled: false,
      dialogAction: () => {}
    }
  },
  methods: {
    async getQuizInfo() {
      await quizApiService
        .getQuizInfo()
        .then((response) => {
          this.totalNumberOfQuestions = response.data.size
        })
        .catch((error) => {
          console.log(error)
        })
    },
    async getQuestionByPosition() {
      await quizApiService
        .getQuestion(this.currentQuestionPosition)
        .then((response) => {
          if (response.data === null) {
            this.startCreateQuestion()
            return
          }
          this.currentQuestion = response.data
          this.creation = false
        })
        .catch((error) => {
          console.log(error)
          this.startCreateQuestion()
        })
    },
    saveQuestion(question: Question) {
      if (this.creation) {
        quizApiService
          .createQuestion(question)
          .then((response) => {
            this.totalNumberOfQuestions++
            this.currentQuestion = { ...question, id: response.data.id }
            this.currentQuestionPosition = question.position
            this.creation = false
          })
          .catch((error) => {
            console.log(error)
          })
      } else {
        quizApiService
          .updateQuestion(question)
          .then(() => {
            this.currentQuestion = question
          })
          .catch((error) => {
            console.log(error)
          })
      }
    },
    startCreateQuestion() {
      this.creation = true
      this.currentQuestionPosition = this.totalNumberOfQuestions + 1
      this.currentQuestion = {
        id: this.totalNumberOfQuestions,
        position: this.currentQuestionPosition,
        title: '',
        text: '',
        image: '',
        possibleAnswers: [],
        multipleAnswers: false
      }
    },
    deleteQuestion(question: Question) {
      quizApiService
        .deleteQuestion(question)
        .then(() => {
          this.totalNumberOfQuestions--
          if (this.totalNumberOfQuestions === 0) {
            this.startCreateQuestion()
            return
          }
          this.currentQuestionPosition = Math.max(1, this.currentQuestionPosition - 1)
          this.getQuestionByPosition()
        })
        .catch((error) => {
          console.log(error)
        })
    },
    async deleteAllQuestions() {
      this.dialogActionsEnabled = false
      await quizApiService
        .deleteAllQuestions()
        .then(() => {
          this.totalNumberOfQuestions = 0
          this.currentQuestionPosition = 1
          this.startCreateQuestion()
        })
        .catch((error) => {
          console.log(error)
        })

      this.dialog = false
    },
    async deleteAllScores() {
      this.dialogActionsEnabled = false
      await quizApiService
        .deleteAllParticipations()
        .then(() => {})
        .catch((error) => {
          console.log(error)
        })
      this.dialog = false
    }
  },
  async created() {
    await this.getQuizInfo()
    if (this.totalNumberOfQuestions === 0) {
      this.startCreateQuestion()
      return
    }
    this.getQuestionByPosition()
  },
  components: {
    EditQuestionDisplay
  }
}
</script>

<template>
  <EditQuestionDisplay
    :creation="creation"
    :question="currentQuestion"
    :totalNumberOfQuestions="totalNumberOfQuestions"
    @save-question="saveQuestion"
    @delete-question="deleteQuestion"
  />
  <v-pagination
    v-model="currentQuestionPosition"
    @update:model-value="getQuestionByPosition"
    :length="totalNumberOfQuestions"
  ></v-pagination>
  <v-sheet class="d-flex flex-column align-center">
    <v-btn v-if="!creation" @click="startCreateQuestion">Créer une question</v-btn>
    <v-btn
      class="mt-4"
      prepend-icon="mdi-delete-forever"
      @click=";(dialogAction = deleteAllQuestions), (dialog = dialogActionsEnabled = true)"
      color="error"
      >Supprimer les questions</v-btn
    >
    <v-btn
      class="mt-4"
      prepend-icon="mdi-delete-forever"
      @click=";(dialogAction = deleteAllScores), (dialog = dialogActionsEnabled = true)"
      color="error"
      >Supprimer les scores</v-btn
    >
  </v-sheet>
  <v-dialog v-model="dialog" width="auto" transition="dialog-bottom-transition" persistent>
    <v-card>
      <v-card-text>
        <p class="text-body-1">Êtes-vous sûr de vouloir supprimer toutes les questions ?</p>
      </v-card-text>
      <v-card-actions>
        <v-btn color="blue darken-1" text @click="dialog = false" :disabled="!dialogActionsEnabled"
          >Annuler</v-btn
        >
        <v-btn color="blue darken-1" text @click="dialogAction" :disabled="!dialogActionsEnabled"
          >Confirmer</v-btn
        >
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>
