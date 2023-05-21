<script lang="ts">
import format from 'date-fns/format'
import QuizApiService from '@/services/QuizApiService'
import type { Question } from '@/types/quiz'

export default {
  data() {
    return {
      questions: [] as Question[],
      questionsDate: format(new Date(), 'yyyy-MM-dd')
    }
  },
  methods: {
    async getQuestions() {
      const questions = await QuizApiService.getQuestions(this.questionsDate)
      this.questions = questions.data
    }
  },
  watch: {
    questionsDate() {
      this.getQuestions()
    }
  },
  async created() {
    await this.getQuestions()
  }
}
</script>

<template>
  <v-expansion-panel>
    <v-expansion-panel-title>
      <v-card-title>Questions</v-card-title>
      <v-btn icon @click.stop="" color="primary">
        <v-icon>mdi-plus</v-icon>
      </v-btn>
    </v-expansion-panel-title>

    <v-expansion-panel-text>
      <input type="date" v-model="questionsDate" />
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
              <v-btn icon>
                <v-icon color="error">mdi-delete</v-icon>
              </v-btn>
            </th>
          </tr>
        </thead>
        <tbody v-if="questions.length > 0">
          <tr v-for="question in questions" :key="question.id">
            <td>{{ question.title }}</td>
            <td>{{ question.text }}</td>
            <td>{{ question.possibleAnswers.length }}</td>
            <td>{{ question.possibleAnswers.find((answer) => answer.isCorrect)?.text }}</td>
            <td class="text-right">
              <v-btn icon>
                <v-icon>mdi-pen</v-icon>
              </v-btn>
            </td>
            <td class="text-right">
              <v-btn icon>
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

      <v-btn color="error">Tout supprimer</v-btn>
    </v-expansion-panel-text>
  </v-expansion-panel>
</template>
