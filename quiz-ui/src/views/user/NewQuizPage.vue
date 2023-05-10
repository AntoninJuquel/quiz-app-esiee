<script lang="ts">
import participationStorageService from '@/services/ParticipationStorageService'
import type { SubmitEventPromise } from 'vuetify/lib/framework.mjs'
import { Difficulty } from '@/types/quiz'
export default {
  data() {
    return {
      playerName: '',
      rules: [(v: string) => !!v || 'Name is required'],
      difficulty: Difficulty.EASY,
      Difficulty
    }
  },
  computed: {
    difficultyLabel() {
      switch (this.difficulty) {
        case Difficulty.EASY:
          return 'Facile, pas de chrono'
        case Difficulty.MEDIUM:
          return 'Moyen, temps total 10 secondes par question'
        case Difficulty.HARD:
          return 'Difficile, temps par question 5 secondes'
        default:
          return ''
      }
    }
  },
  methods: {
    async startQuiz(event: SubmitEventPromise) {
      const results = await event
      if (!results.valid) return
      participationStorageService.savePlayerName(this.playerName)
      participationStorageService.saveDifficulty(this.difficulty)
      this.$router.push('/quiz')
    }
  }
}
</script>

<template>
  <v-sheet width="300" class="mx-auto">
    <v-form validate-on="submit" @submit.prevent="startQuiz">
      <v-text-field v-model="playerName" :rules="rules" label="Player name"></v-text-field>
      <v-label>Difficulté</v-label>
      <v-btn-toggle v-model="difficulty" class="d-flex justify-center mt-2">
        <v-btn text :value="Difficulty.EASY">Facile</v-btn>
        <v-btn text :value="Difficulty.MEDIUM">Moyen</v-btn>
        <v-btn text :value="Difficulty.HARD">Difficile</v-btn>
      </v-btn-toggle>
      <p class="text-caption text-center">{{ difficultyLabel }}</p>
      <v-btn type="submit" block class="mt-2">Entrer !</v-btn>
    </v-form>
  </v-sheet>
</template>
