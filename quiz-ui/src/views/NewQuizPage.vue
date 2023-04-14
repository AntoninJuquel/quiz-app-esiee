<script lang="ts">
import participationStorageService from '@/services/ParticipationStorageService'
export default {
  data: () => ({
    username: '',
    rules: [
      (value: string) => {
        if (value) return true
        return 'You must enter a first name.'
      },
    ],
  }),
  methods:{
    launchNewQuiz(){
      participationStorageService.savePlayerName(this.username);
      this.$router.push('/questions');
    },
  }
}

</script>

<template>
  <v-sheet width="300" class="mx-auto">
    <v-form @submit.prevent="launchNewQuiz">
      <v-text-field v-model="username" :rules="rules" label="Username" />
      <v-btn type="submit" block class="mt-2">GO !</v-btn>
    </v-form>
  </v-sheet>
</template>

<style scoped></style>
