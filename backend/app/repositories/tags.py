import sqlite3

from fastapi import HTTPException

from backend.app.schemas import TagIn


def list_tags(conn: sqlite3.Connection) -> list[dict]:
    rows = conn.execute("SELECT id, name FROM tags ORDER BY name").fetchall()
    return [dict(row) for row in rows]


def create_tag(conn: sqlite3.Connection, payload: TagIn) -> dict:
    name = payload.name.strip()
    if not name:
        raise HTTPException(status_code=400, detail="Tag name is required")
    conn.execute("INSERT OR IGNORE INTO tags(name) VALUES (?)", (name,))
    row = conn.execute("SELECT id, name FROM tags WHERE name = ?", (name,)).fetchone()
    conn.commit()
    return dict(row)


def update_tag(conn: sqlite3.Connection, tag_id: int, payload: TagIn) -> dict:
    name = payload.name.strip()
    if not name:
        raise HTTPException(status_code=400, detail="Tag name is required")

    existing = conn.execute("SELECT id FROM tags WHERE id = ?", (tag_id,)).fetchone()
    if not existing:
        raise HTTPException(status_code=404, detail="Tag not found")

    conn.execute("UPDATE tags SET name = ? WHERE id = ?", (name, tag_id))
    row = conn.execute("SELECT id, name FROM tags WHERE id = ?", (tag_id,)).fetchone()
    conn.commit()
    return dict(row)


def delete_tag(conn: sqlite3.Connection, tag_id: int) -> None:
    conn.execute("DELETE FROM tags WHERE id = ?", (tag_id,))
    conn.commit()
