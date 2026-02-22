<script setup lang="ts">
import type { PropType } from 'vue'

import DayCard from './DayCard.vue'
import type { MealPlanEntry, Recipe } from '@/types/api'

const props = defineProps({
  mealPlan: {
    type: Array as PropType<MealPlanEntry[]>,
    required: true
  },
  recipes: {
    type: Array as PropType<Recipe[]>,
    required: true
  },
  weekLabel: {
    type: String,
    required: true
  },
  loading: {
    type: Boolean,
    default: false
  }
})

const lookbackDays = defineModel<number>('lookbackDays', { default: 7 })
const filterTagsInput = defineModel<string>('filterTagsInput', { default: '' })

const emit = defineEmits<{
  (event: 'assign', day: string, recipeId: string): void
  (event: 'randomize', day: string, mode: 'random' | 'smart' | 'filtered'): void
  (event: 'navigate', delta: number): void
}>()
</script>

<template>
  <v-card class="mb-6">
    <v-card-text>
      <div class="section-title mb-4">
        <div>
          <h2 class="text-h6">Week Plan</h2>
          <p class="text-body2 text-medium-emphasis mb-0">Week: {{ weekLabel }}</p>
        </div>
        <div class="d-flex gap-2">
          <v-btn variant="text" @click="emit('navigate', -1)">Previous</v-btn>
          <v-btn variant="text" @click="emit('navigate', 1)">Next</v-btn>
        </div>
      </div>

      <v-row dense class="mb-4">
        <v-col cols="12" md="5">
          <v-text-field v-model.number="lookbackDays" type="number" min="1" label="Smart lookback days" />
        </v-col>
        <v-col cols="12" md="7">
          <v-text-field v-model="filterTagsInput" label="Filter tags (pasta, quick-lunch)" />
        </v-col>
      </v-row>

      <v-row dense>
        <v-col v-for="entry in props.mealPlan" :key="entry.day" cols="12" md="6" lg="4">
          <DayCard :entry="entry" :recipes="props.recipes" @assign="(day, recipeId) => emit('assign', day, recipeId)"
            @randomize="(day, mode) => emit('randomize', day, mode)" />
        </v-col>
      </v-row>

      <v-skeleton-loader v-if="props.loading" type="article" class="mt-4" />
    </v-card-text>
  </v-card>
</template>
