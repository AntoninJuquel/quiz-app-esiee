<script lang="ts">
import type { Question } from '@/types/quiz'
export default {
  data() {
    return {
      editedQuestion: {} as Question,
      newAnswer: '',
      selected: [] as number[]
    }
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
      },
      immediate: true
    }
  },
  methods: {
    saveQuestion() {
      this.editedQuestion.possibleAnswers = this.editedQuestion.possibleAnswers.map(
        (answer, index) => {
          return {
            text: answer.text,
            isCorrect: this.selected.includes(index)
          }
        }
      )
      this.$emit('save-question', this.editedQuestion)
    },
    addAnswer() {
      this.editedQuestion.possibleAnswers.push({ text: this.newAnswer })
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
    }
  }
}
</script>

<template>
  <v-card class="mx-auto" max-width="700">
    <v-card-title v-if="!creation">
      <v-text-field
        density="compact"
        variant="underlined"
        prepend-icon="mdi-close"
        @click:prepend="deleteQuestion"
        v-model="editedQuestion.position"
        :min="1"
        :max="totalNumberOfQuestions"
        label="Position"
        type="number"
        :suffix="`/${totalNumberOfQuestions}`"
      ></v-text-field>
      <v-file-input
        density="compact"
        variant="underlined"
        label="Image"
        @update:model-value="onFileChange"
        accept="image/png, image/jpeg, image/bmp"
      ></v-file-input>
    </v-card-title>

    <v-img v-if="editedQuestion.image" :src="editedQuestion.image" height="350px" cover></v-img>

    <v-card-title>
      <v-text-field
        density="compact"
        variant="underlined"
        v-model="editedQuestion.title"
        label="Titre"
      ></v-text-field>
      <v-text-field
        density="compact"
        variant="underlined"
        v-model="editedQuestion.text"
        label="Question"
      ></v-text-field>
    </v-card-title>

    <v-card-text>
      <v-switch v-model="editedQuestion.multipleAnswers" label="Réponses multiples"></v-switch>
      <v-text-field
        density="compact"
        variant="underlined"
        v-model="newAnswer"
        label="Réponse"
        append-icon="mdi-plus"
        @click:append="addAnswer"
      ></v-text-field>
    </v-card-text>

    <v-card-text class="d-flex flex-column align-stretch" v-if="editedQuestion.multipleAnswers">
      <v-sheet
        class="d-flex"
        v-for="(answer, index) in editedQuestion.possibleAnswers"
        :key="index"
      >
        <v-checkbox-btn v-model="selected" :value="index"></v-checkbox-btn>
        <v-text-field
          v-model="answer.text"
          variant="underlined"
          append-icon="mdi-delete"
          @click:append="removeAnswer(index)"
        ></v-text-field>
      </v-sheet>
    </v-card-text>

    <v-card-text v-else>
      <v-radio-group v-model="selected" row>
        <v-sheet
          class="d-flex"
          v-for="(answer, index) in editedQuestion.possibleAnswers"
          :key="index"
        >
          <v-radio :value="[index]" class="flex-grow-0"></v-radio>
          <v-text-field
            v-model="answer.text"
            variant="underlined"
            append-icon="mdi-delete"
            @click:append="removeAnswer(index)"
          ></v-text-field>
        </v-sheet>
      </v-radio-group>
    </v-card-text>

    <v-card-actions>
      <v-btn color="primary" @click="saveQuestion">Sauvegarder</v-btn>
    </v-card-actions>
  </v-card>
</template>
