<script setup lang="ts">
import { computed, onMounted } from 'vue'
import MealPlanBoard from '@/components/MealPlanBoard.vue'
import { useMealPlan } from '@/composables/useMealPlan'
import { useRecipes } from '@/composables/useRecipes'

const mealPlanComposable = useMealPlan()
const recipesComposable = useRecipes()

const {
  mealPlan,
  status,
  isLoading,
  lookbackDays,
  filterTagsInput,
  weekLabel,
  assignRecipe,
  randomize,
  navigateWeek,
  loadMealPlan
} = mealPlanComposable

const { recipes } = recipesComposable

const hasStatus = computed(() => Boolean(status.value))

onMounted(async () => {
  await Promise.all([
    loadMealPlan(),
    recipesComposable.loadRecipes()
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

        <MealPlanBoard v-model:lookback-days="lookbackDays" v-model:filter-tags-input="filterTagsInput"
          :meal-plan="mealPlan" :recipes="recipes" :week-label="weekLabel" :loading="isLoading" @assign="assignRecipe"
          @randomize="randomize" @navigate="navigateWeek" />
      </v-col>
    </v-row>
  </v-container>
</template>
