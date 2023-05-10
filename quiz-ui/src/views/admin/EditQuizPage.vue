<script lang="ts">
import { format, parseISO } from 'date-fns'
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
      dialogAction: () => { },
      quizDate: format(new Date(), 'yyyy-MM-dd')
    }
  },
  computed: {
    date: {
      get() {
        return this.quizDate
      },
      set(value: string) {
        this.quizDate = format(parseISO(value), 'yyyy-MM-dd')
      }
    }
  },
  methods: {
    async getQuizInfo() {
      await quizApiService
        .getQuizInfo(this.quizDate)
        .then((response) => {
          this.totalNumberOfQuestions = response.data.size
        })
        .catch((error) => {
          console.log(error)
        })
    },
    async getQuestionByPosition() {
      await quizApiService
        .getQuestion(this.currentQuestionPosition, this.quizDate)
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
          .then(async (response) => {
            this.quizDate = question.date
            this.currentQuestion = { ...question, id: response.data.id }
            this.creation = false
            await this.getQuizInfo()
            this.currentQuestionPosition = this.totalNumberOfQuestions
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
        date: format(new Date(), 'yyyy-MM-dd'),
        possibleAnswers: [],
        multipleAnswers: false
      }
    },
    deleteQuestion(question: Question) {
      quizApiService
        .deleteQuestion(question)
        .then(async () => {
          await this.getQuizInfo()
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
        .then(async () => {
          this.currentQuestionPosition = 1
          await this.getQuizInfo()
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
        .then(() => { })
        .catch((error) => {
          console.log(error)
        })
      this.dialog = false
    },
    async rebuildDatabase() {
      this.dialogActionsEnabled = false
      await quizApiService
        .rebuildDatabase()
        .then(async () => {
          this.currentQuestionPosition = 1
          await this.getQuizInfo()
        })
        .catch((error) => {
          console.log(error)
        })
      this.dialog = false
    },
    async onChangeDate() {
      await this.getQuizInfo()
      this.currentQuestionPosition = 1
      this.getQuestionByPosition()
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
  <input type="date" v-model="date" @change="onChangeDate" />
  <EditQuestionDisplay :creation="creation" :question="currentQuestion" :totalNumberOfQuestions="totalNumberOfQuestions"
    @save-question="saveQuestion" @delete-question="deleteQuestion" />
  <v-pagination v-model="currentQuestionPosition" @update:model-value="getQuestionByPosition"
    :length="totalNumberOfQuestions"></v-pagination>
  <v-sheet class="d-flex flex-column align-center">
    <v-btn v-if="!creation" @click="startCreateQuestion">Créer une question</v-btn>
    <v-btn class="mt-4" prepend-icon="mdi-delete-forever"
      @click="; (dialogAction = deleteAllQuestions), (dialog = dialogActionsEnabled = true)" color="error">Supprimer les
      questions</v-btn>
    <v-btn class="mt-4" prepend-icon="mdi-delete-forever"
      @click="; (dialogAction = deleteAllScores), (dialog = dialogActionsEnabled = true)" color="error">Supprimer les
      scores</v-btn>
    <v-btn class="mt-4" prepend-icon="mdi-delete-forever"
      @click="; (dialogAction = rebuildDatabase), (dialog = dialogActionsEnabled = true)" color="error">Réinitialiser la
      base de donnée</v-btn>
  </v-sheet>
  <v-dialog v-model="dialog" width="auto" transition="dialog-bottom-transition" persistent>
    <v-card>
      <v-card-text>
        <p class="text-body-1">Êtes-vous sûr de vouloir supprimer toutes les questions ?</p>
      </v-card-text>
      <v-card-actions>
        <v-btn color="blue darken-1" text @click="dialog = false" :disabled="!dialogActionsEnabled">Annuler</v-btn>
        <v-btn color="blue darken-1" text @click="dialogAction" :disabled="!dialogActionsEnabled">Confirmer</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>
