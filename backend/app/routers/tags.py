from fastapi import APIRouter, Depends

from backend.app.db import get_db
from backend.app.repositories import tags as tag_repo
from backend.app.schemas import TagIn


router = APIRouter()


@router.get("/tags")
def list_tags(conn=Depends(get_db)) -> list[dict]:
    return tag_repo.list_tags(conn)


@router.post("/tags", status_code=201)
def create_tag(payload: TagIn, conn=Depends(get_db)) -> dict:
    return tag_repo.create_tag(conn, payload)


@router.put("/tags/{tag_id}")
def update_tag(tag_id: int, payload: TagIn, conn=Depends(get_db)) -> dict:
    return tag_repo.update_tag(conn, tag_id, payload)


@router.delete("/tags/{tag_id}", status_code=204)
def delete_tag(tag_id: int, conn=Depends(get_db)) -> None:
    tag_repo.delete_tag(conn, tag_id)
