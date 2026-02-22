from fastapi import APIRouter, Depends

from backend.app.db import get_db
from backend.app.repositories import recipes as recipe_repo
from backend.app.schemas import RecipeIn


router = APIRouter()


@router.get("/recipes")
def list_recipes(conn=Depends(get_db)) -> list[dict]:
    return [recipe_repo.recipe_details(conn, recipe_id) for recipe_id in recipe_repo.list_recipe_ids(conn)]


@router.get("/recipes/{recipe_id}")
def get_recipe(recipe_id: int, conn=Depends(get_db)) -> dict:
    return recipe_repo.recipe_details(conn, recipe_id)


@router.post("/recipes", status_code=201)
def create_recipe(payload: RecipeIn, conn=Depends(get_db)) -> dict:
    return recipe_repo.create_recipe(conn, payload)


@router.put("/recipes/{recipe_id}")
def update_recipe(recipe_id: int, payload: RecipeIn, conn=Depends(get_db)) -> dict:
    return recipe_repo.update_recipe(conn, recipe_id, payload)


@router.delete("/recipes/{recipe_id}", status_code=204)
def delete_recipe(recipe_id: int, conn=Depends(get_db)) -> None:
    recipe_repo.delete_recipe(conn, recipe_id)
