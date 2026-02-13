# FastAPI Authentication App - Implementation Plan

## Overview
Build a basic authentication application using FastAPI, SQLModel as ORM, and SQLite as the database.

## Architecture

### Tech Stack
- **FastAPI**: Modern web framework for building APIs
- **SQLModel**: ORM built on Pydantic and SQLAlchemy
- **SQLite**: File-based database
- **PyJWT**: JWT token generation and validation
- **Passlib**: Password hashing with bcrypt
- **Python-dotenv**: Environment variable management

## Project Structure
```
fast-api-auth/
├── app/
│   ├── __init__.py
│   ├── main.py           # FastAPI app initialization
│   ├── config.py         # Configuration settings
│   ├── models.py         # SQLModel models
│   ├── schemas.py        # Pydantic schemas for request/response
│   ├── auth.py           # Authentication utilities (JWT, password hashing)
│   ├── dependencies.py   # FastAPI dependencies (auth middleware)
│   └── database.py       # Database connection setup
├── .env                  # Environment variables
├── .gitignore
├── requirements.txt      # Python dependencies
└── prp.md               # This plan file
```

## Implementation Steps

### Step 1: Project Setup
1. Create the project directory structure
2. Create `.gitignore` file (ignore `__pycache__`, `.env`, `*.db`)
3. Create `requirements.txt` with all dependencies

### Step 2: Database Layer (`database.py`)
- Create SQLModel database engine
- Create function to initialize/create database tables
- Define get_session dependency for database access

### Step 3: Models (`models.py`)
Define SQLModel models:
- `User` (table model)
  - `id`: Primary key
  - `username`: Unique, indexed
  - `email`: Unique, indexed
  - `hashed_password`: String (storing bcrypt hash)
  - `is_active`: Boolean, default True
  - `created_at`: DateTime

### Step 4: Schemas (`schemas.py`)
Define Pydantic schemas for API:
- `UserBase`: Base fields (username, email)
- `UserCreate`: User registration (username, email, password)
- `UserLogin`: Login credentials (username, password)
- `UserResponse`: User data returned to client (id, username, email, is_active)
- `Token`: JWT token response (access_token, token_type)
- `TokenData`: JWT payload data (username)

### Step 5: Configuration (`config.py`)
- Load environment variables
- Define `SECRET_KEY` for JWT signing
- Define `ALGORITHM` (HS256)
- Define `ACCESS_TOKEN_EXPIRE_MINUTES`

### Step 6: Authentication Utilities (`auth.py`)
- `verify_password()`: Verify plain password against hashed password
- `get_password_hash()`: Hash plain password using bcrypt
- `create_access_token()`: Generate JWT token with expiration
- `get_current_user()`: FastAPI dependency to validate JWT and get current user
- `authenticate_user()`: Verify user credentials and return user if valid

### Step 7: Dependencies (`dependencies.py`)
- Create FastAPI dependency injection for:
  - Database session (`get_db`)
  - Current authenticated user (`get_current_user`)

### Step 8: Main Application (`main.py`)
Create FastAPI app with endpoints:

#### Endpoints
1. `POST /auth/register` - Register new user
   - Input: UserCreate (username, email, password)
   - Validate: username/email uniqueness, password strength
   - Output: UserResponse

2. `POST /auth/login` - Login user
   - Input: UserLogin (username, password)
   - Output: Token (access_token, token_type)

3. `GET /users/me` - Get current user profile
   - Requires authentication (JWT token)
   - Output: UserResponse

4. `GET /users/` - List all users (optional admin endpoint)
   - Requires authentication
   - Output: List[UserResponse]

## Security Considerations
- Passwords hashed with bcrypt (via Passlib)
- JWT tokens with expiration
- HTTPS recommended for production (SECRET_KEY in env)
- Rate limiting considerations for production
- Input validation via Pydantic schemas

## Dependencies (requirements.txt)
```
fastapi==0.109.0
uvicorn[standard]==0.27.0
sqlmodel==0.0.14
pydantic==2.5.3
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
python-dotenv==1.0.0
```

## Verification / Testing

### Manual Testing Steps
1. Install dependencies: `pip install -r requirements.txt`
2. Create `.env` file with SECRET_KEY
3. Run the server: `uvicorn app.main:app --reload`
4. Test endpoints using curl or Postman:
   - Register a new user
   - Login with credentials
   - Access protected endpoint with token
   - Test invalid token/missing token scenarios

### Test Commands (curl examples)
```bash
# Register
curl -X POST "http://localhost:8000/auth/register" \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","email":"test@example.com","password":"securepass123"}'

# Login
curl -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","password":"securepass123"}'

# Get current user (replace TOKEN with actual token)
curl -X GET "http://localhost:8000/users/me" \
  -H "Authorization: Bearer TOKEN"
```

### Success Criteria
- Database file `test.db` created successfully
- User can register with unique username/email
- Login returns valid JWT token
- Protected endpoints work with valid token
- Protected endpoints reject invalid/missing tokens
- Passwords are hashed (not stored in plain text)