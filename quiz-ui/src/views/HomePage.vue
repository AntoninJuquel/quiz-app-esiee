<script lang="ts">
import quizApiService from "@/services/QuizApiService";
import type { QuizInfo } from "@/types/quiz";
export default {
  name: "HomePage",
  data() {
    const data: {
      registeredScores: QuizInfo;
    } = {
      registeredScores: []
    };
    return data;
  },
  async created() {
    await quizApiService.getQuizInfo().then(response => {
      this.registeredScores = response.data;
    }).catch(error => {
      console.log(error);
    });
  },
};
</script>

<template>
  <div v-for="scoreEntry in registeredScores" v-bind:key="scoreEntry.playerName">
    {{ scoreEntry.playerName }} - {{ scoreEntry.score }}
  </div>
  <router-link to="/start-new-quiz-page">Démarrer le quiz !</router-link>
</template>
