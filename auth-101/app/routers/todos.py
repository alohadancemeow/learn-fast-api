# app/routers/todos.py

"""
This module defines the API routes for todo management.
"""

from fastapi import APIRouter, Depends, HTTPException
from ..core import schemas, crud
from ..security import auth
from typing import List

router = APIRouter()


@router.get("/todos/", response_model=List[schemas.Todo])
async def read_todos_endpoint():
    """
    Retrieves a list of all Todo items.

    This endpoint returns all todos available in the system. It is a public route
    accessible without authentication.

    Returns:
        List[schemas.Todo]: A list of all todo items.
    """
    return await crud.get_all_todos()


@router.get("/todos/{todo_id}", response_model=schemas.Todo)
async def read_todo_endpoint(todo_id: int):
    """
    Retrieves a specific Todo item by its ID.

    This endpoint fetches the details of a single todo item. It is a public route.

    Args:
        todo_id (int): The ID of the todo item to retrieve.

    Returns:
        schemas.Todo: The requested todo item.

    Raises:
        HTTPException (404): If the todo item with the specified ID is not found.
    """
    db_todo = await crud.get_todo(todo_id=todo_id)
    if not db_todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return db_todo


# Authenticated Routes
@router.post("/todos/", response_model=schemas.Todo)
async def create_todo_endpoint(
    todo: schemas.TodoCreate,
    current_user: schemas.User = Depends(auth.get_current_user),
):
    """
    Creates a new Todo item for the authenticated user.

    This endpoint allows an authenticated user to create a new todo item. The item
    will be associated with the user's ID.

    Args:
        todo (schemas.TodoCreate): The todo item data (title, description, etc.).
        current_user (schemas.User): The currently authenticated user.

    Returns:
        schemas.Todo: The newly created todo item.
    """
    return await crud.create_todo(todo=todo, owner_id=current_user.id)


@router.put("/todos/{todo_id}", response_model=schemas.Todo)
async def update_todo_endpoint(
    todo_id: int,
    todo: schemas.TodoCreate,
    current_user: schemas.User = Depends(auth.get_current_user),
):
    """
    Updates an existing Todo item.

    This endpoint allows an authenticated user to update a todo item that they own.
    It verifies that the todo exists and belongs to the current user before updating.

    Args:
        todo_id (int): The ID of the todo item to update.
        todo (schemas.TodoCreate): The new data for the todo item.
        current_user (schemas.User): The currently authenticated user.

    Returns:
        schemas.Todo: The updated todo item.

    Raises:
        HTTPException (404): If the todo item is not found or does not belong to the user.
    """
    db_todo = await crud.get_todo(todo_id=todo_id)
    if not db_todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return await crud.update_todo(todo_id=todo_id, todo=todo, owner_id=current_user.id)


@router.delete("/todos/{todo_id}", status_code=204)
async def delete_todo_endpoint(
    todo_id: int, current_user: schemas.User = Depends(auth.get_current_user)
):
    """
    Deletes a Todo item.

    This endpoint allows an authenticated user to delete a todo item that they own.
    It verifies ownerhsip before deletion.

    Args:
        todo_id (int): The ID of the todo item to delete.
        current_user (schemas.User): The currently authenticated user.

    Returns:
        None: Returns a 204 No Content status code upon successful deletion.

    Raises:
        HTTPException (404): If the todo item is not found or does not belong to the user.
    """
    db_todo = await crud.get_todo(todo_id=todo_id)
    if not db_todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    await crud.delete_todo(todo_id=todo_id, owner_id=current_user.id)
    return
