<script lang="ts">
import { format } from 'date-fns'
import QuizApiService from '@/services/QuizApiService'
import EditQuestionDisplay from '@/components/EditQuestionDisplay.vue'
import type { Question } from '@/types/quiz'
export default {
  data() {
    return {
      question: {
        id: 0,
        position: 1,
        question: '',
        title: '',
        text: '',
        possibleAnswers: [],
        image: '',
        date: this.$route.query.date
      } as Question
    }
  },
  methods: {
    createQuestion(question: Question) {
      QuizApiService.createQuestion(question).then((response) => {
        this.$router.push(`/admin/questions/${response.data.id}`)
      })
    }
  },
  components: {
    EditQuestionDisplay
  }
}
</script>

<template>
  <EditQuestionDisplay :question="question" @save-question="createQuestion" />
</template>
