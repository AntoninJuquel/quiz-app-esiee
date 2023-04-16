<script lang="ts">
import QuestionManager from '@/components/QuestionManager.vue';
export default {
  name: "QuestionsPage",
  components: {
    QuestionManager: QuestionManager,
  },
}
</script>

<template>
  <v-sheet width="700" class="mx-auto">
    <QuestionManager />
  </v-sheet>
</template>

<style scoped></style>
