import { computed, ref } from 'vue'

import { fetchJson } from '@/composables/useApi'
import { formatLocalDate, getMonday } from '@/utils/date'
import { parseTags } from '@/utils/parse'
import type { MealPlanEntry, RecipeDraft } from '@/types/api'

export function useMealPlan() {
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

  async function loadMealPlan() {
    isLoading.value = true
    status.value = ''
    try {
      mealPlan.value = await fetchJson(
        `/meal-plan?start_date=${formatLocalDate(weekStart.value)}&days=7`
      )
    } catch (error) {
      status.value = error instanceof Error ? error.message : 'Failed to load meal plan'
      throw error
    } finally {
      isLoading.value = false
    }
  }

  async function assignRecipe(day: string, recipeId: string) {
    try {
      await fetchJson(`/meal-plan/${day}`, {
        method: 'PUT',
        body: JSON.stringify({ recipe_id: recipeId ? Number(recipeId) : null })
      })
      await loadMealPlan()
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
      await loadMealPlan()
    } catch (error) {
      status.value = error instanceof Error ? error.message : 'Failed to randomize recipe'
    }
  }

  function navigateWeek(delta: number) {
    const next = new Date(weekStart.value)
    next.setDate(next.getDate() + delta * 7)
    weekStart.value = next
    loadMealPlan()
  }

  return {
    mealPlan,
    status,
    isLoading,
    lookbackDays,
    filterTagsInput,
    newRecipe,
    weekStart,
    weekLabel,
    loadMealPlan,
    assignRecipe,
    randomize,
    navigateWeek
  }
}
