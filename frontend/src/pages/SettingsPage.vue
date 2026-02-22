<script setup lang="ts">
import { onMounted } from 'vue'
import ThemeToggle from '@/components/ThemeToggle.vue'
import { useTheme } from '@/composables/useTheme'
import { useTags } from '@/composables/useTags'

const { isDark } = useTheme()
const { tags, loadTags, deleteTag } = useTags()

onMounted(async () => {
  await loadTags()
})
</script>

<template>
  <v-container class="py-10">
    <v-row justify="center">
      <v-col cols="12" md="8">
        <h1 class="text-h4 font-weight-bold mb-6">Settings</h1>

        <v-card class="mb-6">
          <v-card-item>
            <div class="text-subtitle1 font-weight-bold">Theme</div>
          </v-card-item>
          <v-card-text>
            <div class="d-flex align-center justify-space-between">
              <span class="text-body2">Dark Mode</span>
              <ThemeToggle />
            </div>
          </v-card-text>
        </v-card>

        <v-card>
          <v-card-item>
            <div class="text-subtitle1 font-weight-bold">Tags</div>
          </v-card-item>
          <v-card-text>
            <p class="text-body2 text-medium-emphasis mb-4">
              Manage recipe tags
            </p>
            <v-table v-if="tags.length > 0">
              <thead>
                <tr>
                  <th class="text-left">Tag</th>
                  <th class="text-right">Actions</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="tag in tags" :key="tag.id">
                  <td>{{ tag.name }}</td>
                  <td class="text-right">
                    <v-btn icon="mdi-delete" size="small" variant="text" @click="deleteTag(tag.id)" />
                  </td>
                </tr>
              </tbody>
            </v-table>
            <p v-else class="text-body2 text-medium-emphasis">No tags created yet</p>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>
