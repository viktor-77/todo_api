# TODO API -- FastAPI + MongoDB + JWT

Production‑grade pet project with DDD layers, SOLID/KISS/DRY and 12‑Factor discipline.  
**Strict settings**: there are **no defaults** -- the app fails fast if any required env var is missing.

## Features
- Versioned API `/api/v1`
- JWT authentication (register, login, me)
- Task domain with `status` (`new | pending | in_progress | resolved`) and `priority` (`low | medium | high | urgent`)
- Per‑user tasks (unique title per owner, case‑insensitive)
- Full CRUD + list with pagination and filters
- Centralized exception handling
- Proper indexes for MongoDB
- Multi‑stage Dockerfile, non‑root runtime
- One image, different processes: `APP_MODE=development|test|production`

## Quick start (Docker)
```bash
# development (auto-reload)
APP_MODE=development docker compose up --build

# production (gunicorn)
APP_MODE=production docker compose up --build -d

# test (wire to your pytest later)
APP_MODE=test docker compose up --build
API: http://localhost:8000
Authentication
POST /api/v1/auth/register -- JSON: { "username": "...", "email": "...", "password": "..." }
POST /api/v1/auth/login -- application/x-www-form-urlencoded (OAuth2 Password): username, password

 Returns: { "access_token": "...", "token_type": "bearer" }
GET /api/v1/auth/me -- requires Authorization: Bearer <token>
Use the token for all task endpoints below.
Task endpoints
POST   /api/v1/tasks/
GET    /api/v1/tasks/{task_id}
GET    /api/v1/tasks/ (filters: status, priority; pagination: limit, skip; sort: created_at|updated_at, asc|desc)
PUT    /api/v1/tasks/{task_id}
PATCH  /api/v1/tasks/{task_id}
DELETE /api/v1/tasks/{task_id}
GET    /health
Run locally without Docker
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# export all required env vars or create env/.env.development from example:
export APP_MODE=development
cp env/.env.development.example env/.env.development

# (ensure a local Mongo is running or change MONGO_URL accordingly)
uvicorn app.main:app --reload
Configuration (no defaults)
Set all variables from the corresponding env/.env.<mode>.example file.
If any variable is missing, the app fails at startup (Pydantic Settings).