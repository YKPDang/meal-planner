<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import RecipeCard from '@/components/RecipeCard.vue'
import { useRecipes } from '@/composables/useRecipes'
import { useTags } from '@/composables/useTags'
import { parseTags } from '@/utils/parse'

const router = useRouter()
const recipesComposable = useRecipes()
const tagsComposable = useTags()

const { recipes, loadRecipes } = recipesComposable
const { tags } = tagsComposable

const searchQuery = ref('')
const selectedTags = ref<string[]>([])

const filteredRecipes = computed(() => {
  return recipes.value.filter(recipe => {
    const matchesSearch = !searchQuery.value ||
      recipe.name.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
      recipe.description.toLowerCase().includes(searchQuery.value.toLowerCase())

    const matchesTags = selectedTags.value.length === 0 ||
      recipe.tags.some(tag => selectedTags.value.includes(String(tag.id)))

    return matchesSearch && matchesTags
  })
})

onMounted(async () => {
  await Promise.all([
    loadRecipes(),
    tagsComposable.loadTags()
  ])
})

const goToRecipe = (id: number) => {
  router.push({ name: 'RecipeDetail', params: { id } })
}

const toggleTag = (tagId: string) => {
  if (selectedTags.value.includes(tagId)) {
    selectedTags.value = selectedTags.value.filter(id => id !== tagId)
  } else {
    selectedTags.value.push(tagId)
  }
}
</script>

<template>
  <v-container class="py-10" fluid>
    <v-row class="mb-6">
      <v-col cols="12">
        <h1 class="text-h4 font-weight-bold mb-4">Recipes</h1>

        <v-row class="gap-4">
          <v-col cols="12" sm="8">
            <v-text-field v-model="searchQuery" placeholder="Search recipes..." prepend-inner-icon="mdi-magnify"
              clearable />
          </v-col>
          <v-col cols="12" sm="4" class="d-flex align-center">
            <v-btn to="/recipes/new" color="primary" prepend-icon="mdi-plus" class="w-100">
              Add Recipe
            </v-btn>
          </v-col>
        </v-row>

        <v-row v-if="tags.length > 0" class="mt-2">
          <v-col cols="12">
            <p class="text-body2 text-medium-emphasis mb-2">Filter by tags:</p>
            <div class="chip-wrap">
              <v-chip v-for="tag in tags" :key="tag.id"
                :color="selectedTags.includes(String(tag.id)) ? 'primary' : undefined" variant="tonal"
                @click="toggleTag(String(tag.id))">
                {{ tag.name }}
              </v-chip>
            </div>
          </v-col>
        </v-row>
      </v-col>
    </v-row>

    <v-row v-if="filteredRecipes.length > 0" class="gap-4">
      <v-col v-for="recipe in filteredRecipes" :key="recipe.id" cols="12" sm="6" md="4" lg="3">
        <RecipeCard :recipe="recipe" @click="goToRecipe(recipe.id)" />
      </v-col>
    </v-row>

    <v-row v-else class="mt-6">
      <v-col cols="12" class="text-center">
        <p class="text-body2 text-medium-emphasis">No recipes found</p>
      </v-col>
    </v-row>
  </v-container>
</template>
