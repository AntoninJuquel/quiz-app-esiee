<script lang="ts">
import QuizApiService from '@/services/QuizApiService';
import ScoreboardDisplay from '@/components/ScoreboardDisplay.vue';
import type { Score } from '@/types/quiz';
export default {
    data() {
        return {
            scores: [] as Score[]
        }
    },
    methods: {
        async getScores() {
            await QuizApiService.getQuizInfo().then((response) => {
                this.scores = response.data.scores;
            });
        },
        async resetScores() {
            await QuizApiService.deleteAllParticipations().then(() => {
                this.getScores();
            });
        }
    },
    created() {
        this.getScores();
    },
    components: {
        ScoreboardDisplay
    }
}
</script>

<template>
    <v-sheet class="d-flex flex-column align-center">
        <ScoreboardDisplay :scores="scores" />
        <v-btn @click="resetScores">Reset Scores</v-btn>
    </v-sheet>
</template>
