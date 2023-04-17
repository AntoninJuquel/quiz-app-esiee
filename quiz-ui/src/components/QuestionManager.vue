<script lang="ts">
import quizApiService from "@/services/QuizApiService";
import QuestionDipslay from '@/components/QuestionDisplay.vue';
import type { Question } from '@/types/quiz';

export default {
    data() {
        return {
            currentQuestionPosition: 1,
            totalNumberOfQuestions: 0,
            currentQuestion: {} as Question,
        };
    },
    methods: {
        async loadQuestionByPosition() {
            await quizApiService.getQuestion(this.currentQuestionPosition).then(response => {
                [this.currentQuestion] = response.data;
                this.totalNumberOfQuestions = 4;
            }).catch(error => {
                console.log(error);
            });
        },
        answerClickedHandler(answerIndex: number) {
            if(this.currentQuestionPosition < this.totalNumberOfQuestions) {
                this.currentQuestionPosition++;
                this.loadQuestionByPosition();
            } else {
                this.endQuiz();
            }
        },
        endQuiz() {
            this.$router.push('/your-score');
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
    <h1>Question {{ currentQuestionPosition }} / {{ totalNumberOfQuestions }}</h1>
    <QuestionDisplay :question="currentQuestion" @answer-selected="answerClickedHandler" />
</template>

<style scoped></style>
