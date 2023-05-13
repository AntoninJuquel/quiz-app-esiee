<script lang="ts">
import { format } from 'date-fns'
import participationStorageService from '@/services/ParticipationStorageService'
export default {
  computed: {
    playerName: participationStorageService.getPlayerName,
    score: participationStorageService.getParticipationScore,
    emoji: participationStorageService.getParticipationEmoji
  },
  methods: {
    copyToClipboard() {
      const text = 
`J' ai fait un score de ${this.score} sur le quiz #${format(new Date(), 'yyyy-MM-dd')}.
${this.emoji}
${window.location.origin}`

      navigator.clipboard.writeText(text)
    }
  }
}
</script>

<template>
  <v-sheet
    class="d-flex flex-column align-center justify-center flex-wrap text-center mx-auto mb-4 text-pre-wrap"
    elevation="4"
    height="500"
    rounded
    max-width="800"
    width="100%"
  >
    <h1 class="text-h6 text-md-h5 text-lg-h4 mb-4">Bravo !</h1>
    <h2 class="text-h6 text-md-h5 text-lg-h4 mb-4">{{ playerName }}</h2>
    <p class="text-body-1 mb-4">Tu as terminé le quiz.</p>
    <p class="text-body-1 mb-4">Voici ton score:</p>
    <h3 class="text-h6 text-md-h5 text-lg-h4 mb-4">{{ score }}</h3>
    <p class="text-body-1 mb-4 text-left">{{ emoji }}</p>
    <v-btn color="primary" @click="copyToClipboard" class="mt-4">Copy to clipboard</v-btn>
  </v-sheet>
</template>
