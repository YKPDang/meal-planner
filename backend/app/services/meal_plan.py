import sqlite3
from datetime import date, timedelta

from fastapi import HTTPException


def select_random_recipe(
    conn: sqlite3.Connection,
    target_day: date,
    mode: str,
    tags: list[str],
    lookback_days: int,
    current_recipe_id: int | None = None,
) -> int:
    params: list[object] = []
    clauses: list[str] = []

    # Never select the currently selected recipe
    if current_recipe_id:
        clauses.append("r.id != ?")
        params.append(current_recipe_id)

    if mode == "smart":
        start_day = target_day - timedelta(days=lookback_days)
        clauses.append(
            """
            r.id NOT IN (
                SELECT recipe_id
                FROM meal_plan
                WHERE recipe_id IS NOT NULL
                  AND day >= ?
                  AND day < ?
            )
            """
        )
        params.extend([start_day.isoformat(), target_day.isoformat()])
    elif mode == "random":
        # For pure random, also skip recipes from the last 3 days for this meal plan entry
        start_day = target_day - timedelta(days=3)
        clauses.append(
            """
            r.id NOT IN (
                SELECT recipe_id
                FROM meal_plan
                WHERE recipe_id IS NOT NULL
                  AND day >= ?
                  AND day < ?
            )
            """
        )
        params.extend([start_day.isoformat(), target_day.isoformat()])

    if mode == "filtered":
        cleaned = sorted({tag.strip() for tag in tags if tag.strip()})
        if not cleaned:
            raise HTTPException(status_code=400, detail="Filtered mode requires one or more tags")
        placeholders = ",".join(["?" for _ in cleaned])
        clauses.append(
            "r.id IN (SELECT rt.recipe_id FROM recipe_tags rt JOIN tags t ON rt.tag_id = t.id "
            f"WHERE t.name IN ({placeholders}))"
        )
        params.extend(cleaned)

    where_sql = f"WHERE {' AND '.join(clauses)}" if clauses else ""
    query = f"SELECT r.id FROM recipes r {where_sql} ORDER BY RANDOM() LIMIT 1"
    row = conn.execute(query, params).fetchone()
    if not row:
        raise HTTPException(status_code=404, detail="No recipe available for selected random mode")
    return row["id"]
