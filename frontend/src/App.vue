<script setup>
import { computed, onMounted, ref } from 'vue'
import { formatLocalDate, parseIngredientLine, parseTags } from './utils'

const API_BASE = import.meta.env.VITE_API_URL || '/api'
const recipes = ref([])
const tags = ref([])
const mealPlan = ref([])
const status = ref('')
const lookbackDays = ref(7)
const filterTagsInput = ref('')

const newRecipe = ref({
  name: '',
  description: '',
  ingredientsText: '',
  tagsText: ''
})

const weekStart = ref(getMonday(new Date()))

const weekLabel = computed(() => {
  const start = new Date(weekStart.value)
  const end = new Date(start)
  end.setDate(end.getDate() + 6)
  return `${start.toLocaleDateString()} - ${end.toLocaleDateString()}`
})

function getMonday(value) {
  const day = new Date(value)
  const d = day.getDay() || 7
  if (d !== 1) day.setHours(-24 * (d - 1))
  day.setHours(0, 0, 0, 0)
  return day
}

async function fetchJson(url, options = {}) {
  const response = await fetch(`${API_BASE}${url}`, {
    headers: { 'Content-Type': 'application/json' },
    ...options
  })
  if (!response.ok) {
    const err = await response.json().catch(() => ({ detail: 'Request failed' }))
    throw new Error(err.detail || 'Request failed')
  }
  if (response.status === 204) return null
  return response.json()
}

async function loadAll() {
  recipes.value = await fetchJson('/recipes')
  tags.value = await fetchJson('/tags')
  mealPlan.value = await fetchJson(`/meal-plan?start_date=${formatLocalDate(weekStart.value)}&days=7`)
}

async function saveRecipe() {
  const ingredients = newRecipe.value.ingredientsText
    .split('\n')
    .map(parseIngredientLine)
    .filter(Boolean)

  const payload = {
    name: newRecipe.value.name,
    description: newRecipe.value.description,
    ingredients,
    tags: parseTags(newRecipe.value.tagsText)
  }

  await fetchJson('/recipes', { method: 'POST', body: JSON.stringify(payload) })
  newRecipe.value = { name: '', description: '', ingredientsText: '', tagsText: '' }
  status.value = 'Recipe added.'
  await loadAll()
}

async function assignRecipe(day, recipeId) {
  await fetchJson(`/meal-plan/${day}`, {
    method: 'PUT',
    body: JSON.stringify({ recipe_id: recipeId ? Number(recipeId) : null })
  })
  await loadAll()
}

async function randomize(day, mode) {
  const tagsList = parseTags(filterTagsInput.value)
  await fetchJson(`/meal-plan/${day}/random`, {
    method: 'POST',
    body: JSON.stringify({ mode, tags: tagsList, lookback_days: lookbackDays.value })
  })
  await loadAll()
}

function navigateWeek(delta) {
  const next = new Date(weekStart.value)
  next.setDate(next.getDate() + delta * 7)
  weekStart.value = next
  loadAll()
}

onMounted(async () => {
  try {
    await loadAll()
  } catch (error) {
    status.value = error.message
  }
})
</script>

<template>
  <main>
    <h1>Meal Planner</h1>
    <p class="status">{{ status }}</p>

    <section class="card">
      <h2>Add Recipe</h2>
      <form @submit.prevent="saveRecipe" class="grid">
        <input v-model="newRecipe.name" placeholder="Recipe name" required />
        <textarea v-model="newRecipe.description" placeholder="Description"></textarea>
        <textarea
          v-model="newRecipe.ingredientsText"
          placeholder="Ingredients (one per line, example: 200g pasta)"
        ></textarea>
        <input v-model="newRecipe.tagsText" placeholder="Tags (comma separated)" />
        <button type="submit">Save Recipe</button>
      </form>
    </section>

    <section class="card">
      <div class="week-header">
        <button @click="navigateWeek(-1)">Previous</button>
        <h2>Week: {{ weekLabel }}</h2>
        <button @click="navigateWeek(1)">Next</button>
      </div>

      <div class="toolbar">
        <label>
          Smart lookback days
          <input type="number" min="1" v-model.number="lookbackDays" />
        </label>
        <label>
          Filter tags
          <input v-model="filterTagsInput" placeholder="pasta,quick-lunch" />
        </label>
      </div>

      <div class="calendar">
        <article v-for="entry in mealPlan" :key="entry.day" class="day">
          <h3>{{ entry.day }}</h3>
          <p><strong>Planned:</strong> {{ entry.recipe?.name || '—' }}</p>

          <select @change="assignRecipe(entry.day, $event.target.value)">
            <option value="">Select recipe</option>
            <option
              v-for="recipe in recipes"
              :key="recipe.id"
              :value="recipe.id"
              :selected="entry.recipe?.id === recipe.id"
            >
              {{ recipe.name }}
            </option>
          </select>

          <div class="actions">
            <button @click="randomize(entry.day, 'random')">Random</button>
            <button @click="randomize(entry.day, 'smart')">Smart Random</button>
            <button @click="randomize(entry.day, 'filtered')">Filtered Random</button>
          </div>
        </article>
      </div>
    </section>

    <section class="card">
      <h2>Recipes</h2>
      <ul>
        <li v-for="recipe in recipes" :key="recipe.id">
          <strong>{{ recipe.name }}</strong> — {{ recipe.description }}
          <br />
          Tags: {{ recipe.tags.join(', ') || 'none' }}
        </li>
      </ul>

      <h3>Available Tags</h3>
      <p>{{ tags.map((tag) => tag.name).join(', ') || 'none' }}</p>
    </section>
  </main>
</template>
