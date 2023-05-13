<script lang="ts">
import type { Question, Category } from '@/types/quiz'
import quizApiService from '@/services/QuizApiService'
export default {
  data() {
    return {
      editedQuestion: {} as Question,
      newAnswerInput: '',
      loading: false,
      categories: [] as Category[]
    }
  },
  computed: {
    selected: {
      get() {
        return this.editedQuestion.possibleAnswers?.find((answer) => answer.isCorrect)?.id ?? -1
      },
      set(value: number) {
        this.editedQuestion.possibleAnswers = this.editedQuestion.possibleAnswers.map((answer) => {
          return {
            ...answer,
            isCorrect: value === answer.id
          }
        })
      }
    }
  },
  created() {
    quizApiService.getCategories().then((response) => {
      this.categories = response.data
    })
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
  },
  emits: ['save-question'],
  watch: {
    question: {
      async handler(newQuestion: Question) {
        this.editedQuestion = { ...newQuestion }
        this.selected = newQuestion.possibleAnswers?.find((answer) => answer.isCorrect)?.id ?? -1
        this.loading = false
      },
      immediate: true
    }
  },
  methods: {
    saveQuestion() {
      this.loading = true
      this.$emit('save-question', this.editedQuestion)
    },
    addAnswer() {
      if (!this.newAnswerInput) { return }
      this.editedQuestion.possibleAnswers.push({
        id: this.editedQuestion.possibleAnswers.length,
        isCorrect: false,
        text: this.newAnswerInput,
        question_id: this.editedQuestion.id
      })
      this.newAnswerInput = ''
    },
    removeAnswer(index: number) {
      this.editedQuestion.possibleAnswers.splice(index, 1)
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
  }
}
</script>

<template>
  <v-card class="mx-auto" max-width="700">
    <v-card-title>
      <v-file-input density="compact" variant="underlined" label="Image" @update:model-value="onFileChange"
        accept="image/png, image/jpeg, image/bmp"></v-file-input>
    </v-card-title>

    <v-img v-if="editedQuestion.image" :src="editedQuestion.image" height="350px" cover></v-img>

    <v-card-title>
      <v-combobox dense v-model="editedQuestion.title" label="Titre" :items="categories.map(cat => cat.name)"
        item-title="name" item-value="name" clearable></v-combobox>
      <v-text-field density="compact" variant="underlined" v-model="editedQuestion.text" label="Question"></v-text-field>
    </v-card-title>

    <v-card-text>
      <v-form @submit.prevent="addAnswer">
        <v-text-field density="compact" variant="underlined" v-model="newAnswerInput" label="Réponse"
          append-icon="mdi-plus" @click:append="addAnswer"></v-text-field>
      </v-form>
    </v-card-text>

    <v-card-text>
      <v-radio-group v-model="selected" row>
        <v-sheet class="d-flex" v-for="(answer, index) in editedQuestion.possibleAnswers" :key="index">
          <v-radio :value="answer.id" class="flex-grow-0"></v-radio>
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
