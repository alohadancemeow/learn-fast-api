# Plan for FastAPI with MongoDB CRUD Application

1.  **Project Setup**: 
    *   Create the `with-mongo` directory.
    *   Create a `requirements.txt` file with the necessary dependencies.

2.  **Install Dependencies**: 
    *   Install `fastapi`, `uvicorn`, and `pymongo`.

3.  **MongoDB Connection**: 
    *   Create a `database.py` module to handle the connection to a MongoDB database using `pymongo`.
    *   This module will include a function to get the database instance.

4.  **Data Model**: 
    *   Create a `schemas.py` module to define the data models using Pydantic.
    *   Define a `ItemBase` model for the basic item attributes.
    *   Define a `ItemCreate` model that inherits from `ItemBase` for creating items.
    *   Define a `Item` model that inherits from `ItemBase` for reading items from the database, including the `id` field.

5.  **CRUD Operations**: 
    *   Create a `crud.py` module to implement the CRUD functions:
        *   `create_item`: Add a new item to the MongoDB collection.
        *   `get_item`: Retrieve a single item by its ID.
        *   `get_items`: Retrieve all items.
        *   `update_item`: Modify an existing item.
        *   `delete_item`: Remove an item.

6.  **FastAPI Endpoints**: 
    *   Create a `main.py` file to define the FastAPI endpoints for each CRUD operation.
    *   These endpoints will use the functions from the `crud.py` module.

7.  **Configuration**: 
    *   Explain how to configure the MongoDB connection string, possibly using an environment variable. For this example, we will hardcode it in the `database.py` file with a clear comment on how to change it.

8.  **Instructions**: 
    *   Provide clear instructions on how to set up and run the application.
