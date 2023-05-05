<script lang="ts">
import type { Question } from '@/types/quiz'
export default {
  data() {
    return {
      selected: [],
      loading: false
    }
  },
  props: {
    question: {
      type: Object as () => Question,
      required: true
    }
  },
  emits: ['answer-question'],
  methods: {
    answerQuestion() {
      this.loading = true
      this.$emit('answer-question', this.selected)
    }
  },
  watch: {
    question() {
      this.selected = []
      this.loading = false
    }
  }
}
</script>

<template>
  <v-card class="mx-auto" max-width="700">
    <v-img v-if="question.image" :src="question.image" height="350px" cover></v-img>

    <v-card-title>{{ question.title }}</v-card-title>

    <v-card-subtitle>{{ question.text }}</v-card-subtitle>

    <v-card-actions class="d-flex flex-column align-start" v-if="question.multipleAnswers">
      <v-checkbox-btn
        v-for="(answer, index) in question.possibleAnswers"
        :key="answer.id"
        v-model="selected"
        :label="answer.text"
        :value="index + 1"
      ></v-checkbox-btn>
    </v-card-actions>
    <v-card-actions v-else>
      <v-radio-group v-model="selected" row>
        <v-radio
          v-for="(answer, index) in question.possibleAnswers"
          :key="answer.id"
          :label="answer.text"
          :value="[index + 1]"
        ></v-radio>
      </v-radio-group>
    </v-card-actions>

    <v-card-actions>
      <v-btn color="primary" @click="answerQuestion" :loading="loading">Répondre</v-btn>
    </v-card-actions>
  </v-card>
</template>
