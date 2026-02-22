import os
import sqlite3
from contextlib import closing
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import Literal

from fastapi import APIRouter, FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

DB_PATH = Path(os.getenv("DATABASE_PATH", "/data/meal_planner.db"))
SMART_RANDOM_LOOKBACK_DAYS = int(os.getenv("SMART_RANDOM_LOOKBACK_DAYS", "7"))


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


def get_connection() -> sqlite3.Connection:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


def init_db() -> None:
    with closing(get_connection()) as conn:
        conn.executescript(
            """
            CREATE TABLE IF NOT EXISTS recipes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                description TEXT DEFAULT ''
            );

            CREATE TABLE IF NOT EXISTS ingredients (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                recipe_id INTEGER NOT NULL,
                unit TEXT DEFAULT '',
                item TEXT NOT NULL,
                FOREIGN KEY (recipe_id) REFERENCES recipes(id) ON DELETE CASCADE
            );

            CREATE TABLE IF NOT EXISTS tags (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL
            );

            CREATE TABLE IF NOT EXISTS recipe_tags (
                recipe_id INTEGER NOT NULL,
                tag_id INTEGER NOT NULL,
                PRIMARY KEY(recipe_id, tag_id),
                FOREIGN KEY (recipe_id) REFERENCES recipes(id) ON DELETE CASCADE,
                FOREIGN KEY (tag_id) REFERENCES tags(id) ON DELETE CASCADE
            );

            CREATE TABLE IF NOT EXISTS meal_plan (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                day TEXT UNIQUE NOT NULL,
                recipe_id INTEGER,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (recipe_id) REFERENCES recipes(id) ON DELETE SET NULL
            );
            """
        )
        conn.commit()


def attach_tags(conn: sqlite3.Connection, recipe_id: int, tags: list[str]) -> None:
    cleaned = sorted({tag.strip() for tag in tags if tag.strip()})
    conn.execute("DELETE FROM recipe_tags WHERE recipe_id = ?", (recipe_id,))
    for tag in cleaned:
        conn.execute("INSERT OR IGNORE INTO tags(name) VALUES (?)", (tag,))
        tag_id = conn.execute("SELECT id FROM tags WHERE name = ?", (tag,)).fetchone()["id"]
        conn.execute(
            "INSERT OR IGNORE INTO recipe_tags(recipe_id, tag_id) VALUES (?, ?)",
            (recipe_id, tag_id),
        )


def recipe_details(conn: sqlite3.Connection, recipe_id: int) -> dict:
    recipe = conn.execute(
        "SELECT id, name, description FROM recipes WHERE id = ?", (recipe_id,)
    ).fetchone()
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")

    ingredients = conn.execute(
        "SELECT id, unit, item FROM ingredients WHERE recipe_id = ? ORDER BY id", (recipe_id,)
    ).fetchall()
    tags = conn.execute(
        """
        SELECT t.name
        FROM tags t
        JOIN recipe_tags rt ON t.id = rt.tag_id
        WHERE rt.recipe_id = ?
        ORDER BY t.name
        """,
        (recipe_id,),
    ).fetchall()

    return {
        "id": recipe["id"],
        "name": recipe["name"],
        "description": recipe["description"],
        "ingredients": [dict(row) for row in ingredients],
        "tags": [row["name"] for row in tags],
    }


def select_random_recipe(
    conn: sqlite3.Connection,
    target_day: date,
    mode: str,
    tags: list[str],
    lookback_days: int,
) -> int:
    params: list[object] = []
    clauses: list[str] = []

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

    if mode == "filtered":
        cleaned = sorted({tag.strip() for tag in tags if tag.strip()})
        if not cleaned:
            raise HTTPException(status_code=400, detail="Filtered mode requires one or more tags")
        placeholders = ",".join(["?" for _ in cleaned])
        clauses.append(
            f"r.id IN (SELECT rt.recipe_id FROM recipe_tags rt JOIN tags t ON rt.tag_id = t.id WHERE t.name IN ({placeholders}))"
        )
        params.extend(cleaned)

    where_sql = f"WHERE {' AND '.join(clauses)}" if clauses else ""
    query = f"SELECT r.id FROM recipes r {where_sql} ORDER BY RANDOM() LIMIT 1"
    row = conn.execute(query, params).fetchone()
    if not row:
        raise HTTPException(status_code=404, detail="No recipe available for selected random mode")
    return row["id"]


app = FastAPI(
    title="Meal Planner API",
    docs_url="/api/docs",
    openapi_url="/api/openapi.json",
)
api = APIRouter(prefix="/api")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup() -> None:
    init_db()


@api.get("/health")
def health() -> dict:
    return {"status": "ok"}


@api.get("/recipes")
def list_recipes() -> list[dict]:
    with closing(get_connection()) as conn:
        rows = conn.execute("SELECT id FROM recipes ORDER BY name").fetchall()
        return [recipe_details(conn, row["id"]) for row in rows]


@api.get("/recipes/{recipe_id}")
def get_recipe(recipe_id: int) -> dict:
    with closing(get_connection()) as conn:
        return recipe_details(conn, recipe_id)


