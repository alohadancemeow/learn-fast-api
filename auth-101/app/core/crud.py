# app/crud.py

"""
This module contains the CRUD (Create, Read, Update, Delete) operations
for interacting with the database.
"""

from . import schemas
from ..security import auth
from ..db.database import database, users_table, todos_table


#  --- User CRUD ---


async def get_user(username: str):
    query = users_table.select().where(users_table.c.username == username)
    return await database.fetch_one(query)


async def create_user(user: schemas.UserCreate):
    hashed_password = auth.get_password_hash(user.password)
    query = users_table.insert().values(
        username=user.username, hashed_password=hashed_password
    )
    last_record_id = await database.execute(query)
    return {**user.model_dump(), "id": last_record_id}


#  --- Todo CRUD ---


async def get_todos(owner_id: int):
    query = todos_table.select().where(todos_table.c.owner_id == owner_id)
    return await database.fetch_all(query)


async def get_all_todos():
    query = todos_table.select()
    return await database.fetch_all(query)


async def create_todo(todo: schemas.TodoCreate, owner_id: int):
    query = todos_table.insert().values(
        title=todo.title,
        description=todo.description,
        completed=todo.completed,
        owner_id=owner_id,
    )
    last_record_id = await database.execute(query)
    return {**todo.model_dump(), "id": last_record_id, "owner_id": owner_id}


async def get_todo(todo_id: int):
    query = todos_table.select().where(todos_table.c.id == todo_id)
    return await database.fetch_one(query)


async def update_todo(todo_id: int, todo: schemas.TodoCreate, owner_id: int):
    update_query = (
        todos_table.update()
        .where(todos_table.c.id == todo_id, todos_table.c.owner_id == owner_id)
        .values(
            title=todo.title, description=todo.description, completed=todo.completed
        )
    )
    await database.execute(update_query)
    return await get_todo(todo_id=todo_id)


async def delete_todo(todo_id: int, owner_id: int):
    delete_query = todos_table.delete().where(
        todos_table.c.id == todo_id, todos_table.c.owner_id == owner_id
    )
    await database.execute(delete_query)
    return
