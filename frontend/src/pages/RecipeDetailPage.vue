<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import type { Recipe } from '@/types/api'
import { useRecipes } from '@/composables/useRecipes'

const route = useRoute()
const router = useRouter()
const { getRecipe } = useRecipes()

const recipe = ref<Recipe | null>(null)
const isLoading = ref(false)

const recipeId = computed(() => route.params.id as string)

onMounted(async () => {
  isLoading.value = true
  try {
    recipe.value = await getRecipe(recipeId.value)
  } finally {
    isLoading.value = false
  }
})

const goToEdit = () => {
  router.push({ name: 'RecipeEdit', params: { id: recipeId.value } })
}

const goBack = () => {
  router.push({ name: 'Recipes' })
}
</script>

<template>
  <v-container class="py-10">
    <v-row v-if="isLoading" class="justify-center">
      <v-progress-circular indeterminate />
    </v-row>

    <v-row v-else-if="recipe" class="mb-6">
      <v-col cols="12" md="8">
        <div class="mb-6">
          <h1 class="text-h4 font-weight-bold mb-2">{{ recipe.name }}</h1>
          <p class="text-body1">{{ recipe.description }}</p>
        </div>

        <v-card class="mb-6">
          <v-card-item>
            <div class="text-subtitle1 font-weight-bold">Ingredients</div>
          </v-card-item>
          <v-card-text>
            <ul class="ps-5">
              <li v-for="(ingredient, idx) in recipe.ingredients" :key="idx" class="mb-2">
                {{ ingredient.name }}
              </li>
            </ul>
          </v-card-text>
        </v-card>

        <v-card v-if="recipe.tags.length > 0" class="mb-6">
          <v-card-item>
            <div class="text-subtitle1 font-weight-bold">Tags</div>
          </v-card-item>
          <v-card-text>
            <div class="chip-wrap">
              <v-chip v-for="tag in recipe.tags" :key="tag.id" variant="tonal">
                {{ tag.name }}
              </v-chip>
            </div>
          </v-card-text>
        </v-card>

        <v-row class="gap-2">
          <v-btn @click="goToEdit" color="primary" prepend-icon="mdi-pencil">
            Edit
          </v-btn>
          <v-btn @click="goBack" variant="tonal" prepend-icon="mdi-arrow-left">
            Back to Recipes
          </v-btn>
        </v-row>
      </v-col>
    </v-row>

    <v-row v-else class="justify-center mt-6">
      <v-col cols="12" class="text-center">
        <p class="text-body2 text-medium-emphasis">Recipe not found</p>
      </v-col>
    </v-row>
  </v-container>
</template>
