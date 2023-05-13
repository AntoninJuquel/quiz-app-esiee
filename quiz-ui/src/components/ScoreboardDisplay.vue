<script lang="ts">
export default {
    props: ['scores'],
}
</script>

<template>
    <v-sheet class="d-flex flex-column align-center flex-wrap text-center mx-auto mb-4 pa-4" elevation="4"
        height="fit-content" rounded max-width="800" width="100%">
        <h1 class="text-h6 text-md-h5 text-lg-h4 mb-4">Scoreboard</h1>
        <p v-for="scoreEntry, index in scores" :key="index" class="text-body-1">
            {{ scoreEntry.playerName }} - {{ scoreEntry.score }} - {{ "💩".repeat(scoreEntry.difficulty) }}
        </p>
    </v-sheet>
</template>
