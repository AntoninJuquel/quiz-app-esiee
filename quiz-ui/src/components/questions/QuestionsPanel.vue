<script lang="ts">
import format from 'date-fns/format'
import QuizApiService from '@/services/QuizApiService'
import type { Question, Category } from '@/types/quiz'

import EditQuestionDialog from './EditQuestionDialog.vue'
import type { AxiosError } from 'axios'

export default {
  props: {
    categories: {
      type: Array as () => Category[],
      required: true
    }
  },
  data() {
    return {
      questions: [] as Question[],
      questionsDate: format(new Date(), 'yyyy-MM-dd'),
      editQuestion: null as Question | null,
      generatingQuestions: false,
      snackbar: {
        show: false,
        text: '',
        color: '',
        timeout: 3000
      }
    }
  },
  methods: {
    newQuestion() {
      this.editQuestion = {
        id: -1,
        position: 1,
        title: '',
        image: '',
        text: '',
        possibleAnswers: [],
        date: this.questionsDate
      }
    },
    async getQuestions() {
      try {
        const questions = await QuizApiService.getQuestions(this.questionsDate)
        this.questions = questions.data
      } catch (e) {
        const error = e as AxiosError
        this.snackbar = {
          show: true,
          text: error.message,
          color: 'error',
          timeout: 5000
        }
      }
    },
    async saveQuestion() {
      if (this.editQuestion === null) {
        return
      }

      try {
        if (this.editQuestion.id === -1) {
          await QuizApiService.createQuestion(this.editQuestion)
        } else {
          await QuizApiService.updateQuestion(this.editQuestion)
        }
        if (this.editQuestion.date !== this.questionsDate) {
          this.questionsDate = this.editQuestion.date
        } else {
          await this.getQuestions()
        }
        this.editQuestion = null
      } catch (e) {
        const error = e as AxiosError
        this.snackbar = {
          show: true,
          text: error.message,
          color: 'error',
          timeout: 5000
        }

        if (this.editQuestion) {
          this.editQuestion = { ...this.editQuestion }
        }
      }
    },
    async deleteQuestion(question: Question) {
      await QuizApiService.deleteQuestion(question)
      this.questions = this.questions.filter((c) => c.id !== question.id)
    },
    async deleteAllQuestions() {
      await QuizApiService.deleteAllQuestions(this.questionsDate)
      this.questions = []
    },
    async autoGenerateQuestions() {
      this.generatingQuestions = true
      try {
        await QuizApiService.autoGenerateQuestions(this.questionsDate)
        await this.getQuestions()
      } catch (e) {
        const error = e as AxiosError
        this.snackbar = {
          show: true,
          text: error.message,
          color: 'error',
          timeout: 5000
        }
      }
      this.generatingQuestions = false
    }
  },
  watch: {
    async questionsDate() {
      this.snackbar = {
        show: true,
        text: 'Chargement des questions...',
        color: 'info',
        timeout: 3000
      }
      await this.getQuestions()
      if (this.questions.length === 0) {
        this.snackbar = {
          show: true,
          text: 'Aucune question pour cette date',
          color: 'warning',
          timeout: 5000
        }
      } else {
        this.snackbar = {
          show: true,
          text: 'Questions chargées',
          color: 'success',
          timeout: 3000
        }
      }
    }
  },
  async created() {
    await this.getQuestions()
  },
  components: {
    EditQuestionDialog
  }
}
</script>

<template>
  <v-expansion-panel>
    <v-expansion-panel-title>
      <v-card-title>Questions</v-card-title>
    </v-expansion-panel-title>

    <v-expansion-panel-text>
      <v-card-actions>
        <v-btn color="primary" @click="newQuestion">Nouvelle question</v-btn>
        <v-spacer />
        <input type="date" v-model="questionsDate" />
      </v-card-actions>

      <v-table density="compact">
        <thead>
          <tr>
            <th class="text-left">Catégorie</th>
            <th class="text-left">Question</th>
            <th class="text-left">Réponse possibles</th>
            <th class="text-left">Bonne réponse</th>
            <th class="text-right">
              <v-btn icon @click="deleteAllQuestions">
                <v-icon color="error">mdi-delete</v-icon>
              </v-btn>
            </th>
          </tr>
        </thead>
        <tbody v-if="questions.length > 0">
          <v-hover v-for="question in questions" :key="question.id">
            <template v-slot:default="{ isHovering, props }">
              <tr
                v-bind="props"
                @click="editQuestion = question"
                style="cursor: pointer"
                :class="{
                  'bg-background darken-2': isHovering
                }"
              >
                <td>
                  {{ categories?.find((category) => category.name === question.title)?.emoji }}
                  {{ question.title }}
                </td>
                <td>{{ question.text }}</td>
                <td>{{ question.possibleAnswers.length }}</td>
                <td>{{ question.possibleAnswers.find((answer) => answer.isCorrect)?.text }}</td>
                <td class="text-right">
                  <v-btn icon @click.stop="deleteQuestion(question)">
                    <v-icon color="error">mdi-delete</v-icon>
                  </v-btn>
                </td>
              </tr>
            </template>
          </v-hover>
        </tbody>

        <tbody v-else>
          <tr>
            <td colspan="4" class="text-center">Aucune question</td>
          </tr>
        </tbody>
      </v-table>

      <v-card-actions>
        <v-btn color="primary" @click="autoGenerateQuestions" :loading="generatingQuestions"
          >Générer des questions</v-btn
        >
        <v-spacer />
        <v-btn color="error" @click="deleteAllQuestions">Tout supprimer</v-btn>
      </v-card-actions>
    </v-expansion-panel-text>
  </v-expansion-panel>

  <EditQuestionDialog v-model="editQuestion" :categories="categories" @save="saveQuestion" />

  <v-snackbar v-model="snackbar.show" :color="snackbar.color" :timeout="snackbar.timeout">
    {{ snackbar.text }}
  </v-snackbar>
</template>
