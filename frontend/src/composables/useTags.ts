import { ref } from "vue";
import { fetchJson } from "@/composables/useApi";
import type { Tag } from "@/types/api";

export function useTags() {
  const tags = ref<Tag[]>([]);
  const isLoading = ref(false);
  const status = ref("");

  async function loadTags() {
    isLoading.value = true;
    try {
      tags.value = await fetchJson("/tags");
    } catch (error) {
      status.value =
        error instanceof Error ? error.message : "Failed to load tags";
      throw error;
    } finally {
      isLoading.value = false;
    }
  }

  async function deleteTag(tagId: string | number) {
    try {
      await fetchJson(`/tags/${tagId}`, { method: "DELETE" });
      status.value = "Tag deleted.";
      await loadTags();
    } catch (error) {
      status.value =
        error instanceof Error ? error.message : "Failed to delete tag";
      throw error;
    }
  }

  return {
    tags,
    isLoading,
    status,
    loadTags,
    deleteTag
  };
}
