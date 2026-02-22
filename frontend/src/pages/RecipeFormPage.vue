<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import type { RecipeDraft } from '@/types/api'
import { useRecipes } from '@/composables/useRecipes'

const route = useRoute()
const router = useRouter()
const { saveRecipe, updateRecipe, getRecipe } = useRecipes()

const isEditMode = computed(() => Boolean(route.params.id))
const recipeId = computed(() => route.params.id as string)

const formData = ref<RecipeDraft>({
  name: '',
  description: '',
  ingredientsText: '',
  tagsText: ''
})

const isLoading = ref(false)
const isSaving = ref(false)

onMounted(async () => {
  if (isEditMode.value) {
    isLoading.value = true
    try {
      const recipe = await getRecipe(recipeId.value)
      formData.value = {
        name: recipe.name,
        description: recipe.description,
        ingredientsText: recipe.ingredients.map(i => i.item).join('\n'),
        tagsText: recipe.tags.join(', ')
      }
    } finally {
      isLoading.value = false
    }
  }
})

const handleSave = async () => {
  isSaving.value = true
  try {
    if (isEditMode.value) {
      await updateRecipe(recipeId.value, formData.value)
      router.push({ name: 'RecipeDetail', params: { id: recipeId.value } })
    } else {
      await saveRecipe(formData.value)
      router.push({ name: 'Recipes' })
    }
  } finally {
    isSaving.value = false
  }
}

const handleCancel = () => {
  if (isEditMode.value) {
    router.push({ name: 'RecipeDetail', params: { id: recipeId.value } })
  } else {
    router.push({ name: 'Recipes' })
  }
}
</script>

<template>
  <v-container class="py-10">
    <v-row v-if="isLoading" class="justify-center">
      <v-progress-circular indeterminate />
    </v-row>

    <v-row v-else>
      <v-col cols="12" md="8">
        <h1 class="text-h4 font-weight-bold mb-6">
          {{ isEditMode ? 'Edit Recipe' : 'Add New Recipe' }}
        </h1>

        <v-form @submit.prevent="handleSave">
          <v-text-field v-model="formData.name" label="Recipe Name" placeholder="Enter recipe name" required
            class="mb-4" />

          <v-textarea v-model="formData.description" label="Description" placeholder="Enter recipe description"
            class="mb-4" />

          <v-textarea v-model="formData.ingredientsText" label="Ingredients (one per line)"
            placeholder="Ingredient 1&#10;Ingredient 2&#10;..." class="mb-4" />

          <v-text-field v-model="formData.tagsText" label="Tags (comma-separated)" placeholder="tag1, tag2, tag3"
            class="mb-6" />

          <v-row class="gap-2">
            <v-btn type="submit" color="primary" :loading="isSaving">
              {{ isEditMode ? 'Update Recipe' : 'Add Recipe' }}
            </v-btn>
            <v-btn @click="handleCancel" variant="tonal">
              Cancel
            </v-btn>
          </v-row>
        </v-form>
      </v-col>
    </v-row>
  </v-container>
</template>
