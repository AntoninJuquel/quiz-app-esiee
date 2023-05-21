<script lang="ts">
import format from 'date-fns/format'
import QuizApiService from '@/services/QuizApiService'
import type { Question, Category } from '@/types/quiz'

import EditQuestionDialog from './EditQuestionDialog.vue'

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
      editQuestion: null as Question | null
    }
  },
  methods: {
    async getQuestions() {
      const questions = await QuizApiService.getQuestions(this.questionsDate)
      this.questions = questions.data
    },
    async saveQuestion() {
      if (this.editQuestion === null) {
        return
      }
      if (this.editQuestion.id === -1) {
        await QuizApiService.createQuestion(this.editQuestion)
      } else {
        await QuizApiService.updateQuestion(this.editQuestion)
      }
      await this.getQuestions()
      this.editQuestion = null
    },
    async deleteQuestion(question: Question) {
      await QuizApiService.deleteQuestion(question)
      this.questions = this.questions.filter((c) => c.id !== question.id)
    },
    async deleteAllQuestions() {
      await QuizApiService.deleteAllQuestions()
      this.questions = []
    },
    async autoGenerateQuestions() {
      await QuizApiService.autoGenerateQuestions()
      await this.getQuestions()
    }
  },
  watch: {
    questionsDate() {
      this.getQuestions()
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
        <v-btn
          color="primary"
          @click="
            editQuestion = {
              id: -1,
              position: 1,
              title: '',
              image: '',
              text: '',
              possibleAnswers: [],
              date: questionsDate
            }
          "
          >Nouvelle question</v-btn
        >
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
              <v-btn icon>
                <v-icon>mdi-pen</v-icon>
              </v-btn>
            </th>
            <th class="text-right">
              <v-btn icon @click="deleteAllQuestions">
                <v-icon color="error">mdi-delete</v-icon>
              </v-btn>
            </th>
          </tr>
        </thead>
        <tbody v-if="questions.length > 0">
          <tr v-for="question in questions" :key="question.id">
            <td>
              {{ categories?.find((category) => category.name === question.title)?.emoji }}
              {{ question.title }}
            </td>
            <td>{{ question.text }}</td>
            <td>{{ question.possibleAnswers.length }}</td>
            <td>{{ question.possibleAnswers.find((answer) => answer.isCorrect)?.text }}</td>
            <td class="text-right">
              <v-btn icon @click="editQuestion = question">
                <v-icon>mdi-pen</v-icon>
              </v-btn>
            </td>
            <td class="text-right">
              <v-btn icon @click="deleteQuestion(question)">
                <v-icon color="error">mdi-delete</v-icon>
              </v-btn>
            </td>
          </tr>
        </tbody>

        <tbody v-else>
          <tr>
            <td colspan="4" class="text-center">Aucune question</td>
          </tr>
        </tbody>
      </v-table>

      <v-card-actions>
        <v-btn color="primary" @click="autoGenerateQuestions">Générer des questions</v-btn>
        <v-spacer />
        <v-btn color="error" @click="deleteAllQuestions">Tout supprimer</v-btn>
      </v-card-actions>
    </v-expansion-panel-text>
  </v-expansion-panel>

  <EditQuestionDialog v-model="editQuestion" :categories="categories" @save="saveQuestion" />
</template>
