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

  async function createTag(name: string) {
    try {
      const newTag = await fetchJson("/tags", {
        method: "POST",
        body: JSON.stringify({ name })
      });
      status.value = "Tag created.";
      await loadTags();
      return newTag;
    } catch (error) {
      status.value =
        error instanceof Error ? error.message : "Failed to create tag";
      throw error;
    }
  }

  async function updateTag(tagId: string | number, name: string) {
    try {
      const updated = await fetchJson(`/tags/${tagId}`, {
        method: "PUT",
        body: JSON.stringify({ name })
      });
      status.value = "Tag updated.";
      await loadTags();
      return updated;
    } catch (error) {
      status.value =
        error instanceof Error ? error.message : "Failed to update tag";
      throw error;
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
    createTag,
    updateTag,
    deleteTag
  };
}
