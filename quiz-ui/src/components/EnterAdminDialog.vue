<script lang="ts">
import QuizApiService from '@/services/QuizApiService'
export default {
  data() {
    return {
      password: ''
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
    login() {
      QuizApiService.login(this.password)
        .then(() => {
          this.$router.push('/admin')
        })
        .finally(() => {
          this.password = ''
          this.$emit('update:modelValue', false)
        })
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
        <v-btn color="primary" text @click="$emit('update:modelValue', false)">Cancel</v-btn>
        <v-btn color="primary" text @click="login">Connexion</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>
