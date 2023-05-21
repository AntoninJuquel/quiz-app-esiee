<script lang="ts">
import EnterAdminDialog from './components/EnterAdminDialog.vue'
export default {
  name: 'App',
  data() {
    return {
      openAdmin: false
    }
  },
  components: {
    EnterAdminDialog
  }
}
</script>

<template>
  <v-app>
    <v-toolbar app dark height="100" color="primary">
      <v-toolbar-title class="headline">
        <router-link to="/" class="text-h2 text-decoration-none text-white">
          Shcooldle
        </router-link>
      </v-toolbar-title>
      <v-spacer></v-spacer>
      <v-btn icon @click="openAdmin = true">
        <v-icon>mdi-cog</v-icon>
      </v-btn>
    </v-toolbar>
    <router-view />

    <EnterAdminDialog v-model="openAdmin" />
  </v-app>
</template>
