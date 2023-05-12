<script lang="ts">
import { format, parseISO } from "date-fns"
import type { Question, Category } from '@/types/quiz'
import quizApiService from '@/services/QuizApiService'
export default {
  data() {
    return {
      editedQuestion: {} as Question,
      newAnswer: '',
      selected: [] as number[],
      loading: false,
      totalNumberOfQuestions: 0,
      categories: [] as Category[]
    }
  },
  created() {
    quizApiService.getCategories().then((response) => {
      this.categories = response.data
    })
  },
  computed: {
    date: {
      get() {
        return this.editedQuestion.date
      },
      set(value: string) {
        this.editedQuestion.date = format(parseISO(value), 'yyyy-MM-dd')
      }
    },

  },
  props: {
    creation: {
      type: Boolean,
      required: true
    },
    question: {
      type: Object as () => Question,
      required: true
    },
    totalNumberOfQuestions: {
      type: Number,
      required: true
    }
  },
  emits: ['save-question', 'delete-question'],
  watch: {
    question: {
      handler: function (newQuestion: Question) {
        this.editedQuestion = { ...newQuestion }
        this.selected = (this.editedQuestion.possibleAnswers || [])
          .map((answer) => {
            return answer.isCorrect ? answer.id : -1
          })
          .filter((index) => index !== -1)
        this.loading = false
      },
      immediate: true
    }
  },
  methods: {
    saveQuestion() {
      this.loading = true
      this.editedQuestion.possibleAnswers = this.editedQuestion.possibleAnswers.map((answer) => {
        return {
          ...answer,
          isCorrect: this.selected.includes(answer.id)
        }
      })
      this.$emit('save-question', {
        ...this.editedQuestion,
        position: parseInt(this.editedQuestion.position.toString())
      })
    },
    addAnswer() {
      if (!this.newAnswer) { return }
      this.editedQuestion.possibleAnswers.push({
        id: this.editedQuestion.possibleAnswers.length,
        isCorrect: false,
        text: this.newAnswer,
        question_id: this.editedQuestion.id
      })
      this.newAnswer = ''
    },
    removeAnswer(index: number) {
      this.editedQuestion.possibleAnswers.splice(index, 1)
    },
    deleteQuestion() {
      this.$emit('delete-question', this.editedQuestion)
    },
    onFileChange(files: File[]) {
      const [file] = files
      if (!file) {
        this.editedQuestion.image = ''
        return
      }
      const reader = new FileReader()
      reader.onload = (e) => {
        this.editedQuestion.image = e.target?.result as string
      }
      reader.readAsDataURL(file)
    },
    async onChangeDate() {
      await quizApiService
        .getQuizInfo(this.editedQuestion.date).then((response) => {
          this.editedQuestion.position = response.data.size + 1
          this.totalNumberOfQuestions = response.data.size
        })
    }
  }
}
</script>

<template>
  <v-card class="mx-auto" max-width="700">
    <v-card-title>
      <input type="date" v-model="date" class="mx-2" @change="onChangeDate">
      <v-text-field v-if="!creation" density="compact" variant="underlined" prepend-icon="mdi-close"
        @click:prepend="deleteQuestion" v-model="editedQuestion.position" :min="1" :max="totalNumberOfQuestions"
        label="Position" type="number" :suffix="`/${totalNumberOfQuestions}`"></v-text-field>
      <v-file-input density="compact" variant="underlined" label="Image" @update:model-value="onFileChange"
        accept="image/png, image/jpeg, image/bmp"></v-file-input>
    </v-card-title>

    <v-img v-if="editedQuestion.image" :src="editedQuestion.image" height="350px" cover></v-img>

    <v-card-title>
      <v-combobox dense v-model="editedQuestion.title" label="Titre" :items="categories.map(cat => cat.name)" item-title="name"
        item-value="name" clearable></v-combobox>
      <v-text-field density="compact" variant="underlined" v-model="editedQuestion.text" label="Question"></v-text-field>
    </v-card-title>

    <v-card-text>
      <v-switch v-model="editedQuestion.multipleAnswers" label="Réponses multiples"></v-switch>
      <v-form @submit.prevent="addAnswer">
        <v-text-field density="compact" variant="underlined" v-model="newAnswer" label="Réponse" append-icon="mdi-plus"
          @click:append="addAnswer"></v-text-field>
      </v-form>
    </v-card-text>

    <v-card-text class="d-flex flex-column align-stretch" v-if="editedQuestion.multipleAnswers">
      <v-sheet class="d-flex" v-for="(answer, index) in editedQuestion.possibleAnswers" :key="index">
        <v-checkbox-btn v-model="selected" :value="answer.id"></v-checkbox-btn>
        <v-text-field v-model="answer.text" variant="underlined" append-icon="mdi-delete"
          @click:append="removeAnswer(index)"></v-text-field>
      </v-sheet>
    </v-card-text>
    <v-card-text v-else>
      <v-radio-group v-model="selected" row>
        <v-sheet class="d-flex" v-for="(answer, index) in editedQuestion.possibleAnswers" :key="index">
          <v-radio :value="[answer.id]" class="flex-grow-0"></v-radio>
          <v-text-field v-model="answer.text" variant="underlined" append-icon="mdi-delete"
            @click:append="removeAnswer(index)"></v-text-field>
        </v-sheet>
      </v-radio-group>
    </v-card-text>

    <v-card-actions>
      <v-btn color="primary" @click="saveQuestion" :loading="loading">Sauvegarder</v-btn>
    </v-card-actions>
  </v-card>
</template>
