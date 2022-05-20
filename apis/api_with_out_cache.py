from fastapi import APIRouter

from utils.mock_response import get_todo_all, get_todo_by_id

router = APIRouter(
    prefix="/todo",
    tags=["without-cache/todos"],
    responses={404: {"message": "Not found"}}
)


@router.get("/find/all")
async def find_all():
    return get_todo_all()


@router.get("/find/{todo_id}")
async def find_by_id(todo_id: int):
    return get_todo_by_id(todo_id)
