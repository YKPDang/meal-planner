from typing import Literal

from pydantic import BaseModel, Field


class IngredientIn(BaseModel):
    unit: str = Field(default="")
    item: str


class RecipeIn(BaseModel):
    name: str
    description: str = ""
    ingredients: list[IngredientIn] = Field(default_factory=list)
    tags: list[str] = Field(default_factory=list)


class MealPlanAssign(BaseModel):
    recipe_id: int | None = None


class RandomizeRequest(BaseModel):
    mode: Literal["random", "smart", "filtered"] = "random"
    tags: list[str] = Field(default_factory=list)
    lookback_days: int | None = None
