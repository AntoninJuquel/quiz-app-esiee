<script lang="ts">
</script>

<template>
  <header>
    <div class="wrapper">
      <h1>Hello world</h1>

      <nav>
        <router-link to="/">Home</router-link>
        <router-link to="/about">About</router-link>
      </nav>
    </div>
  </header>
  <v-sheet width="700" class="mx-auto">
    <router-view />
  </v-sheet>
</template>

<style scoped></style>