@api.post("/recipes", status_code=201)
def create_recipe(payload: RecipeIn) -> dict:
    with closing(get_connection()) as conn:
        cursor = conn.execute(
            "INSERT INTO recipes(name, description) VALUES (?, ?)",
            (payload.name.strip(), payload.description.strip()),
        )
        recipe_id = cursor.lastrowid
        for ingredient in payload.ingredients:
            conn.execute(
                "INSERT INTO ingredients(recipe_id, unit, item) VALUES (?, ?, ?)",
                (recipe_id, ingredient.unit.strip(), ingredient.item.strip()),
            )
        attach_tags(conn, recipe_id, payload.tags)
        conn.commit()
        return recipe_details(conn, recipe_id)


@api.put("/recipes/{recipe_id}")
def update_recipe(recipe_id: int, payload: RecipeIn) -> dict:
    with closing(get_connection()) as conn:
        exists = conn.execute("SELECT id FROM recipes WHERE id = ?", (recipe_id,)).fetchone()
        if not exists:
            raise HTTPException(status_code=404, detail="Recipe not found")

        conn.execute(
            "UPDATE recipes SET name = ?, description = ? WHERE id = ?",
            (payload.name.strip(), payload.description.strip(), recipe_id),
        )
        conn.execute("DELETE FROM ingredients WHERE recipe_id = ?", (recipe_id,))
        for ingredient in payload.ingredients:
            conn.execute(
                "INSERT INTO ingredients(recipe_id, unit, item) VALUES (?, ?, ?)",
                (recipe_id, ingredient.unit.strip(), ingredient.item.strip()),
            )
        attach_tags(conn, recipe_id, payload.tags)
        conn.commit()
        return recipe_details(conn, recipe_id)


@api.delete("/recipes/{recipe_id}", status_code=204)
def delete_recipe(recipe_id: int) -> None:
    with closing(get_connection()) as conn:
        conn.execute("DELETE FROM recipes WHERE id = ?", (recipe_id,))
        conn.commit()


@api.get("/tags")
def list_tags() -> list[dict]:
    with closing(get_connection()) as conn:
        rows = conn.execute("SELECT id, name FROM tags ORDER BY name").fetchall()
        return [dict(row) for row in rows]


@api.post("/tags", status_code=201)
def create_tag(tag: dict) -> dict:
    name = str(tag.get("name", "")).strip()
    if not name:
        raise HTTPException(status_code=400, detail="Tag name is required")
    with closing(get_connection()) as conn:
        conn.execute("INSERT OR IGNORE INTO tags(name) VALUES (?)", (name,))
        row = conn.execute("SELECT id, name FROM tags WHERE name = ?", (name,)).fetchone()
        conn.commit()
        return dict(row)


@api.delete("/tags/{tag_id}", status_code=204)
def delete_tag(tag_id: int) -> None:
    with closing(get_connection()) as conn:
        conn.execute("DELETE FROM tags WHERE id = ?", (tag_id,))
        conn.commit()


@api.get("/meal-plan")
def get_meal_plan(start_date: date = Query(default_factory=date.today), days: int = 7) -> list[dict]:
    with closing(get_connection()) as conn:
        result = []
        for offset in range(days):
            day_value = start_date + timedelta(days=offset)
            row = conn.execute(
                "SELECT recipe_id FROM meal_plan WHERE day = ?", (day_value.isoformat(),)
            ).fetchone()
            recipe = recipe_details(conn, row["recipe_id"]) if row and row["recipe_id"] else None
            result.append({"day": day_value.isoformat(), "recipe": recipe})
        return result


@api.put("/meal-plan/{day}")
def assign_recipe(day: date, payload: MealPlanAssign) -> dict:
    with closing(get_connection()) as conn:
        if payload.recipe_id is not None:
            exists = conn.execute("SELECT id FROM recipes WHERE id = ?", (payload.recipe_id,)).fetchone()
            if not exists:
                raise HTTPException(status_code=404, detail="Recipe not found")
        conn.execute(
            "INSERT INTO meal_plan(day, recipe_id, created_at) VALUES (?, ?, ?) "
            "ON CONFLICT(day) DO UPDATE SET recipe_id = excluded.recipe_id, created_at = excluded.created_at",
            (day.isoformat(), payload.recipe_id, datetime.utcnow().isoformat()),
        )
        conn.commit()
        recipe = recipe_details(conn, payload.recipe_id) if payload.recipe_id else None
        return {"day": day.isoformat(), "recipe": recipe}


@api.post("/meal-plan/{day}/random")
def randomize_recipe(day: date, payload: RandomizeRequest) -> dict:
    lookback = payload.lookback_days if payload.lookback_days is not None else SMART_RANDOM_LOOKBACK_DAYS
    with closing(get_connection()) as conn:
        recipe_id = select_random_recipe(conn, day, payload.mode, payload.tags, lookback)
        conn.execute(
            "INSERT INTO meal_plan(day, recipe_id, created_at) VALUES (?, ?, ?) "
            "ON CONFLICT(day) DO UPDATE SET recipe_id = excluded.recipe_id, created_at = excluded.created_at",
            (day.isoformat(), recipe_id, datetime.utcnow().isoformat()),
        )
        conn.commit()
        return {"day": day.isoformat(), "recipe": recipe_details(conn, recipe_id), "mode": payload.mode}


app.include_router(api)
