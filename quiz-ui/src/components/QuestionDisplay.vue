<script lang="ts">
import type { Question } from '@/types/quiz';
export default {
    name: 'QuestionDisplay',
    props: {
        question: {
            type: Object as () => Question,
            required: true,
        },
    },
    emits: ['answer-selected'],
}
</script>

<template>
    <img v-if="question.image" :src="question.image" />
    <h1>{{ question.title }}</h1>
    <p>{{ question.text }}</p>
    <v-btn v-for="(answer, index) in question.possibleAnswers" :key="answer" block
        @click="$emit('answer-selected', index)">{{
            answer
        }}</v-btn>
</template>

<style scoped></style>
