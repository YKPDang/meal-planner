import { ref } from "vue";
import { fetchJson } from "@/composables/useApi";
import { parseIngredientLine, parseTags } from "@/utils/parse";
import type { Recipe, RecipeDraft } from "@/types/api";

export function useRecipes() {
  const recipes = ref<Recipe[]>([]);
  const isLoading = ref(false);
  const status = ref("");

  async function loadRecipes() {
    isLoading.value = true;
    try {
      recipes.value = await fetchJson("/recipes");
    } catch (error) {
      status.value =
        error instanceof Error ? error.message : "Failed to load recipes";
      throw error;
    } finally {
      isLoading.value = false;
    }
  }

  async function getRecipe(id: string | number) {
    try {
      return await fetchJson(`/recipes/${id}`);
    } catch (error) {
      status.value =
        error instanceof Error ? error.message : "Failed to load recipe";
      throw error;
    }
  }

  async function saveRecipe(draft: RecipeDraft) {
    const ingredients = draft.ingredientsText
      .split("\n")
      .map(parseIngredientLine)
      .filter(Boolean);

    const payload = {
      name: draft.name,
      description: draft.description,
      ingredients,
      tags: parseTags(draft.tagsText)
    };

    try {
      await fetchJson("/recipes", {
        method: "POST",
        body: JSON.stringify(payload)
      });
      status.value = "Recipe saved.";
      await loadRecipes();
    } catch (error) {
      status.value =
        error instanceof Error ? error.message : "Failed to save recipe";
      throw error;
    }
  }

  async function updateRecipe(id: string | number, draft: RecipeDraft) {
    const ingredients = draft.ingredientsText
      .split("\n")
      .map(parseIngredientLine)
      .filter(Boolean);

    const payload = {
      name: draft.name,
      description: draft.description,
      ingredients,
      tags: parseTags(draft.tagsText)
    };

    try {
      await fetchJson(`/recipes/${id}`, {
        method: "PUT",
        body: JSON.stringify(payload)
      });
      status.value = "Recipe updated.";
      await loadRecipes();
    } catch (error) {
      status.value =
        error instanceof Error ? error.message : "Failed to update recipe";
      throw error;
    }
  }

  return {
    recipes,
    isLoading,
    status,
    loadRecipes,
    getRecipe,
    saveRecipe,
    updateRecipe
  };
}
