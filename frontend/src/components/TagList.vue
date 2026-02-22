<script setup lang="ts">
import type { PropType } from 'vue'

import type { Tag } from '@/types/api'

defineProps({
  tags: {
    type: Array as PropType<Tag[]>,
    required: true
  }
})
</script>

<template>
  <v-card elevation="1" class="h-100">
    <v-card-title class="text-h6">Available Tags</v-card-title>
    <v-divider />
    <v-card-text>
      <div class="chip-wrap">
        <v-chip v-for="tag in tags" :key="tag.id" color="secondary" variant="tonal">
          {{ tag.name }}
        </v-chip>
        <v-chip v-if="tags.length === 0" variant="outlined">No tags yet</v-chip>
      </div>
    </v-card-text>
  </v-card>
</template>
