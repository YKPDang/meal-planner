<script setup lang="ts">
import type { PropType } from 'vue'

import type { Recipe } from '@/types/api'

defineProps({
  recipes: {
    type: Array as PropType<Recipe[]>,
    required: true
  }
})
</script>

<template>
  <v-card elevation="1" class="h-100">
    <v-card-title class="text-h6">Recipes</v-card-title>
    <v-divider />
    <v-card-text>
      <v-list density="comfortable">
        <v-list-item v-for="recipe in recipes" :key="recipe.id">
          <v-list-item-title class="font-weight-medium">
            {{ recipe.name }}
          </v-list-item-title>
          <v-list-item-subtitle>
            {{ recipe.description || 'No description' }}
          </v-list-item-subtitle>
          <div class="chip-wrap mt-2">
            <v-chip
              v-for="tag in recipe.tags"
              :key="tag"
              size="small"
              color="primary"
              variant="tonal"
            >
              {{ tag }}
            </v-chip>
            <v-chip v-if="recipe.tags.length === 0" size="small" variant="outlined">
              No tags
            </v-chip>
          </div>
        </v-list-item>
      </v-list>
    </v-card-text>
  </v-card>
</template>
