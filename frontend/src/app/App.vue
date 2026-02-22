<script setup lang="ts">
import { computed } from 'vue'

import MealPlanBoard from '@/components/MealPlanBoard.vue'
import RecipeForm from '@/components/RecipeForm.vue'
import RecipeList from '@/components/RecipeList.vue'
import TagList from '@/components/TagList.vue'
import { useMealPlan } from '@/composables/useMealPlan'

const {
  recipes,
  tags,
  mealPlan,
  status,
  isLoading,
  lookbackDays,
  filterTagsInput,
  newRecipe,
  weekLabel,
  saveRecipe,
  assignRecipe,
  randomize,
  navigateWeek
} = useMealPlan()

const hasStatus = computed(() => Boolean(status.value))
</script>

<template>
  <v-app class="app-shell">
    <v-main>
      <v-container class="py-10" fluid>
        <v-row justify="center">
          <v-col cols="12" md="10" lg="8">
            <v-card elevation="1" class="mb-8">
              <v-card-text>
                <div class="section-title">
                  <div>
                    <h1 class="text-h4 font-weight-bold">Meal Planner</h1>
                    <p class="subtitle">Plan, randomize, and keep your favorite recipes in one place.</p>
                  </div>
                  <v-chip color="primary" variant="flat">Weekly view</v-chip>
                </div>
              </v-card-text>
            </v-card>

            <v-alert
              v-if="hasStatus"
              type="info"
              variant="tonal"
              class="mb-6"
            >
              {{ status }}
            </v-alert>

            <RecipeForm :model="newRecipe" :loading="isLoading" @save="saveRecipe" />

            <MealPlanBoard
              v-model:lookback-days="lookbackDays"
              v-model:filter-tags-input="filterTagsInput"
              :meal-plan="mealPlan"
              :recipes="recipes"
              :week-label="weekLabel"
              :loading="isLoading"
              @assign="assignRecipe"
              @randomize="randomize"
              @navigate="navigateWeek"
            />

            <v-row class="mt-6" dense>
              <v-col cols="12" md="7">
                <RecipeList :recipes="recipes" />
              </v-col>
              <v-col cols="12" md="5">
                <TagList :tags="tags" />
              </v-col>
            </v-row>
          </v-col>
        </v-row>
      </v-container>
    </v-main>
  </v-app>
</template>
