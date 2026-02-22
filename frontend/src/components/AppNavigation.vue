<script setup lang="ts">
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import { useDisplay } from 'vuetify'

const props = defineProps<{
  modelValue: boolean
}>()

const emit = defineEmits<{
  'update:modelValue': [value: boolean]
}>()

const route = useRoute()
const display = useDisplay()

const navItems = [
  { title: 'Meal Plan', icon: 'mdi-calendar-week', to: '/' },
  { title: 'Recipes', icon: 'mdi-book-open', to: '/recipes' },
  { title: 'Add Recipe', icon: 'mdi-plus-circle', to: '/recipes/new' },
  { title: 'Settings', icon: 'mdi-cog', to: '/settings' }
]

const isLarge = computed(() => display.lgAndUp.value)

const drawerModel = computed({
  get: () => props.modelValue,
  set: (val) => emit('update:modelValue', val)
})
</script>

<template>
  <v-navigation-drawer v-model="drawerModel" :permanent="isLarge" :rail="isLarge" color="surface-bright" width="256">
    <v-list>
      <v-list-item v-for="item in navItems" :key="item.to" :to="item.to" :active="route.path === item.to"
        :prepend-icon="item.icon" :title="isLarge ? undefined : item.title" />
    </v-list>
  </v-navigation-drawer>
</template>
