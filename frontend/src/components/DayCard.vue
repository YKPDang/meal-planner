<script setup lang="ts">
import { computed } from 'vue'
import type { MealPlanEntry, Recipe } from '@/types/api'

const props = defineProps<{
  entry: MealPlanEntry
  recipes: Recipe[]
}>()

const emit = defineEmits<{
  assign: [day: string, recipeId: string]
  randomize: [day: string, mode: 'random' | 'smart' | 'filtered']
}>()

const weekdayName = computed(() => {
  const d = new Date(props.entry.day + 'T00:00:00')
  return d.toLocaleDateString(undefined, { weekday: 'long' })
})

const shortDate = computed(() => {
  const d = new Date(props.entry.day + 'T00:00:00')
  return d.toLocaleDateString(undefined, { month: 'short', day: 'numeric' })
})

const isPlanned = computed(() => !!props.entry.recipe)

const isToday = computed(() => {
  const today = new Date()
  const entryDate = new Date(props.entry.day + 'T00:00:00')
  return today.toDateString() === entryDate.toDateString()
})
</script>

<template>
  <v-card :class="['day-card', { 'day-card--planned': isPlanned, 'day-card--today': isToday }]"
    :elevation="isToday ? 4 : 1" rounded="lg">
    <!-- Day Header -->
    <div :class="['day-card__header', isPlanned ? 'bg-primary' : 'day-card__header--empty']">
      <div class="d-flex align-center justify-space-between px-4 py-3">
        <div>
          <div :class="['text-subtitle-1 font-weight-bold', { 'hero-text': isPlanned }]">
            {{ weekdayName }}
          </div>
          <div :class="['text-caption', isPlanned ? 'hero-text-muted' : 'text-medium-emphasis']">
            {{ shortDate }}
          </div>
        </div>
        <v-chip v-if="isToday" size="x-small" color="warning" variant="flat" class="font-weight-bold">
          TODAY
        </v-chip>
      </div>
    </div>

    <v-card-text class="pa-4">
      <!-- Recipe Info -->
      <div v-if="entry.recipe" class="mb-3">
        <div class="text-body-1 font-weight-medium mb-1">{{ entry.recipe.name }}</div>
        <div v-if="entry.recipe.description" class="text-body-2 text-medium-emphasis mb-2 description-preview">
          {{ entry.recipe.description }}
        </div>
        <div v-if="entry.recipe.tags?.length" class="d-flex flex-wrap ga-1">
          <v-chip v-for="tag in entry.recipe.tags" :key="tag" size="x-small" variant="tonal" color="primary">
            {{ tag }}
          </v-chip>
        </div>
      </div>
      <div v-else class="text-center py-4">
        <v-icon size="32" color="grey-lighten-1" class="mb-2">mdi-silverware-variant</v-icon>
        <div class="text-body-2 text-medium-emphasis">No meal planned</div>
      </div>

      <!-- Recipe selector -->
      <v-select :items="recipes" item-title="name" item-value="id" label="Select recipe" density="compact"
        variant="outlined" hide-details class="mb-3" :model-value="entry.recipe?.id ?? ''"
        @update:model-value="emit('assign', entry.day, String($event || ''))" />

      <!-- Randomize buttons -->
      <div class="d-flex flex-column ga-1">
        <v-btn variant="tonal" color="primary" size="small" density="comfortable" block
          prepend-icon="mdi-dice-3-outline" @click="emit('randomize', entry.day, 'random')">
          Random
        </v-btn>
        <v-btn variant="tonal" color="secondary" size="small" density="comfortable" block prepend-icon="mdi-brain"
          @click="emit('randomize', entry.day, 'smart')">
          Smart Random
        </v-btn>
        <v-btn variant="tonal" color="tertiary" size="small" density="comfortable" block
          prepend-icon="mdi-filter-outline" @click="emit('randomize', entry.day, 'filtered')">
          Filtered Random
        </v-btn>
      </div>
    </v-card-text>
  </v-card>
</template>

<style scoped>
.day-card {
  transition: transform 0.15s ease, box-shadow 0.15s ease;
  overflow: hidden;
}

.day-card:hover {
  transform: translateY(-2px);
}

.day-card--today {
  border: 2px solid rgb(var(--v-theme-primary));
}

.day-card__header {
  border-bottom: 1px solid rgba(var(--v-border-color), var(--v-border-opacity));
}

.day-card__header--empty {
  background: rgba(var(--v-theme-on-surface), 0.04);
}

.hero-text {
  color: rgba(255, 255, 255, 0.95);
}

.hero-text-muted {
  color: rgba(255, 255, 255, 0.7);
}

.description-preview {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>
