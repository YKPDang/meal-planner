import sqlite3

from fastapi import HTTPException


def list_tags(conn: sqlite3.Connection) -> list[dict]:
    rows = conn.execute("SELECT id, name FROM tags ORDER BY name").fetchall()
    return [dict(row) for row in rows]


def create_tag(conn: sqlite3.Connection, payload: dict) -> dict:
    name = str(payload.get("name", "")).strip()
    if not name:
        raise HTTPException(status_code=400, detail="Tag name is required")
    conn.execute("INSERT OR IGNORE INTO tags(name) VALUES (?)", (name,))
    row = conn.execute("SELECT id, name FROM tags WHERE name = ?", (name,)).fetchone()
    conn.commit()
    return dict(row)


def delete_tag(conn: sqlite3.Connection, tag_id: int) -> None:
    conn.execute("DELETE FROM tags WHERE id = ?", (tag_id,))
    conn.commit()
