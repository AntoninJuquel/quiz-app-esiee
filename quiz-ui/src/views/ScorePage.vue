<script lang="ts">
import participationStorageService from '@/services/ParticipationStorageService'
export default {
  data(){
    return {
      score: participationStorageService.getParticipationScore()
    }
  }
}
</script>

<template>
  <main>
    <h1>This is your score</h1>
    <p>{{ score }}</p>
  </main>
</template>

<style scoped></style>
