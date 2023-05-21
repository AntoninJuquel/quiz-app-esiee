<script lang="ts">
//@ts-ignore
import EmojiPicker from 'vue3-emoji-picker'
import type { Category } from '@/types/quiz'

export default {
  props: {
    modelValue: {
      type: Object as () => Category | null,
      required: true
    }
  },
  emits: ['update:modelValue', 'save'],
  methods: {
    onSelectEmoji(emoji: Record<string, string>) {
      this.$emit('update:modelValue', { ...this.modelValue, emoji: emoji.i })
    },
    close() {
      this.$emit('update:modelValue', null)
    },
    save() {
      if (this.modelValue === null) {
        return
      }

      if (this.modelValue.name === '' || this.modelValue.emoji === '') {
        return
      }

      this.$emit('save')
    }
  },
  computed: {
    creating() {
      return this.modelValue?.id === -1
    }
  },
  components: {
    EmojiPicker
  }
}
</script>

<template>
  <v-dialog :model-value="modelValue !== null" max-width="500" @update:model-value="close">
    <v-card>
      <v-card-title class="text-h5">
        <span v-if="creating">Nouvelle Categorie</span>
        <span v-else>Modifier Categorie</span>
      </v-card-title>
      <v-card-text>
        <v-form @submit.prevent="save">
          <v-text-field
            :model-value="modelValue?.name"
            @input="$emit('update:modelValue', { ...modelValue, name: $event.target.value })"
            label="Name"
            required
          >
            <template #prepend>
              <span class="mr-2">{{ modelValue?.emoji }}</span>
            </template>
          </v-text-field>
          <EmojiPicker
            :native="true"
            @select="onSelectEmoji"
            :disable-skin-tones="true"
            :hide-group-names="true"
            class="mx-auto mb-4"
          />
        </v-form>
      </v-card-text>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn color="primary" @click="close">Cancel</v-btn>
        <v-btn color="primary" @click="save">Save</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>
