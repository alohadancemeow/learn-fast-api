# Project Requirements Prompt (PRP) - FastAPI Learning Project

## 1. Project Goal
To learn the fundamentals of FastAPI by building a simple, functional application that demonstrates:
- Basic application setup.
- Defining data models using Pydantic.
- Implementing Create, Read, Update, and Delete (CRUD) operations for a resource.
- User management and authentication using FastAPI's recommended approach (OAuth2 with Bearer Tokens).

## 2. Core Functionality

### 2.1 Todo Management
The application will manage "Todo" items, each having:
- A unique ID.
- A title (string).
- A description (optional string).
- A status (e.g., boolean for "completed" or an enum for "pending", "in-progress", "completed").
- An owner (the user who created it).

**Required Operations:**
- **Create Todo:** An authenticated user can create a new todo item.
- **Read All Todos:** An authenticated user can view all todo items they own.
- **Read Single Todo:** An authenticated user can retrieve a specific todo item by its ID, if they own it.
- **Update Todo:** An authenticated user can modify an existing todo item by its ID, if they own it.
- **Delete Todo:** An authenticated user can delete a todo item by its ID, if they own it.

### 2.2 User Management & Authentication
The application will provide basic user management and secure access to todo operations.

**Required Operations:**
- **User Registration:** Allow new users to register with a username and password.
- **User Login:** Users can log in with their credentials to obtain an authentication token (Bearer Token).
- **Protected Endpoints:** All Todo management endpoints (Create, Read, Update, Delete) must require a valid authentication token.
- **Get Current User:** An authenticated endpoint to retrieve information about the currently logged-in user.

## 3. Technologies & Libraries
-   **Web Framework:** FastAPI
-   **Programming Language:** Python 3.8+
-   **ASGI Server:** Uvicorn (for running the FastAPI application)
-   **Data Validation & Serialization:** Pydantic (integrated with FastAPI)
-   **Password Hashing:** `passlib[bcrypt]`
-   **JWT Token Handling:** `python-jose[jwt]`
-   **Database (Initial):** In-memory dictionary/list for simplicity during initial development.
-   **Database (Future Consideration/Upgrade):** SQLite or PostgreSQL for persistence (this will be a later step).

## 4. High-Level API Endpoints (Examples)

### User Endpoints
-   `POST /users/`: Register a new user.
-   `POST /token`: User login, returns an access token.
-   `GET /users/me/`: Retrieve details of the authenticated user.

### Todo Endpoints
-   `POST /todos/`: Create a new todo item (requires authentication).
-   `GET /todos/`: Retrieve all todo items for the authenticated user (requires authentication).
-   `GET /todos/{todo_id}`: Retrieve a specific todo item by ID for the authenticated user (requires authentication).
-   `PUT /todos/{todo_id}`: Update a specific todo item by ID for the authenticated user (requires authentication).
-   `DELETE /todos/{todo_id}`: Delete a specific todo item by ID for the authenticated user (requires authentication).

## 5. Development Steps (High-Level)
1.  Project Setup: Virtual environment, dependency installation.
2.  Basic FastAPI App: "Hello World" endpoint.
3.  Data Modeling: Define Pydantic models for Todo and User.
4.  In-Memory Storage: Implement simple data storage.
5.  CRUD Operations: Implement API endpoints for Todo management.
6.  User Authentication: Implement user registration, login, and token generation.
7.  Protecting Endpoints: Integrate authentication into Todo endpoints.
8.  Database Integration: (Optional, as a later step) Migrate from in-memory to a persistent database.

---
