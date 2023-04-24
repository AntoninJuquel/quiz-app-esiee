<script lang="ts">
import participationStorageService from '@/services/ParticipationStorageService'
import type { SubmitEventPromise } from 'vuetify/lib/framework.mjs'
export default {
  data() {
    return {
      playerName: '',
      rules: [(v: string) => !!v || 'Name is required']
    }
  },
  methods: {
    async startQuiz(event: SubmitEventPromise) {
      const results = await event
      if (!results.valid) return
      participationStorageService.savePlayerName(this.playerName)
      this.$router.push('/quiz')
    }
  }
}
</script>

<template>
  <v-sheet width="300" class="mx-auto">
    <v-form validate-on="submit" @submit.prevent="startQuiz">
      <v-text-field v-model="playerName" :rules="rules" label="Player name"></v-text-field>
      <v-btn type="submit" block class="mt-2">Entrer !</v-btn>
    </v-form>
  </v-sheet>
</template>
