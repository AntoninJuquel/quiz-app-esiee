<script lang="ts">
import QuizApiService from '@/services/QuizApiService'
import type { Category } from '@/types/quiz'

import EditCategoryDialog from './EditCategoryDialog.vue'

export default {
  props: {
    modelValue: {
      type: Array as () => Category[],
      required: true
    }
  },
  emits: ['update:modelValue'],
  data() {
    return {
      categories: [] as Category[],
      editCategory: null as Category | null
    }
  },
  methods: {
    async getCategories() {
      const categories = await QuizApiService.getCategories()
      this.categories = categories.data
      this.$emit('update:modelValue', this.categories)
    },
    async saveCategory() {
      if (this.editCategory === null) return
      if (this.editCategory.id === -1) {
        await QuizApiService.createCategory(this.editCategory)
      } else {
        await QuizApiService.updateCategory(this.editCategory)
      }
      await this.getCategories()
      this.editCategory = null
    },
    async deleteCategory(category: Category) {
      await QuizApiService.deleteCategory(category)
      this.categories = this.categories.filter((c) => c.id !== category.id)
      this.$emit('update:modelValue', this.categories)
    }
  },
  async created() {
    await this.getCategories()
  },
  components: {
    EditCategoryDialog
  }
}
</script>

<template>
  <v-expansion-panel>
    <v-expansion-panel-title>
      <v-card-title>Categories</v-card-title>
    </v-expansion-panel-title>
    <v-expansion-panel-text>
      <v-card-actions>
        <v-btn
          color="primary"
          @click="
            editCategory = {
              id: -1,
              name: '',
              emoji: ''
            }
          "
          >Nouvelle catégorie</v-btn
        >
      </v-card-actions>

      <v-table density="compact">
        <thead>
          <tr>
            <th class="text-left">Emoji</th>
            <th class="text-left">Nom</th>
            <th class="text-right">Action</th>
          </tr>
        </thead>
        <tbody v-if="categories.length > 0">
          <v-hover v-for="category in categories" :key="category.id">
            <template v-slot:default="{ isHovering, props }">
              <tr
                v-bind="props"
                @click="editCategory = category"
                style="cursor: pointer"
                :class="{
                  'bg-background darken-2': isHovering
                }"
              >
                <td>{{ category.emoji }}</td>
                <td>{{ category.name }}</td>
                <td class="text-right">
                  <v-btn icon @click.stop="deleteCategory(category)">
                    <v-icon color="error">mdi-delete</v-icon>
                  </v-btn>
                </td>
              </tr>
            </template>
          </v-hover>
        </tbody>
      </v-table>
    </v-expansion-panel-text>
  </v-expansion-panel>

  <EditCategoryDialog v-model="editCategory" @save="saveCategory" />
</template>
