<script lang="ts">
import type { Answer, Question } from '@/types/quiz'
export default {
  name: 'QuestionDisplay',
  props: {
    question: {
      type: Object as () => Question,
      required: true
    }
  },
  data() {
    return {
      answers: [] as Answer
    }
  },
  methods: {
    answerClickedHandler() {
      this.$emit('answer-selected', this.answers)
      this.answers = []
    }
  },
  emits: ['answer-selected']
}
</script>

<template>
  <img v-if="question.image" :src="question.image" />
  <h1>{{ question.title }}</h1>
  <p>{{ question.text }}</p>
  <v-form @submit.prevent="answerClickedHandler">
    <template v-if="question.multipleAnswers">
      <v-checkbox
        v-for="(answer, index) in question.possibleAnswers"
        :key="answer"
        :label="answer"
        :value="index"
        v-model="answers"
        hide-details
      ></v-checkbox>
    </template>
    <v-radio-group v-else v-model="answers">
      <v-radio
        v-for="(answer, index) in question.possibleAnswers"
        :key="answer"
        :label="answer"
        :value="[index]"
      ></v-radio>
    </v-radio-group>
    <v-btn block type="submit">Answer</v-btn>
  </v-form>
</template>

<style scoped></style>
