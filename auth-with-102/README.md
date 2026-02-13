# FastAPI Authentication App

A basic authentication application built with FastAPI, SQLModel (ORM), and SQLite database.

## Features

- User registration with username and email
- User login with JWT token authentication
- Protected endpoints that require authentication
- Password hashing with argon2
- SQLite database with SQLModel
- Layered architecture with service layer
- API versioning with `/api/v1` prefix
- Configurable database via environment variables
- Test infrastructure with pytest

## Project Structure

```
fast-api-auth/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI app instance only
│   ├── api/                    # API routes layer
│   │   ├── __init__.py
│   │   ├── deps.py             # FastAPI dependencies
│   │   └── v1/                 # API versioning
│   │       ├── __init__.py
│   │       ├── api.py          # Router aggregation
│   │       └── endpoints/      # Route modules
│   │           ├── __init__.py
│   │           ├── auth.py     # Auth endpoints
│   │           └── users.py    # User endpoints
│   ├── core/                   # Core components
│   │   ├── __init__.py
│   │   ├── config.py           # Configuration settings
│   │   ├── security.py         # Security (JWT, password hashing)
│   │   └── database.py         # Database connection & session
│   ├── models/                 # Database models
│   │   ├── __init__.py
│   │   └── user.py
│   ├── schemas/                # Pydantic schemas
│   │   ├── __init__.py
│   │   ├── token.py
│   │   └── user.py
│   └── services/               # Business logic layer
│       ├── __init__.py
│       ├── auth_service.py
│       └── user_service.py
├── tests/                      # Test files
│   ├── __init__.py
│   ├── conftest.py             # Pytest fixtures
│   ├── test_auth.py
│   └── test_users.py
├── .env.example
├── .gitignore
├── pyproject.toml              # Modern Python project config
└── README.md
```

## Setup

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Create environment file

Copy `.env.example` to `.env`:

```bash
cp .env.example .env
```

Edit `.env` and set your secret key:

```
SECRET_KEY=your-super-secret-key-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
DATABASE_URL=sqlite:///./test.db
```

### 3. Run the server

```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

## API Endpoints

### Root
- `GET /` - API information and available endpoints

### Authentication (v1)
- `POST /api/v1/auth/register` - Register a new user
- `POST /api/v1/auth/login` - Login and get JWT token

### Users (v1)
- `GET /api/v1/users/me` - Get current user profile (requires authentication)
- `GET /api/v1/users/` - List all users (requires authentication)

## API Documentation

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Usage Examples

### Register a new user

```bash
curl -X POST "http://localhost:8000/api/v1/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "securepass123"
  }'
```

Response:
```json
{
  "id": 1,
  "username": "testuser",
  "email": "test@example.com",
  "is_active": true,
  "created_at": "2024-01-01T12:00:00"
}
```

### Login

```bash
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=testuser&password=securepass123"
```

Response:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### Get current user profile

Replace `YOUR_TOKEN` with the access token from login:

```bash
curl -X GET "http://localhost:8000/api/v1/users/me" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### List all users

```bash
curl -X GET "http://localhost:8000/api/v1/users/" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

## Running Tests

```bash
# Install test dependencies
pip install -e ".[dev]"

# Run all tests
pytest tests/ -v

# Run specific test file
pytest tests/test_auth.py -v
```

## Database

The SQLite database file `test.db` will be created automatically when the server starts.

## Architecture

This project follows a layered architecture:

1. **API Layer** (`app/api/`): FastAPI routes and dependencies
2. **Service Layer** (`app/services/`): Business logic
3. **Data Layer** (`app/models/`): Database models
4. **Core Layer** (`app/core/`): Configuration, security, database connections

This separation of concerns makes the codebase:
- Easier to test
- More maintainable
- Better organized for scaling

## Security Notes

- Change `SECRET_KEY` in `.env` before production use
- Use HTTPS in production
- Consider adding rate limiting
- Add password strength validation
- Implement role-based access control for admin endpoints

## License

MIT