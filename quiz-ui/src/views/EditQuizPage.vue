<script lang="ts">
import quizApiService from '@/services/QuizApiService'
import EditQuestionDisplay from '@/components/EditQuestionDisplay.vue'
import type { Question } from '@/types/quiz'
export default {
  async created() {
    await quizApiService
      .getQuizInfo()
      .then((response) => {
        this.totalNumberOfQuestions = response.data.size
      })
      .catch((error) => {
        console.log(error)
      })

    this.getQuestionByPosition()
  },
  data() {
    return {
      currentQuestionPosition: 0,
      totalNumberOfQuestions: 0,
      currentQuestion: {} as Question,
      creation: false,
      dialog: false,
      dialogActionsEnabled: false
    }
  },
  methods: {
    async getQuestionByPosition() {
      await quizApiService
        .getQuestion(this.currentQuestionPosition)
        .then((response) => {
          if (response.data === null) {
            this.createQuestion()
            return
          }
          this.currentQuestion = response.data
          this.creation = false
        })
        .catch((error) => {
          console.log(error)
          this.createQuestion()
        })
    },
    saveQuestion(question: Question) {
      console.log(question)
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
        id: this.totalNumberOfQuestions.toString(),
        position: this.totalNumberOfQuestions,
        title: '',
        text: '',
        possibleAnswers: [],
        multipleAnswers: false
      }
    },
    deleteQuestion(question: Question) {
      quizApiService
        .deleteQuestion(question.position)
        .then(() => {
          this.currentQuestionPosition--
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
          this.currentQuestionPosition = 0
          this.getQuestionByPosition()
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
    <v-btn v-if="!creation" @click="createQuestion">Créer une question</v-btn>
    <v-btn
      class="mt-4"
      prepend-icon="mdi-delete-forever"
      @click="dialog = dialogActionsEnabled = true"
      color="error"
      >Supprimer les questions</v-btn
    >
    <v-btn
      class="mt-4"
      prepend-icon="mdi-delete-forever"
      @click="dialog = dialogActionsEnabled = true"
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
        <v-btn
          color="blue darken-1"
          text
          @click="deleteAllQuestions"
          :disabled="!dialogActionsEnabled"
          >Confirmer</v-btn
        >
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>
