<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import MealPlanBoard from '@/components/MealPlanBoard.vue'
import { useMealPlan } from '@/composables/useMealPlan'
import { useRecipes } from '@/composables/useRecipes'
import { useTags } from '@/composables/useTags'

const mealPlanComposable = useMealPlan()
const recipesComposable = useRecipes()
const tagsComposable = useTags()

const {
  mealPlan,
  status,
  isLoading,
  lookbackDays,
  weekLabel,
  assignRecipe,
  randomize,
  navigateWeek,
  loadMealPlan,
  clearWeek
} = mealPlanComposable

const { recipes } = recipesComposable
const { tags } = tagsComposable

const filterTags = ref<string[]>([])
const excludeTags = ref<string[]>([])
const showFilters = ref(false)
const hasStatus = computed(() => Boolean(status.value))

// Sync tag arrays to the composable's comma-separated strings
const syncTags = () => {
  mealPlanComposable.filterTagsInput.value = filterTags.value.join(', ')
  mealPlanComposable.excludeTagsInput.value = excludeTags.value.join(', ')
}

// Stats
const totalRecipes = computed(() => recipes.value.length)
const plannedMeals = computed(() => mealPlan.value.filter(e => e.recipe).length)
const unplannedDays = computed(() => mealPlan.value.filter(e => !e.recipe).length)

const handleRandomize = (day: string, mode: 'random' | 'smart' | 'filtered') => {
  syncTags()
  randomize(day, mode)
}

const heroLines = [
  { title: "Ugh, I have to think about dinner again?", subtitle: "I don't wanna..." },
  { title: "What do we even eat anymore...", subtitle: "Seriously, I forgot." },
  { title: "I don't wanna cook but here we are", subtitle: "At least the app remembers recipes for me." },
  { title: "Not the 'what's for dinner' question again", subtitle: "Every. Single. Day." },
  { title: "Brain empty, fridge full, no ideas", subtitle: "Classic combo." },
  { title: "Can someone else decide what to eat?", subtitle: "That someone is the random button." },
  { title: "Staring at the fridge won't help, trust me", subtitle: "I've tried. Many times." },
  { title: "Why is meal planning a daily thing??", subtitle: "Nobody warned me about this part of adulting." },
  { title: "If only food just appeared on the table", subtitle: "But noooo, I have to plan it." },
  { title: "I swear we just ate yesterday", subtitle: "And now we have to do it again?!" },
  { title: "My kingdom for someone to just tell me what to cook", subtitle: "Okay fine, I'll click the button myself." },
  { title: "The eternal struggle: what's for dinner", subtitle: "Humanity's oldest unsolved problem." },
  { title: "Thinking about food is exhausting", subtitle: "Eating it is the easy part." },
  { title: "Please not another 'I dunno, what do you want?'", subtitle: "Let's just let the algorithm decide." },
  { title: "Do we really need to eat every single day?", subtitle: "Asking for a friend." },
  { title: "Same groceries, zero inspiration", subtitle: "Maybe the random button will save us." },
  { title: "Adulting is just deciding meals forever", subtitle: "Nobody mentioned this in the brochure." },
  { title: "I'd rather do laundry than figure out dinner", subtitle: "And I really hate laundry." },
  { title: "Food decision fatigue is real and I have it", subtitle: "Symptoms include opening and closing the fridge repeatedly." },
  { title: "Let the random button decide, I'm too tired", subtitle: "Technology was made for this moment." },
]

const heroLine = heroLines[Math.floor(Math.random() * heroLines.length)]

onMounted(async () => {
  await Promise.all([
    loadMealPlan(),
    recipesComposable.loadRecipes(),
    tagsComposable.loadTags()
  ])
})
</script>

