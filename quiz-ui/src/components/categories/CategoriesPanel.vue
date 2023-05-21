<script lang="ts">
import QuizApiService from '@/services/QuizApiService'
import type { Category } from '@/types/quiz'

export default {
  data() {
    return {
      categories: [] as Category[]
    }
  },
  methods: {
    async getCategories() {
      const categories = await QuizApiService.getCategories()
      this.categories = categories.data
    }
  },
  async created() {
    await this.getCategories()
  }
}
</script>

<template>
  <v-expansion-panel>
    <v-expansion-panel-title>
      <v-card-title>Categories</v-card-title>
      <v-btn icon @click.stop="" color="primary">
        <v-icon>mdi-plus</v-icon>
      </v-btn>
    </v-expansion-panel-title>
    <v-expansion-panel-text>
      <v-table density="compact">
        <thead>
          <tr>
            <th class="text-left">Emoji</th>
            <th class="text-left">Nom</th>
            <th class="text-right">
              <v-btn icon>
                <v-icon>mdi-pen</v-icon>
              </v-btn>
            </th>
            <th class="text-right">
              <v-btn icon>
                <v-icon color="error">mdi-delete</v-icon>
              </v-btn>
            </th>
          </tr>
        </thead>
        <tbody v-if="categories.length > 0">
          <tr v-for="category in categories" :key="category.id">
            <td>{{ category.emoji }}</td>
            <td>{{ category.name }}</td>
            <td class="text-right">
              <v-btn icon>
                <v-icon>mdi-pen</v-icon>
              </v-btn>
            </td>
            <td class="text-right">
              <v-btn icon>
                <v-icon color="error">mdi-delete</v-icon>
              </v-btn>
            </td>
          </tr>
        </tbody>
      </v-table>

      <v-btn color="error">Tout supprimer</v-btn>
    </v-expansion-panel-text>
  </v-expansion-panel>
</template>
