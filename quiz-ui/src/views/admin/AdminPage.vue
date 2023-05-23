<script lang="ts">
import { version } from '@/../package.json'

import QuizApiService from '@/services/QuizApiService'

import CategoriesPanel from '@/components/categories/CategoriesPanel.vue'
import QuestionsPanel from '@/components/questions/QuestionsPanel.vue'
import ParticipationPanel from '@/components/participations/ParticipationsPanel.vue'

import type { Category } from '@/types/quiz'

export default {
  data() {
    return {
      categories: [] as Category[],
      key: 0,
      applicationVersion: version
    }
  },
  methods: {
    async rebuildDatabase() {
      await QuizApiService.rebuildDatabase()
      this.key++
    }
  },
  async created() {},
  components: {
    CategoriesPanel,
    QuestionsPanel,
    ParticipationPanel
  }
}
</script>

<template>
  <v-container class="mt-8 rounded-lg" :key="key">
    <v-expansion-panels variant="popout">
      <CategoriesPanel v-model="categories" />
      <QuestionsPanel :categories="categories" />
      <ParticipationPanel />
    </v-expansion-panels>
  </v-container>

  <v-container class="d-flex justify-center mt-8 rounded-lg">
    <v-btn color="primary" @click="rebuildDatabase">Rebuild Database</v-btn>
  </v-container>

  <v-footer app dark height="50">
    <v-spacer></v-spacer>
    <span class="white--text">Version {{ applicationVersion }}</span>
  </v-footer>
</template>
