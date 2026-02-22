import { createRouter, createWebHistory, RouteRecordRaw } from "vue-router";

const routes: RouteRecordRaw[] = [
  {
    path: "/",
    name: "Dashboard",
    component: () => import("@/pages/DashboardPage.vue")
  },
  {
    path: "/recipes",
    name: "Recipes",
    component: () => import("@/pages/RecipesPage.vue")
  },
  {
    path: "/recipes/new",
    name: "RecipeCreate",
    component: () => import("@/pages/RecipeFormPage.vue")
  },
  {
    path: "/recipes/:id",
    name: "RecipeDetail",
    component: () => import("@/pages/RecipeDetailPage.vue")
  },
  {
    path: "/recipes/:id/edit",
    name: "RecipeEdit",
    component: () => import("@/pages/RecipeFormPage.vue")
  },
  {
    path: "/settings",
    name: "Settings",
    component: () => import("@/pages/SettingsPage.vue")
  }
];

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
});

export default router;
