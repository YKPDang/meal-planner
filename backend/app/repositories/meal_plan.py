import sqlite3
from datetime import date, datetime, timedelta, timezone


def get_meal_plan(conn: sqlite3.Connection, start_date: date, days: int) -> list[dict]:
    result: list[dict] = []
    for offset in range(days):
        day_value = start_date + timedelta(days=offset)
        row = conn.execute(
            "SELECT recipe_id FROM meal_plan WHERE day = ?", (day_value.isoformat(),)
        ).fetchone()
        result.append({"day": day_value.isoformat(), "recipe_id": row["recipe_id"] if row else None})
    return result


def upsert_meal_plan(conn: sqlite3.Connection, day: date, recipe_id: int | None) -> None:
    conn.execute(
        "INSERT INTO meal_plan(day, recipe_id, created_at) VALUES (?, ?, ?) "
        "ON CONFLICT(day) DO UPDATE SET recipe_id = excluded.recipe_id, created_at = excluded.created_at",
        (day.isoformat(), recipe_id, datetime.now(timezone.utc).isoformat()),
    )
    conn.commit()
