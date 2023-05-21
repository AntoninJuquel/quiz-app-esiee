<script lang="ts">
import CategoriesPanel from '@/components/categories/CategoriesPanel.vue'
import QuestionsPanel from '@/components/questions/QuestionsPanel.vue'
import ParticipationPanel from '@/components/participations/ParticipationsPanel.vue'

import type { Category } from '@/types/quiz'

export default {
  data() {
    return {
      categories: [] as Category[]
    }
  },
  methods: {},
  async created() {},
  components: {
    CategoriesPanel,
    QuestionsPanel,
    ParticipationPanel
  }
}
</script>

<template>
  <v-container class="mt-8 rounded-lg">
    <v-expansion-panels variant="popout">
      <CategoriesPanel v-model="categories" />
      <QuestionsPanel :categories="categories" />
      <ParticipationPanel />
    </v-expansion-panels>
  </v-container>
</template>
