<script lang="ts">
import ParticipationStorageService from '@/services/ParticipationStorageService'
export default {
  data() {
    return {
      playerName: '',
      difficulty: 1
    }
  },
  props: {
    modelValue: {
      type: Boolean,
      required: true
    }
  },
  emits: ['update:modelValue'],
  methods: {
    async startQuiz() {
      if (this.playerName === '') {
        return
      }
      ParticipationStorageService.savePlayerName(this.playerName)
      ParticipationStorageService.saveDifficulty(this.difficulty)
      this.$router.push('/quiz')
    }
  }
}
</script>

<template>
  <v-dialog
    :model-value="modelValue"
    @update:model-value="$emit('update:modelValue', $event.valueOf())"
    max-width="500px"
  >
    <v-card>
      <v-card-title class="headline">Choisissez un nom</v-card-title>

      <v-card-text>
        <v-form @submit.prevent="startQuiz">
          <v-text-field v-model="playerName" label="Nom" required></v-text-field>
          <v-btn-toggle
            v-model="difficulty"
            variant="outlined"
            divided
            class="w-100 justify-center"
          >
            <v-btn :value="1">Facile</v-btn>
            <v-btn :value="2">Moyen</v-btn>
            <v-btn :value="3">Difficile</v-btn>
          </v-btn-toggle>
        </v-form>
      </v-card-text>

      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn color="primary" text @click="$emit('update:modelValue', false)">Cancel</v-btn>
        <v-btn color="primary" text @click="startQuiz">Start</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>
