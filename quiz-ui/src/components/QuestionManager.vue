<script lang="ts">
import QuestionDipslay from '@/components/QuestionDisplay.vue';
import type { Question } from '@/types/quiz';

export default {
    data() {
        return {
            currentQuestionPosition: 1,
            totalNumberOfQuestion: 0,
            currentQuestion: {} as Question,
        };
    },
    methods: {
        loadQuestionByPosition() {
            this.currentQuestion = {
                image: "https://picsum.photos/200/300",
                title: "Question 1",
                text: 'What is the capital of France?',
                possibleAnswers: [
                    "Paris",
                    "London",
                    "Berlin",
                    "Rome",
                ],
                correctAnswerIndex: 0,
            }
        },
        answerClickedHandler(answerIndex: number) {
            console.log('answer clicked', answerIndex)
        },
        endQuiz() {

        }
    },
    created() {
        this.loadQuestionByPosition();
    },
    components: {
        QuestionDisplay: QuestionDipslay,
    },
};
</script>

<template>
    <h1>Question {{ currentQuestionPosition }} / {{ totalNumberOfQuestion }}</h1>
    <QuestionDisplay :question="currentQuestion" @answer-selected="answerClickedHandler" />
</template>

<style scoped></style>
