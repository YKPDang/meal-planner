<script setup lang="ts">
import { computed, ref } from 'vue'
import { useRoute } from 'vue-router'
import { useDisplay } from 'vuetify'
import ThemeToggle from '@/components/ThemeToggle.vue'

const route = useRoute()
const display = useDisplay()
const drawer = ref(true)
const isLarge = computed(() => display.lgAndUp.value)

const navItems = [
  { title: 'Meal Plan', icon: 'mdi-calendar-week', to: '/' },
  { title: 'Recipes', icon: 'mdi-book-open', to: '/recipes' },
  { title: 'Add Recipe', icon: 'mdi-plus-circle', to: '/recipes/new' },
  { title: 'Settings', icon: 'mdi-cog', to: '/settings' }
]
</script>

<template>
  <v-app class="app-shell">
    <v-navigation-drawer v-model="drawer" :permanent="isLarge" :rail="isLarge" color="surface-bright">
      <v-list>
        <v-list-item v-for="item in navItems" :key="item.to" :to="item.to" :active="route.path === item.to"
          :prepend-icon="item.icon" :title="isLarge ? undefined : item.title" />
      </v-list>
    </v-navigation-drawer>

    <v-app-bar color="surface-bright" flat>
      <v-app-bar-nav-icon class="d-lg-none" @click="drawer = !drawer" />
      <v-app-bar-title>Meal Planner</v-app-bar-title>
      <v-spacer />
      <ThemeToggle />
    </v-app-bar>

    <v-main>
      <router-view />
    </v-main>
  </v-app>
</template>
