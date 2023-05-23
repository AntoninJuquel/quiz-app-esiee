<script lang="ts">
import QuizApiService from '@/services/QuizApiService'
import type { AxiosError } from 'axios'
export default {
  data() {
    return {
      password: '',
      snackbar: false,
      snackbarText: '',
      loading: false
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
    async login() {
      this.loading = true

      if (this.password === '') {
        this.snackbarText = 'Le mot de passe ne peut pas être vide'
        this.snackbar = true
        this.loading = false
        return
      }

      try {
        await QuizApiService.login(this.password)
        this.$router.push('/admin')
        this.$emit('update:modelValue', false)
        this.password = ''
      } catch (err) {
        const error = err as AxiosError
        if (error.response?.status === 401) {
          this.snackbarText = 'Mot de passe incorrect'
          this.snackbar = true
        } else {
          this.snackbarText = 'Une erreur est survenue'
          this.snackbar = true
        }
      }

      this.loading = false
    }
  },
  watch: {
    modelValue(val) {
      if (val && QuizApiService.authenticated()) {
        this.$router.push('/admin')
        this.$emit('update:modelValue', false)
      }
    }
  }
}
</script>

<template>
  <v-dialog
    :model-value="modelValue"
    @update:model-value="$emit('update:modelValue', $event.valueOf())"
    max-width="500px"
    persistent
  >
    <v-card>
      <v-card-title class="headline">Entrer le mot de passe</v-card-title>

      <v-card-text>
        <v-form @submit.prevent="login">
          <v-text-field v-model="password" label="Password" required type="password"></v-text-field>
        </v-form>
      </v-card-text>

      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn color="primary" variant="text" @click="$emit('update:modelValue', false)"
          >RETOUR</v-btn
        >
        <v-btn color="primary" variant="text" @click="login" :loading="loading">Connexion</v-btn>
      </v-card-actions>
    </v-card>

    <v-snackbar v-model="snackbar" :timeout="5000" top color="error">
      {{ snackbarText }}
      <template v-slot:actions>
        <v-btn variant="text" @click="snackbar = false">FERMER</v-btn>
      </template>
    </v-snackbar>
  </v-dialog>
</template>
