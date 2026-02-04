# app/routers/todos.py

"""
This module defines the API routes for todo management.
"""

from fastapi import APIRouter, Depends, HTTPException
from .. import schemas, crud, auth
from typing import List
from typing import List

router = APIRouter()

@router.post("/todos/", response_model=schemas.Todo)
async def create_todo_endpoint(todo: schemas.TodoCreate, current_user: schemas.User = Depends(auth.get_current_user)):
    return await crud.create_todo(todo=todo, owner_id=current_user.id)

@router.get("/todos/", response_model=List[schemas.Todo])
async def read_todos_endpoint(current_user: schemas.User = Depends(auth.get_current_user)):
    return await crud.get_todos(owner_id=current_user.id)

@router.get("/todos/{todo_id}", response_model=schemas.Todo)
async def read_todo_endpoint(todo_id: int, current_user: schemas.User = Depends(auth.get_current_user)):
    db_todo = await crud.get_todo(todo_id=todo_id, owner_id=current_user.id)
    if not db_todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return db_todo

@router.put("/todos/{todo_id}", response_model=schemas.Todo)
async def update_todo_endpoint(todo_id: int, todo: schemas.TodoCreate, current_user: schemas.User = Depends(auth.get_current_user)):
    db_todo = await crud.get_todo(todo_id=todo_id, owner_id=current_user.id)
    if not db_todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return await crud.update_todo(todo_id=todo_id, todo=todo, owner_id=current_user.id)

@router.delete("/todos/{todo_id}", status_code=204)
async def delete_todo_endpoint(todo_id: int, current_user: schemas.User = Depends(auth.get_current_user)):
    db_todo = await crud.get_todo(todo_id=todo_id, owner_id=current_user.id)
    if not db_todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    await crud.delete_todo(todo_id=todo_id, owner_id=current_user.id)
    return
