<script lang="ts">
import quizApiService from '@/services/QuizApiService'
import type { SubmitEventPromise } from 'vuetify/lib/framework.mjs'
export default {
  data() {
    return {
      password: '',
      rules: [(v: string) => !!v || 'Password is required']
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
          this.$router.push('/')
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
</template>
