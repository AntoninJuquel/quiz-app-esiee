<script lang="ts">
import CategoriesPanel from '@/components/categories/CategoriesPanel.vue'
import QuestionsPanel from '@/components/questions/QuestionsPanel.vue'
import ParticipationPanel from '@/components/ParticipationPanel.vue'

export default {
  data() {
    return {}
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
      <CategoriesPanel />
      <QuestionsPanel />
      <ParticipationPanel />
    </v-expansion-panels>
  </v-container>
</template>
