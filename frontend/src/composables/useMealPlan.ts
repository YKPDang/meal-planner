import { computed, ref } from "vue";

import { fetchJson } from "@/composables/useApi";
import { formatLocalDate, getMonday } from "@/utils/date";
import { parseTags } from "@/utils/parse";
import type { MealPlanEntry, RecipeDraft } from "@/types/api";

export function useMealPlan() {
  const mealPlan = ref<MealPlanEntry[]>([]);
  const status = ref("");
  const isLoading = ref(false);
  const lookbackDays = ref(7);
  const filterTagsInput = ref("");
  const excludeTagsInput = ref("");
  const newRecipe = ref<RecipeDraft>({
    name: "",
    description: "",
    ingredientsText: "",
    tagsText: ""
  });

  const weekStart = ref(getMonday(new Date()));

  const weekLabel = computed(() => {
    const start = new Date(weekStart.value);
    const end = new Date(start);
    end.setDate(end.getDate() + 6);
    return `${start.toLocaleDateString()} - ${end.toLocaleDateString()}`;
  });

  async function loadMealPlan() {
    isLoading.value = true;
    status.value = "";
    try {
      mealPlan.value = await fetchJson(
        `/meal-plan?start_date=${formatLocalDate(weekStart.value)}&days=7`
      );
    } catch (error) {
      status.value =
        error instanceof Error ? error.message : "Failed to load meal plan";
      throw error;
    } finally {
      isLoading.value = false;
    }
  }

  async function assignRecipe(day: string, recipeId: string) {
    try {
      await fetchJson(`/meal-plan/${day}`, {
        method: "PUT",
        body: JSON.stringify({ recipe_id: recipeId ? Number(recipeId) : null })
      });
      await loadMealPlan();
    } catch (error) {
      status.value =
        error instanceof Error ? error.message : "Failed to assign recipe";
    }
  }

  async function randomize(day: string, mode: "random" | "smart" | "filtered") {
    const tagsList = parseTags(filterTagsInput.value);
    const excludeTagsList = parseTags(excludeTagsInput.value);
    try {
      await fetchJson(`/meal-plan/${day}/random`, {
        method: "POST",
        body: JSON.stringify({
          mode,
          tags: tagsList,
          exclude_tags: excludeTagsList,
          lookback_days: lookbackDays.value
        })
      });
      await loadMealPlan();
    } catch (error) {
      status.value =
        error instanceof Error ? error.message : "Failed to randomize recipe";
    }
  }

  async function clearWeek() {
    try {
      for (const entry of mealPlan.value) {
        if (entry.recipe) {
          await fetchJson(`/meal-plan/${entry.day}`, {
            method: "PUT",
            body: JSON.stringify({ recipe_id: null })
          });
        }
      }
      await loadMealPlan();
    } catch (error) {
      status.value =
        error instanceof Error ? error.message : "Failed to clear meal plan";
    }
  }

  function navigateWeek(delta: number) {
    const next = new Date(weekStart.value);
    next.setDate(next.getDate() + delta * 7);
    weekStart.value = next;
    loadMealPlan();
  }

  return {
    mealPlan,
    status,
    isLoading,
    lookbackDays,
    filterTagsInput,
    excludeTagsInput,
    newRecipe,
    weekStart,
    weekLabel,
    loadMealPlan,
    assignRecipe,
    randomize,
    navigateWeek,
    clearWeek
  };
}
