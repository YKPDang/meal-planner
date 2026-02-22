<script setup lang="ts">
import type { MealPlanEntry, Recipe } from '@/types/api'

defineProps<{
  entry: MealPlanEntry
  recipes: Recipe[]
}>()

const emit = defineEmits<{
  assign: [day: string, recipeId: string]
  randomize: [day: string, mode: 'random' | 'smart' | 'filtered']
}>()
</script>

<template>
  <v-card class="h-100">
    <v-card-text>
      <div class="d-flex align-center justify-space-between mb-2">
        <div class="text-subtitle1 font-weight-medium">{{ entry.day }}</div>
        <v-chip size="small" color="secondary" variant="tonal">
          {{ entry.recipe?.name || 'Unplanned' }}
        </v-chip>
      </div>

      <v-select :items="recipes" item-title="name" item-value="id" label="Select recipe" density="compact"
        :model-value="entry.recipe?.id ?? ''" @update:model-value="emit('assign', entry.day, String($event || ''))" />

      <div class="d-flex flex-column gap-2 mt-3">
        <v-btn variant="outlined" color="primary" size="small" @click="emit('randomize', entry.day, 'random')">
          Random
        </v-btn>
        <v-btn variant="outlined" color="primary" size="small" @click="emit('randomize', entry.day, 'smart')">
          Smart Random
        </v-btn>
        <v-btn variant="flat" color="secondary" size="small" @click="emit('randomize', entry.day, 'filtered')">
          Filtered Random
        </v-btn>
      </div>
    </v-card-text>
  </v-card>
</template>
