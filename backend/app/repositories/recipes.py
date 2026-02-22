import sqlite3

from fastapi import HTTPException

from backend.app.schemas import RecipeIn


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


def list_recipe_ids(conn: sqlite3.Connection) -> list[int]:
    rows = conn.execute("SELECT id FROM recipes ORDER BY name").fetchall()
    return [row["id"] for row in rows]


def create_recipe(conn: sqlite3.Connection, payload: RecipeIn) -> dict:
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


def update_recipe(conn: sqlite3.Connection, recipe_id: int, payload: RecipeIn) -> dict:
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


def delete_recipe(conn: sqlite3.Connection, recipe_id: int) -> None:
    conn.execute("DELETE FROM recipes WHERE id = ?", (recipe_id,))
    conn.commit()
