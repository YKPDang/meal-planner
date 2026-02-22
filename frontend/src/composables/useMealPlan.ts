import { computed, onMounted, ref } from 'vue'

import { fetchJson } from '@/composables/useApi'
import { formatLocalDate, getMonday } from '@/utils/date'
import { parseIngredientLine, parseTags } from '@/utils/parse'
import type { MealPlanEntry, Recipe, RecipeDraft, Tag } from '@/types/api'

export function useMealPlan() {
  const recipes = ref<Recipe[]>([])
  const tags = ref<Tag[]>([])
  const mealPlan = ref<MealPlanEntry[]>([])
  const status = ref('')
  const isLoading = ref(false)
  const lookbackDays = ref(7)
  const filterTagsInput = ref('')
  const newRecipe = ref<RecipeDraft>({
    name: '',
    description: '',
    ingredientsText: '',
    tagsText: ''
  })

  const weekStart = ref(getMonday(new Date()))

  const weekLabel = computed(() => {
    const start = new Date(weekStart.value)
    const end = new Date(start)
    end.setDate(end.getDate() + 6)
    return `${start.toLocaleDateString()} - ${end.toLocaleDateString()}`
  })

  async function loadAll() {
    isLoading.value = true
    status.value = ''
    try {
      recipes.value = await fetchJson('/recipes')
      tags.value = await fetchJson('/tags')
      mealPlan.value = await fetchJson(
        `/meal-plan?start_date=${formatLocalDate(weekStart.value)}&days=7`
      )
    } catch (error) {
      status.value = error instanceof Error ? error.message : 'Failed to load data'
      throw error
    } finally {
      isLoading.value = false
    }
  }

  async function saveRecipe() {
    const ingredients = newRecipe.value.ingredientsText
      .split('\n')
      .map(parseIngredientLine)
      .filter(Boolean)

    const payload = {
      name: newRecipe.value.name,
      description: newRecipe.value.description,
      ingredients,
      tags: parseTags(newRecipe.value.tagsText)
    }

    try {
      await fetchJson('/recipes', { method: 'POST', body: JSON.stringify(payload) })
      newRecipe.value = { name: '', description: '', ingredientsText: '', tagsText: '' }
      status.value = 'Recipe added.'
      await loadAll()
    } catch (error) {
      status.value = error instanceof Error ? error.message : 'Failed to save recipe'
    }
  }

  async function assignRecipe(day: string, recipeId: string) {
    try {
      await fetchJson(`/meal-plan/${day}`, {
        method: 'PUT',
        body: JSON.stringify({ recipe_id: recipeId ? Number(recipeId) : null })
      })
      await loadAll()
    } catch (error) {
      status.value = error instanceof Error ? error.message : 'Failed to assign recipe'
    }
  }

  async function randomize(day: string, mode: 'random' | 'smart' | 'filtered') {
    const tagsList = parseTags(filterTagsInput.value)
    try {
      await fetchJson(`/meal-plan/${day}/random`, {
        method: 'POST',
        body: JSON.stringify({ mode, tags: tagsList, lookback_days: lookbackDays.value })
      })
      await loadAll()
    } catch (error) {
      status.value = error instanceof Error ? error.message : 'Failed to randomize recipe'
    }
  }

  function navigateWeek(delta: number) {
    const next = new Date(weekStart.value)
    next.setDate(next.getDate() + delta * 7)
    weekStart.value = next
    loadAll()
  }

  onMounted(async () => {
    await loadAll()
  })

  return {
    recipes,
    tags,
    mealPlan,
    status,
    isLoading,
    lookbackDays,
    filterTagsInput,
    newRecipe,
    weekStart,
    weekLabel,
    loadAll,
    saveRecipe,
    assignRecipe,
    randomize,
    navigateWeek
  }
}
