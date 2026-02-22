export interface Ingredient {
  id?: number
  unit: string
  item: string
}

export interface Recipe {
  id: number
  name: string
  description: string
  ingredients: Ingredient[]
  tags: string[]
}

export interface Tag {
  id: number
  name: string
}

export interface MealPlanEntry {
  day: string
  recipe: Recipe | null
}

export interface RecipeDraft {
  name: string
  description: string
  ingredientsText: string
  tagsText: string
}
