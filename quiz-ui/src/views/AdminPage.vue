<script lang="ts">
import quizApiService from '@/services/QuizApiService'
import type { SubmitEventPromise } from 'vuetify/lib/framework.mjs'
export default {
  data() {
    return {
      password: '',
      rules: [(v: string) => !!v || 'Veillez entrer un mot de passe'],
      dialog: false
    }
  },
  methods: {
    async login(event: SubmitEventPromise) {
      const results = await event
      if (!results.valid) return
      await quizApiService
        .login(this.password)
        .then(() => {
          this.$router.push('/edit-quiz')
        })
        .catch((error) => {
          console.log(error)
          this.dialog = true
          this.password = ''
        })
    }
  }
}
</script>

<template>
  <v-sheet width="300" class="mx-auto">
    <v-form validate-on="submit" @submit.prevent="login">
      <v-text-field
        v-model="password"
        :rules="rules"
        label="Mot de passe"
        type="password"
      ></v-text-field>
      <v-btn type="submit" block class="mt-2">Entrer !</v-btn>
    </v-form>
  </v-sheet>
  <v-dialog v-model="dialog" width="auto" transition="dialog-top-transition">
    <v-card>
      <v-card-text>
        <p class="text-body-1">Mot de passe incorrect</p>
      </v-card-text>
      <v-card-actions>
        <v-btn color="blue darken-1" text @click="dialog = false">Fermer</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>
