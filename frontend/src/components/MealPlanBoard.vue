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

const emit = defineEmits<{
  (event: 'assign', day: string, recipeId: string): void
  (event: 'randomize', day: string, mode: 'random' | 'smart' | 'filtered'): void
  (event: 'navigate', delta: number): void
  (event: 'clear'): void
}>()
</script>

<template>
  <div>
    <!-- Week Navigation -->
    <div class="d-flex align-center justify-space-between mb-5">
      <v-btn variant="tonal" color="primary" prepend-icon="mdi-chevron-left" @click="emit('navigate', -1)">
        Previous
      </v-btn>
      <div class="text-center">
        <div class="text-h6 font-weight-bold">{{ weekLabel }}</div>
      </div>
      <v-btn variant="tonal" color="primary" append-icon="mdi-chevron-right" @click="emit('navigate', 1)">
        Next
      </v-btn>
    </div>

    <!-- Clear Week Button -->
    <div class="d-flex justify-end mb-4">
      <v-btn variant="tonal" color="error" size="small" prepend-icon="mdi-eraser" @click="emit('clear')">
        Clear Week
      </v-btn>
    </div>

    <!-- Day Cards Grid -->
    <v-row>
      <v-col v-for="entry in props.mealPlan" :key="entry.day" cols="12" sm="6" lg="4" xl="3">
        <DayCard :entry="entry" :recipes="props.recipes" @assign="(day, recipeId) => emit('assign', day, recipeId)"
          @randomize="(day, mode) => emit('randomize', day, mode)" />
      </v-col>
    </v-row>

    <div v-if="props.loading" class="d-flex justify-center py-8">
      <v-progress-circular indeterminate color="primary" size="48" />
    </div>
  </div>
</template>
