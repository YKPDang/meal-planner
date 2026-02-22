<script setup lang="ts">
import { computed } from 'vue'
import type { Recipe } from '@/types/api'

defineProps<{
  recipe: Recipe
}>()

const emit = defineEmits<{
  click: []
}>()
</script>

<template>
  <v-card @click="emit('click')" class="cursor-pointer h-100">
    <v-card-item>
      <div class="text-h6 font-weight-bold">{{ recipe.name }}</div>
    </v-card-item>

    <v-card-text>
      <p class="text-body2 text-medium-emphasis line-clamp-3">
        {{ recipe.description || 'No description' }}
      </p>
    </v-card-text>

    <v-card-text class="py-1">
      <div class="chip-wrap">
        <v-chip v-for="tag in recipe.tags" :key="tag.id" size="small" variant="tonal">
          {{ tag.name }}
        </v-chip>
      </div>
    </v-card-text>
  </v-card>
</template>

<style scoped>
.cursor-pointer {
  cursor: pointer;
}

.line-clamp-3 {
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>
