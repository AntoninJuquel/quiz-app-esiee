<script lang="ts">
//@ts-ignore
import EmojiPicker from 'vue3-emoji-picker'
import QuizApiService from '@/services/QuizApiService'
import type { Category } from '@/types/quiz'
export default {
  data() {
    return {
      editedCategory: {} as Category,
      rules: {
        required: (value: string) => !!value || 'Champ requis'
      }
    }
  },
  methods: {
    createCategory(category: Category) {
      if (!this.editedCategory.name || !this.editedCategory.emoji) {
        return
      }
      QuizApiService.createCategory(category).then(() => {
        // this.$router.push(`/admin/categories/${response.data.id}`)
        this.$router.push(`/admin`)
      })
    },
    onSelectEmoji(emoji: Record<string, string>) {
      console.log(emoji.i)
      this.editedCategory.emoji = emoji.i
    }
  },
  components: {
    EmojiPicker
  }
}
</script>

<template>
  <v-card class="mx-auto" max-width="700">
    <v-card-title>
      <v-form @submit.prevent="createCategory(editedCategory)">
        <v-text-field
          density="compact"
          variant="underlined"
          v-model="editedCategory.name"
          label="Nom"
          append-icon="mdi-check"
          @click:append="createCategory(editedCategory)"
          :rules="[rules.required]"
        >
          <template v-slot:prepend>
            <v-icon v-if="!editedCategory.emoji">mdi-emoticon</v-icon>
            <p v-else>{{ editedCategory.emoji }}</p>
          </template>
        </v-text-field>
      </v-form>
    </v-card-title>
    <EmojiPicker
      :native="true"
      @select="onSelectEmoji"
      :disable-skin-tones="true"
      :hide-group-names="true"
      class="ml-4 mb-4"
    />
  </v-card>
</template>
