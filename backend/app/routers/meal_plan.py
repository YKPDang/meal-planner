from datetime import date

from fastapi import APIRouter, Depends, Query

from backend.app import config
from backend.app.db import get_db
from backend.app.repositories import meal_plan as meal_plan_repo
from backend.app.repositories import recipes as recipe_repo
from backend.app.schemas import MealPlanAssign, RandomizeRequest
from backend.app.services import meal_plan as meal_plan_service


router = APIRouter()


@router.get("/meal-plan")
def get_meal_plan(
    start_date: date = Query(default_factory=date.today),
    days: int = 7,
    conn=Depends(get_db),
) -> list[dict]:
    result = []
    for entry in meal_plan_repo.get_meal_plan(conn, start_date, days):
        recipe = recipe_repo.recipe_details(conn, entry["recipe_id"]) if entry["recipe_id"] else None
        result.append({"day": entry["day"], "recipe": recipe})
    return result


@router.put("/meal-plan/{day}")
def assign_recipe(day: date, payload: MealPlanAssign, conn=Depends(get_db)) -> dict:
    if payload.recipe_id is not None:
        recipe_repo.recipe_details(conn, payload.recipe_id)
    meal_plan_repo.upsert_meal_plan(conn, day, payload.recipe_id)
    recipe = recipe_repo.recipe_details(conn, payload.recipe_id) if payload.recipe_id else None
    return {"day": day.isoformat(), "recipe": recipe}


@router.post("/meal-plan/{day}/random")
def randomize_recipe(day: date, payload: RandomizeRequest, conn=Depends(get_db)) -> dict:
    # Get current recipe for this day (if any) to avoid selecting it
    current_entry = conn.execute(
        "SELECT recipe_id FROM meal_plan WHERE day = ?", (day.isoformat(),)
    ).fetchone()
    current_recipe_id = current_entry["recipe_id"] if current_entry else None

    lookback = payload.lookback_days if payload.lookback_days is not None else config.SMART_RANDOM_LOOKBACK_DAYS
    recipe_id = meal_plan_service.select_random_recipe(
        conn, day, payload.mode, payload.tags, lookback, current_recipe_id
    )
    meal_plan_repo.upsert_meal_plan(conn, day, recipe_id)
    return {"day": day.isoformat(), "recipe": recipe_repo.recipe_details(conn, recipe_id), "mode": payload.mode}
