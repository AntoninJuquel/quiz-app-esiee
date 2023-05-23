<script lang="ts">
import type { Category, Question } from '@/types/quiz'

export default {
  props: {
    modelValue: {
      type: Object as () => Question | null,
      required: true
    },
    categories: {
      type: Array as () => Category[],
      required: true
    }
  },
  emits: ['update:modelValue', 'save'],
  data() {
    return {
      newAnswer: '',
      imagePreview: false,
      rules: {
        title: (v: number) => !!v || 'Choisir un titre',
        text: (v: string) => !!v || 'Entrer une question'
      },
      loading: false,
      snackbar: {
        show: false,
        text: '',
        color: '',
        timeout: 3000
      }
    }
  },
  computed: {
    creating() {
      return this.modelValue?.id === -1
    },
    correctAnswer: {
      get() {
        return this.modelValue?.possibleAnswers.find((a) => a.isCorrect)?.id
      },
      set(value: number) {
        this.$emit('update:modelValue', {
          ...this.modelValue,
          possibleAnswers: this.modelValue?.possibleAnswers.map((possibleAnswer) => {
            return {
              ...possibleAnswer,
              isCorrect: value === possibleAnswer.id
            }
          })
        })
      }
    }
  },
  methods: {
    onDateChange(payload: Event) {
      const target = payload.target as HTMLInputElement
      this.$emit('update:modelValue', {
        ...this.modelValue,
        date: target.value
      })
    },
    onFileChange(files: File[]) {
      const [file] = files
      if (!file) {
        this.$emit('update:modelValue', {
          ...this.modelValue,
          image: ''
        })
        return
      }
      const reader = new FileReader()
      reader.onload = (e) => {
        this.$emit('update:modelValue', {
          ...this.modelValue,
          image: e.target?.result as string
        })
      }
      reader.readAsDataURL(file)
    },
    updateTitle(title: unknown) {
      this.$emit('update:modelValue', {
        ...this.modelValue,
        title: title as string
      })
    },
    addAnswer() {
      if (this.newAnswer === '' || this.modelValue === null) {
        return
      }

      this.$emit('update:modelValue', {
        ...this.modelValue,
        possibleAnswers: [
          ...this.modelValue.possibleAnswers,
          {
            id: this.modelValue?.possibleAnswers.length + 1,
            text: this.newAnswer,
            isCorrect: false
          }
        ]
      })

      this.newAnswer = ''
    },
    removeAnswer(answerId: number) {
      if (this.modelValue === null) {
        return
      }

      this.$emit('update:modelValue', {
        ...this.modelValue,
        possibleAnswers: this.modelValue.possibleAnswers.filter((a) => a.id !== answerId)
      })
    },
    close() {
      this.$emit('update:modelValue', null)
    },
    save() {
      if (this.modelValue === null) {
        return
      }

      if (this.modelValue.title === '' || this.modelValue.text === '') {
        return
      }

      if (this.modelValue.possibleAnswers.length < 2) {
        this.snackbar = {
          show: true,
          text: 'Il faut au moins 2 reponses',
          color: 'error',
          timeout: 3000
        }
        return
      }

      if (this.correctAnswer === undefined) {
        this.snackbar = {
          show: true,
          text: 'Il faut au moins une reponse correcte',
          color: 'error',
          timeout: 3000
        }
        return
      }

      this.loading = true
      this.$emit('save')
    }
  },
  watch: {
    modelValue: {
      handler() {
        this.newAnswer = ''
        this.loading = false
      },
      deep: true
    }
  }
}
</script>

<template>
  <v-dialog
    :model-value="modelValue !== null"
    max-width="500"
    @update:model-value="close"
    persistent
  >
    <v-dialog v-model="imagePreview" width="auto">
      <v-img
        :src="modelValue?.image"
        width="90vw"
        height="90vh"
        @click="imagePreview = false"
        style="cursor: zoom-out"
      ></v-img>
    </v-dialog>

    <v-card>
      <v-form @submit.prevent="save" validate-on="input">
        <v-card-title class="text-h5">
          <span v-if="creating">Nouvelle Question</span>
          <span v-else>Modifier Question</span>
        </v-card-title>
        <v-card-text>
          <input type="date" :value="modelValue?.date" @input="onDateChange" />
          <v-file-input
            density="compact"
            variant="underlined"
            label="Image"
            @update:model-value="onFileChange"
            accept="image/png, image/jpeg, image/bmp"
            :append-icon="modelValue?.image ? 'mdi-eye' : undefined"
            @click:append="imagePreview = true"
          ></v-file-input>
          <v-combobox
            dense
            :model-value="modelValue?.title"
            @update:model-value="updateTitle"
            label="Categorie"
            :items="categories.map((cat) => cat.name)"
            item-title="name"
            item-value="name"
            clearable
            required
            :rules="[rules.title]"
          ></v-combobox>
          <v-text-field
            :model-value="modelValue?.text"
            @input="$emit('update:modelValue', { ...modelValue, text: $event.target.value })"
            label="Question"
            required
            :rules="[rules.text]"
          ></v-text-field>
          <v-form @submit.prevent="addAnswer">
            <v-text-field
              v-model="newAnswer"
              label="Ajouter une reponse"
              append-icon="mdi-plus"
              @click:append="addAnswer"
            ></v-text-field>
          </v-form>
          <v-radio-group v-model="correctAnswer">
            <v-row v-for="answer in modelValue?.possibleAnswers" :key="answer.id">
              <v-radio :label="answer.text" :value="answer.id"></v-radio>
              <v-btn icon @click="removeAnswer(answer.id)">
                <v-icon color="error">mdi-delete</v-icon>
              </v-btn>
            </v-row>
          </v-radio-group>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="primary" @click="close">Cancel</v-btn>
          <v-btn color="primary" type="submit" :loading="loading">Save</v-btn>
        </v-card-actions>
      </v-form>
    </v-card>

    <v-snackbar v-model="snackbar.show" :color="snackbar.color" :timeout="snackbar.timeout">
      {{ snackbar.text }}
    </v-snackbar>
  </v-dialog>
</template>
