<script lang="ts">
import QuizApiService from '@/services/QuizApiService';
import type { Question } from '@/types/quiz';
export default {
    methods: {
        createQuestion(question: Question) {
            QuizApiService.createQuestion(question).then((response) => {
                this.$router.push(`/admin/questions/${response.data.id}`);
            });
        }
    }
}
</script>

<template>
    <p>AdminQuestionNew</p>
</template>
