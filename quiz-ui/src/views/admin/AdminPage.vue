<script lang="ts">
import { format } from 'date-fns';
import type { Category, Question } from '@/types/quiz';
import QuizApiService from '@/services/QuizApiService';
export default {
  data() {
    return {
      drawer: false,
      questions: [] as Question[],
      categories: [] as Category[],
      date: format(new Date(), 'yyyy-MM-dd'),
    }
  },
  watch: {
    "$route": function () {
      this.drawer = QuizApiService.authenticated();
    }
  },
  methods: {
    async getQuestions() {
      await QuizApiService.getQuestions(this.date).then((response) => {
        this.questions = response.data;
      });
    },
    async deleteQuestion(question: Question) {
      QuizApiService.deleteQuestion(question).then((response) => {
        this.getQuestions();
      })
    },
    async getCategories() {
      await QuizApiService.getCategories().then((response) => {
        this.categories = response.data;
      });
    },
    async deleteCategory(category: Category) {
      QuizApiService.deleteCategory(category).then((response) => {
        this.getCategories();
      })
    },
    logout() {
      QuizApiService.logout();
      this.$router.push('/admin/login');
    }
  },
  created() {
    this.getQuestions();
    this.getCategories();
    this.drawer = QuizApiService.authenticated();
  },
}
</script>

<template>
  <v-layout>
    <v-navigation-drawer v-model="drawer" location="right" app>
      <v-list>
        <v-list-item>
          <input type="date" v-model="date" @change="getQuestions" />
        </v-list-item>
        <v-list-item title="Scoreboard" to="/admin/scoreboard"></v-list-item>
        <v-list-group value="Questions">
          <template v-slot:activator="{ props }">
            <v-list-item v-bind="props" title="Questions"></v-list-item>
          </template>
          <v-list-item v-for="question in questions" :key="question.id" :to="`/admin/questions/${question.id}`"
            :title="`#${question.id} ${question.title}`" nav>
            <template v-slot:append>
              <v-icon color="error" @click="deleteQuestion(question)">mdi-delete</v-icon>
            </template>
          </v-list-item>
        </v-list-group>

        <v-list-group value="Categories">
          <template v-slot:activator="{ props }">
            <v-list-item v-bind="props" title="Categories"></v-list-item>
          </template>
          <v-list-item v-for="category in categories" :key="category.id" :title="`${category.emoji} ${category.name}`"
            nav>
            <template v-slot:append>
              <v-icon color="error" @click="deleteCategory(category)">mdi-delete</v-icon>
            </template>
          </v-list-item>
        </v-list-group>
      </v-list>

      <template v-slot:append>
        <v-list class="pa-2 ">
          <v-btn block to="/admin/questions/new" color="primary" class="mb-4">
            Nouvelle question
          </v-btn>
          <v-btn block @click="logout" color="error">
            Logout
          </v-btn>
        </v-list>
      </template>
    </v-navigation-drawer>
  </v-layout>

  <router-view />
</template>
