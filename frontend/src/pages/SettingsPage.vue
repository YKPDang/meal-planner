<script setup lang="ts">
import { onMounted, ref } from 'vue'
import ThemeToggle from '@/components/ThemeToggle.vue'
import { useTheme } from '@/composables/useTheme'
import { useTags } from '@/composables/useTags'

const { isDark } = useTheme()
const { tags, loadTags, createTag, updateTag, deleteTag, status } = useTags()

const newTagName = ref('')
const editingId = ref<number | null>(null)
const editingName = ref('')
const isSaving = ref(false)

const handleAddTag = async () => {
  if (!newTagName.value.trim()) return
  isSaving.value = true
  try {
    await createTag(newTagName.value)
    newTagName.value = ''
  } finally {
    isSaving.value = false
  }
}

const handleEditStart = (tag: any) => {
  editingId.value = tag.id
  editingName.value = tag.name
}

const handleEditSave = async () => {
  if (!editingName.value.trim()) return
  isSaving.value = true
  try {
    await updateTag(editingId.value, editingName.value)
    editingId.value = null
    editingName.value = ''
  } finally {
    isSaving.value = false
  }
}

const handleEditCancel = () => {
  editingId.value = null
  editingName.value = ''
}

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
            <p class="text-body2 text-medium-emphasis mb-6">
              Manage recipe tags
            </p>

            <!-- Add new tag form -->
            <div class="mb-6">
              <div class="text-subtitle2 font-weight-bold mb-2">Add New Tag</div>
              <div class="d-flex gap-2">
                <v-text-field
                  v-model="newTagName"
                  placeholder="Enter tag name"
                  density="compact"
                  class="flex-grow-1"
                />
                <v-btn
                  @click="handleAddTag"
                  color="primary"
                  :loading="isSaving"
                  :disabled="!newTagName.trim()"
                >
                  Add
                </v-btn>
              </div>
            </div>

            <!-- Tags list -->
            <div v-if="tags.length > 0">
              <div class="text-subtitle2 font-weight-bold mb-2">Existing Tags</div>
              <v-table>
                <thead>
                  <tr>
                    <th class="text-left">Tag</th>
                    <th class="text-right">Actions</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="tag in tags" :key="tag.id">
                    <td v-if="editingId === tag.id">
                      <v-text-field
                        v-model="editingName"
                        density="compact"
                        autofocus
                        @keyup.enter="handleEditSave"
                        @keyup.escape="handleEditCancel"
                      />
                    </td>
                    <td v-else>{{ tag.name }}</td>
                    <td class="text-right">
                      <v-btn
                        v-if="editingId === tag.id"
                        icon="mdi-check"
                        size="small"
                        variant="text"
                        color="success"
                        @click="handleEditSave"
                        :loading="isSaving"
                      />
                      <v-btn
                        v-else
                        icon="mdi-pencil"
                        size="small"
                        variant="text"
                        @click="handleEditStart(tag)"
                      />
                      <v-btn
                        v-if="editingId === tag.id"
                        icon="mdi-close"
                        size="small"
                        variant="text"
                        color="error"
                        @click="handleEditCancel"
                      />
                      <v-btn
                        v-else
                        icon="mdi-delete"
                        size="small"
                        variant="text"
                        @click="deleteTag(tag.id)"
                      />
                    </td>
                  </tr>
                </tbody>
              </v-table>
            </div>
            <p v-else class="text-body2 text-medium-emphasis">No tags created yet</p>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>
