<div align="center">

# Hello World - FastAPI Learning Template

**Perfect for learning FastAPI fundamentals and starting new projects**

*This project was bootstrapped with [FastAPI Gen](https://github.com/mirpo/fastapi-gen)*

[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com)
[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://python.org)

</div>

---

## Project Summary

This project is a FastAPI application designed to demonstrate essential backend development patterns, now enhanced with PostgreSQL integration and Dockerization. It showcases how to build a robust API, manage configuration, handle database interactions, and deploy using containers.

**Key Technologies & Libraries:**

*   **FastAPI**: A modern, fast (high-performance) web framework for building APIs with Python 3.8+ based on standard Python type hints.
*   **PostgreSQL**: A powerful, open-source object-relational database system used for data storage.
*   **Docker & Docker Compose**: Tools for containerizing the application and its database, ensuring consistent environments across development and production.
*   **SQLAlchemy**: A Python SQL toolkit and Object Relational Mapper (ORM) that gives developers the full power of SQL. It's used here for interacting with the PostgreSQL database.
*   **Psycopg**: A PostgreSQL adapter for Python, providing the actual connectivity to the database when used with SQLAlchemy.
*   **Alembic**: A lightweight database migration tool for usage with SQLAlchemy. It manages schema changes over time.
*   **Pydantic / Pydantic-Settings**: Used for data validation, settings management, and type hinting, ensuring data integrity and structured configuration.
*   **Uvicorn**: A lightning-fast ASGI server, used to serve the FastAPI application.

## What You'll Build

A FastAPI application focused on core CRUD (Create, Read, Update, Delete) operations for different models, with robust database integration, structured configuration management, and Docker-based deployment.

## Quick Start

```bash
# You're already here! Just run:
make start

# Or manually:
uvicorn src.main:app --reload
```

Open [http://localhost:8000/docs](http://localhost:8000/docs) to see your interactive API documentation.

## Running with Docker

To run the application using Docker Compose:

1.  Build and start the services:
    ```bash
    docker compose up --build
    ```
2.  Apply database migrations (run this command only after the `db` service is healthy):
    ```bash
    docker compose run web uv run alembic upgrade head
    ```

Open [http://localhost:8000/docs](http://localhost:8000/docs) to see your interactive API documentation.

---

## API Endpoints

### Post Operations
```http
POST /posts/              # Create a new post
GET  /posts/              # Retrieve all posts
```

### Item Operations
```http
POST /items/              # Create a new item
GET  /items/              # Retrieve all items
GET  /items/{item_id}     # Retrieve a single item by ID
PUT  /items/{item_id}     # Update an existing item
DELETE /items/{item_id}   # Delete an item by ID
```

## Development Commands

| Command      | Description                                  |
| ------------ | -------------------------------------------- |
| `make start` | Run app in development mode with auto-reload |
| `make test`  | Run comprehensive test suite                 |
| `make lint`  | Run code quality checks with Ruff            |

## Project Structure

```
with_postgres/
├── alembic/                 # Alembic migration scripts
├── src/
│   ├── __init__.py
│   ├── config.py            # Application settings and configuration
│   ├── crud.py              # Database CRUD operations
│   ├── database.py          # Database engine, session, and base
│   ├── models.py            # SQLAlchemy ORM models
│   ├── schemas.py           # Pydantic schemas for data validation
│   ├── utils.py             # Utility functions (e.g., logging)
│   └── main.py              # Main FastAPI application
├── tests/
│   ├── test_main.py         # Comprehensive test suite
│   └── __init__.py
├── pyproject.toml           # Project configuration (uv)
├── .env_dev                 # Environment variables
├── Makefile                 # Development commands
├── .gitignore
├── Dockerfile               # Docker configuration for the application
├── docker-compose.yml       # Docker Compose setup for web and database services
└── README.md                # This file
```