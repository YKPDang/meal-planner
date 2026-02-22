<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import MealPlanBoard from '@/components/MealPlanBoard.vue'
import { useMealPlan } from '@/composables/useMealPlan'
import { useRecipes } from '@/composables/useRecipes'
import { useTags } from '@/composables/useTags'

const mealPlanComposable = useMealPlan()
const recipesComposable = useRecipes()
const tagsComposable = useTags()

const {
  mealPlan,
  status,
  isLoading,
  lookbackDays,
  weekLabel,
  assignRecipe,
  randomize,
  navigateWeek,
  loadMealPlan
} = mealPlanComposable

const { recipes } = recipesComposable
const { tags } = tagsComposable

const filterTags = ref<string[]>([])
const hasStatus = computed(() => Boolean(status.value))

// Convert filterTags array to comma-separated string for randomize function
const filterTagsInput = computed(() => filterTags.value.join(', '))

// Wrapper for randomize that uses the computed filterTagsInput
const handleRandomize = (day: string, mode: 'random' | 'smart' | 'filtered') => {
  randomize(day, mode)
}

onMounted(async () => {
  await Promise.all([
    loadMealPlan(),
    recipesComposable.loadRecipes(),
    tagsComposable.loadTags()
  ])
})
</script>

<template>
  <v-container class="py-10" fluid>
    <v-row justify="center">
      <v-col cols="12" md="10" lg="8">
        <v-card class="mb-8">
          <v-card-text>
            <div class="d-flex align-center justify-space-between">
              <div>
                <h1 class="text-h4 font-weight-bold">Weekly Meal Plan</h1>
                <p class="text-body2 text-medium-emphasis">Plan, randomize, and organize your meals for the week.</p>
              </div>
              <v-btn to="/recipes/new" color="primary" prepend-icon="mdi-plus">
                Add Recipe
              </v-btn>
            </div>
          </v-card-text>
        </v-card>

        <v-alert v-if="hasStatus" type="info" variant="tonal" class="mb-6">
          {{ status }}
        </v-alert>

        <!-- Filter controls -->
        <v-row dense class="mb-4">
          <v-col cols="12" md="5">
            <v-text-field
              v-model.number="lookbackDays"
              type="number"
              min="1"
              label="Smart lookback days"
            />
          </v-col>
          <v-col cols="12" md="7">
            <v-select
              v-model="filterTags"
              :items="tags"
              item-title="name"
              item-value="name"
              label="Filter by tags"
              multiple
              chips
              clearable
            />
          </v-col>
        </v-row>

        <MealPlanBoard
          :meal-plan="mealPlan"
          :recipes="recipes"
          :week-label="weekLabel"
          :loading="isLoading"
          @assign="assignRecipe"
          @randomize="handleRandomize"
          @navigate="navigateWeek"
        />
      </v-col>
    </v-row>
  </v-container>
</template>