<template>
  <v-container class="py-6 py-md-10" fluid>
    <v-row justify="center">
      <v-col cols="12" lg="10" xl="9">
        <!-- Hero Header -->
        <div class="hero-section mb-8 pa-6 pa-md-8 rounded-xl">
          <div class="d-flex flex-column flex-md-row align-md-center justify-space-between ga-4">
            <div>
              <h1 class="text-h4 text-md-h3 font-weight-bold hero-text mb-2">
                {{ heroLine.title }}
              </h1>
              <p class="text-body-1 hero-text-muted mb-0">
                {{ heroLine.subtitle }}
              </p>
            </div>
            <v-btn to="/recipes/new" color="surface" variant="flat" prepend-icon="mdi-plus" size="large" rounded="lg"
              class="font-weight-bold">
              Add Recipe
            </v-btn>
          </div>
        </div>

        <!-- Stats Cards -->
        <v-row class="mb-6" dense>
          <v-col cols="12" sm="4">
            <v-card rounded="lg" elevation="0" class="stat-card">
              <v-card-text class="d-flex align-center ga-4 pa-4">
                <v-avatar color="primary" variant="tonal" size="48" rounded="lg">
                  <v-icon>mdi-book-open-variant</v-icon>
                </v-avatar>
                <div>
                  <div class="text-h5 font-weight-bold">{{ totalRecipes }}</div>
                  <div class="text-body-2 text-medium-emphasis">Total Recipes</div>
                </div>
              </v-card-text>
            </v-card>
          </v-col>
          <v-col cols="12" sm="4">
            <v-card rounded="lg" elevation="0" class="stat-card">
              <v-card-text class="d-flex align-center ga-4 pa-4">
                <v-avatar color="success" variant="tonal" size="48" rounded="lg">
                  <v-icon>mdi-check-circle-outline</v-icon>
                </v-avatar>
                <div>
                  <div class="text-h5 font-weight-bold">{{ plannedMeals }}</div>
                  <div class="text-body-2 text-medium-emphasis">Planned Meals</div>
                </div>
              </v-card-text>
            </v-card>
          </v-col>
          <v-col cols="12" sm="4">
            <v-card rounded="lg" elevation="0" class="stat-card">
              <v-card-text class="d-flex align-center ga-4 pa-4">
                <v-avatar color="warning" variant="tonal" size="48" rounded="lg">
                  <v-icon>mdi-calendar-question</v-icon>
                </v-avatar>
                <div>
                  <div class="text-h5 font-weight-bold">{{ unplannedDays }}</div>
                  <div class="text-body-2 text-medium-emphasis">Unplanned Days</div>
                </div>
              </v-card-text>
            </v-card>
          </v-col>
        </v-row>

        <v-alert v-if="hasStatus" type="info" variant="tonal" class="mb-6" rounded="lg">
          {{ status }}
        </v-alert>

        <!-- Filter Controls (expandable) -->
        <v-card class="mb-6" rounded="lg" elevation="0" border>
          <v-card-text class="pa-0">
            <v-btn variant="text" block class="justify-start text-none pa-4"
              :append-icon="showFilters ? 'mdi-chevron-up' : 'mdi-chevron-down'" @click="showFilters = !showFilters">
              <template #prepend>
                <v-icon color="primary">mdi-tune-variant</v-icon>
              </template>
              <span class="text-body-1 font-weight-medium">Randomization Settings</span>
              <v-chip v-if="filterTags.length || excludeTags.length" size="x-small" color="primary" class="ml-2">
                {{ filterTags.length + excludeTags.length }} active
              </v-chip>
            </v-btn>

            <v-expand-transition>
              <div v-show="showFilters">
                <v-divider />
                <div class="pa-4">
                  <v-row dense>
                    <v-col cols="12" md="4">
                      <v-text-field v-model.number="lookbackDays" type="number" min="1" label="Smart lookback days"
                        variant="outlined" density="comfortable" hide-details prepend-inner-icon="mdi-history" />
                    </v-col>
                    <v-col cols="12" md="4">
                      <v-select v-model="filterTags" :items="tags" item-title="name" item-value="name"
                        label="Include tags" multiple chips closable-chips clearable variant="outlined"
                        density="comfortable" hide-details prepend-inner-icon="mdi-tag-check-outline" />
                    </v-col>
                    <v-col cols="12" md="4">
                      <v-select v-model="excludeTags" :items="tags" item-title="name" item-value="name"
                        label="Exclude tags" multiple chips closable-chips clearable variant="outlined"
                        density="comfortable" hide-details prepend-inner-icon="mdi-tag-off-outline" />
                    </v-col>
                  </v-row>
                </div>
              </div>
            </v-expand-transition>
          </v-card-text>
        </v-card>

        <!-- Meal Plan Board -->
        <MealPlanBoard :meal-plan="mealPlan" :recipes="recipes" :week-label="weekLabel" :loading="isLoading"
          @assign="assignRecipe" @randomize="handleRandomize" @navigate="navigateWeek" @clear="clearWeek" />
      </v-col>
    </v-row>
  </v-container>
</template>

<style scoped>
.hero-section {
  background: linear-gradient(135deg, rgb(var(--v-theme-primary)) 0%, rgb(var(--v-theme-primary-darken-1, var(--v-theme-primary))) 50%, #1a237e 100%);
  position: relative;
  overflow: hidden;
}

.hero-section::before {
  content: '';
  position: absolute;
  top: -50%;
  right: -20%;
  width: 400px;
  height: 400px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.05);
}

.hero-section::after {
  content: '';
  position: absolute;
  bottom: -30%;
  left: 10%;
  width: 250px;
  height: 250px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.03);
}

.stat-card {
  border: 1px solid rgba(var(--v-border-color), var(--v-border-opacity));
  transition: transform 0.15s ease;
}

.stat-card:hover {
  transform: translateY(-2px);
}

.hero-text {
  color: rgba(255, 255, 255, 0.95);
}

.hero-text-muted {
  color: rgba(255, 255, 255, 0.7);
}
</style>
