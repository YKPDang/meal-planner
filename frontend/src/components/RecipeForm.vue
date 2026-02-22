<script setup lang="ts">
import type { PropType } from 'vue'

import type { RecipeDraft } from '@/types/api'

defineProps({
  model: {
    type: Object as PropType<RecipeDraft>,
    required: true
  },
  loading: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits<{
  (event: 'save'): void
}>()
</script>

<template>
  <v-card elevation="2" class="mb-6">
    <v-card-title class="text-h6">Add Recipe</v-card-title>
    <v-card-text>
      <v-form @submit.prevent="emit('save')" class="d-flex flex-column gap-4">
        <v-text-field v-model="model.name" label="Recipe name" variant="outlined" required />
        <v-textarea v-model="model.description" label="Description" variant="outlined" rows="2" />
        <v-textarea
          v-model="model.ingredientsText"
          label="Ingredients (one per line, example: 200g pasta)"
          variant="outlined"
          rows="4"
        />
        <v-text-field v-model="model.tagsText" label="Tags (comma separated)" variant="outlined" />
        <div class="d-flex justify-end">
          <v-btn color="primary" variant="flat" type="submit" :loading="loading">
            Save Recipe
          </v-btn>
        </div>
      </v-form>
    </v-card-text>
  </v-card>
</template>
