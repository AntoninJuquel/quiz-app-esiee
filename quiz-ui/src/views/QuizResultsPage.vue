<script lang="ts">
import participationStorageService from '@/services/ParticipationStorageService'
export default {
  computed: {
    playerName: participationStorageService.getPlayerName,
    score: participationStorageService.getParticipationScore
  }
}
</script>

<template>
  <v-sheet
    class="d-flex flex-column align-center justify-center flex-wrap text-center mx-auto mb-4"
    elevation="4"
    height="350"
    rounded
    max-width="800"
    width="100%"
  >
    <h1 class="text-h6 text-md-h5 text-lg-h4 mb-4">Congratulation !</h1>
    <h2 class="text-h6 text-md-h5 text-lg-h4 mb-4">{{ playerName }}</h2>
    <p class="text-body-1 mb-4">You have finished the quiz.</p>
    <p class="text-body-1 mb-4">Your score is:</p>
    <h3 class="text-h6 text-md-h5 text-lg-h4 mb-4">{{ score }}</h3>
  </v-sheet>
</template>
