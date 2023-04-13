<script lang="ts">
import { RouterLink } from 'vue-router'
import quizApiService from "@/services/QuizApiService";
import type { QuizInfo } from "@/types/quiz";
export default {
  name: "HomePage",
  data() {
    const data: QuizInfo = {
      registeredScores: []
    };
    return data;
  },
  async created() {
    await quizApiService.getQuizInfo().then(response => {
      this.registeredScores = response.data.registeredScores;
    }).catch(error => {
      console.log(error);
    });
  },
  setup() {
    return {
      RouterLink
    };
  }
};
</script>

<template>
  <div v-for="scoreEntry in registeredScores" v-bind:key="scoreEntry.date.toISOString()">
    {{ scoreEntry.playerName }} - {{ scoreEntry.score }}
  </div>
  <RouterLink to="/start-new-quiz-page">Démarrer le quiz !</RouterLink>
</template>
