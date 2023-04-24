<script lang="ts">
import type { Question } from '@/types/quiz'
export default {
  data() {
    return {
      editedQuestion: {} as Question,
      newAnswer: '',
      selected: []
    }
  },
  props: {
    question: {
      type: Object as () => Question,
      required: true
    }
  },
  emits: ['save-question'],
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
      this.selected.forEach((index: number) => {
        this.editedQuestion.possibleAnswers[index].isCorrect = true
      })
      this.$emit('save-question', this.editedQuestion)
    },
    addAnswer() {
      console.log(this.editedQuestion)
      this.editedQuestion.possibleAnswers.push({ text: this.newAnswer })
    }
  }
}
</script>

<template>
  <v-card class="mx-auto" max-width="700">
    <v-img v-if="question.image" :src="question.image" height="350px" cover></v-img>

    <v-card-title>
      <v-text-field v-model="editedQuestion.title" label="Titre" outlined></v-text-field>
    </v-card-title>

    <v-card-subtitle>
      <v-text-field v-model="editedQuestion.text" label="Question" outlined></v-text-field>
    </v-card-subtitle>

    <v-card-text>
      <v-switch v-model="editedQuestion.multipleAnswers" label="Réponses multiples"></v-switch>
      <v-text-field
        v-model="newAnswer"
        label="Réponse"
        outlined
        append-icon="mdi-plus"
        @click:append="addAnswer"
      ></v-text-field>
    </v-card-text>

    <v-card-actions class="d-flex flex-column align-start" v-if="editedQuestion.multipleAnswers">
      <v-checkbox-btn
        v-for="(answer, index) in editedQuestion.possibleAnswers"
        v-model="selected"
        :key="answer.text"
        :label="answer.text"
        :value="index"
      ></v-checkbox-btn>
    </v-card-actions>
    <v-card-actions v-else>
      <v-radio-group v-model="selected" row>
        <v-radio
          v-for="(answer, index) in editedQuestion.possibleAnswers"
          :key="answer.text"
          :label="answer.text"
          :value="[index]"
        ></v-radio>
      </v-radio-group>
    </v-card-actions>

    <v-card-actions>
      <v-btn color="primary" @click="saveQuestion">Sauvegarder</v-btn>
    </v-card-actions>
  </v-card>
</template>
