<script lang="ts">
import quizApiService from '@/services/QuizApiService'
import EditQuestionDisplay from '@/components/EditQuestionDisplay.vue'
import type { Question } from '@/types/quiz'
export default {
  props: ['id'],
  data() {
    return {
      question: {} as Question
    }
  },
  methods: {
    getQuestion() {
      quizApiService.getQuestionById(this.id).then((response) => {
        this.question = response.data
      })
    },
    saveQuestion(question: Question) {
      quizApiService.updateQuestion(question).then(() => {
        this.getQuestion()
      })
    }
  },
  watch: {
    id() {
      this.getQuestion()
    }
  },
  created() {
    this.getQuestion()
  },
  components: {
    EditQuestionDisplay
  }
}
</script>

<template>
  <EditQuestionDisplay v-if="question" :question="question" @save-question="saveQuestion" />
</template>
