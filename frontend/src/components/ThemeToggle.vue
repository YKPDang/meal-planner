<script setup lang="ts">
import { useTheme } from '@/composables/useTheme'

const { isDark, toggle } = useTheme()
</script>

<template>
  <v-btn :icon="isDark ? 'mdi-white-balance-sunny' : 'mdi-moon-waning-crescent'" @click="toggle" variant="text" />
</template>
