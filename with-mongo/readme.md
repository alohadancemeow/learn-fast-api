# FastAPI with MongoDB CRUD Application

This project is a simple CRUD (Create, Read, Update, Delete) application built with FastAPI and MongoDB. It provides a RESTful API for managing a collection of items. The application is containerized using Docker and can be easily run with Docker Compose.

## Features

*   **FastAPI**: A modern, fast (high-performance), web framework for building APIs with Python 3.7+ based on standard Python type hints.
*   **MongoDB**: A NoSQL database for storing and retrieving data.
*   **Pydantic**: Data validation and settings management using Python type annotations.
*   **Dockerized**: The application and its database are containerized for easy setup and deployment.
*   **CRUD Operations**: Basic CRUD functionality for managing items.
*   **Health Check**: An endpoint to check the status of the API and the database connection.

## Project Structure

```
with-mongo/
├── .env.example        # Example environment variables
├── Dockerfile          # Dockerfile for the FastAPI application
├── crud.py             # CRUD operations for interacting with the database
├── database.py         # MongoDB connection setup
├── docker-compose.yml  # Docker Compose file for running the application and database
├── main.py             # Main FastAPI application file with API endpoints
├── readme.md           # This file
├── requirements.txt    # Python dependencies
└── schemas.py          # Pydantic models for data validation
```

## Getting Started

### Prerequisites

*   [Python 3.7+](https://www.python.org/downloads/)
*   [Docker](https://www.docker.com/get-started) and [Docker Compose](https://docs.docker.com/compose/install/)

### Installation

1.  **Clone the repository (or download the files).**

2.  **Create a `.env` file** from the `.env.example` file and update the environment variables if needed.
    ```bash
    cp .env.example .env
    ```

3.  **Install Python dependencies** (optional, if you want to run locally without Docker).
    ```bash
    pip install -r requirements.txt
    ```

## Usage

### Running with Docker Compose (Recommended)

This is the easiest way to get the application and the MongoDB database running.

1.  **Start the services:**
    ```bash
    docker compose up -d
    ```

2.  The application will be available at `http://localhost:8000`.

### Running Locally

If you prefer to run the application without Docker, you can do so by following these steps:

1.  **Start a MongoDB instance.** You can use a local installation or a cloud-based service like MongoDB Atlas. Make sure to update the `MONGO_URL` in your `.env` file.

2.  **Run the FastAPI application:**
    ```bash
    uvicorn main:app --reload
    ```

3.  The application will be available at `http://localhost:8000`.

## API Endpoints

The API documentation is available at `http://localhost:8000/docs` (Swagger UI) and `http://localhost:8000/redoc` (ReDoc).

*   `POST /items/`: Create a new item.
*   `GET /items/`: Retrieve all items.
*   `GET /items/{item_id}`: Retrieve a single item by its ID.
*   `PUT /items/{item_id}`: Update an existing item.
*   `DELETE /items/{item_id}`: Delete an item.
*   `GET /health`: Health check endpoint.

## Configuration

The following environment variables can be configured in the `.env` file:

*   `MONGO_URL`: The connection string for the MongoDB database. Default is `mongodb://localhost:27017/`.
