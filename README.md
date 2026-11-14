# CampusFlow API

The backend for **[CampusFlow](https://github.com/Muhammad-Zaheeb/campusflow-frontend)**, a task manager for students. A REST API built with **FastAPI**, **SQLAlchemy** and **PostgreSQL**, with JWT authentication.

**[Live app](https://campusflow-frontend-blond.vercel.app)** · **[Interactive API docs](https://campusflow-uoi7.onrender.com/docs)** · **[Frontend repo](https://github.com/Muhammad-Zaheeb/campusflow-frontend)**

![Python](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?logo=fastapi&logoColor=white)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy_2.0-D71F00?logo=sqlalchemy&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1?logo=postgresql&logoColor=white)
![JWT](https://img.shields.io/badge/JWT-000000?logo=jsonwebtokens&logoColor=white)

![CampusFlow dashboard](https://raw.githubusercontent.com/Muhammad-Zaheeb/campusflow-frontend/main/screenshots/dashboard-light.png)

> Hosted on Render's free tier: the first request after a quiet period can take 30–60 seconds while the server wakes up.

---

## Features

- **Authentication:** register and log in; passwords hashed with bcrypt; JWT access tokens
- **Per-user data:** every task query is scoped to the logged-in user, so users can never read or change each other's tasks
- **Task management:** create, update, delete and toggle tasks, with priority (Low / Medium / High) and an optional due date
- **Partial updates:** `PUT /tasks/{id}` only changes the fields you send, and `"due_date": null` clears a due date
- **Input validation with Pydantic:**
  - valid email format, a name, and a password of 8–72 characters
  - non-blank task titles; priority limited to Low, Medium or High
  - emails trimmed and compared case-insensitively
- **Safe error messages:** login returns the same error for an unknown email and a wrong password, so the form can't be used to find registered accounts
- **Auto-generated docs:** Swagger UI at `/docs`, ReDoc at `/redoc`

## API endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| `GET` | `/` | – | Health check |
| `POST` | `/register` | – | Create an account (`name`, `email`, `password`) |
| `POST` | `/login` | – | Log in and receive an access token |
| `GET` | `/me` | ✅ | The logged-in user's profile |
| `GET` | `/tasks` | ✅ | List your tasks (newest first) |
| `POST` | `/tasks` | ✅ | Create a task |
| `PUT` | `/tasks/{id}` | ✅ | Update any fields of a task |
| `PATCH` | `/tasks/{id}/toggle` | ✅ | Mark a task done / not done |
| `DELETE` | `/tasks/{id}` | ✅ | Delete a task |

Authenticated endpoints expect an `Authorization: Bearer <token>` header.

<details>
<summary>Example: log in and create a task</summary>

```bash
# Log in
curl -X POST http://localhost:8000/login \
  -H "Content-Type: application/json" \
  -d '{"email": "you@example.com", "password": "your-password"}'
# → {"message": "Login successful", "access_token": "eyJ...", "token_type": "bearer"}

# Create a task
curl -X POST http://localhost:8000/tasks \
  -H "Authorization: Bearer eyJ..." \
  -H "Content-Type: application/json" \
  -d '{"title": "Database quiz prep", "priority": "High", "due_date": "2026-11-20"}'
```
</details>

## Project structure

```
app/
├── auth/          # Password hashing, JWT creation, current-user dependency
├── core/          # Settings loaded from environment variables
├── database/      # SQLAlchemy engine and session
├── models/        # Database tables: User, Task
├── routers/       # Endpoints: home, user (auth), task
├── schemas/       # Pydantic request validation
└── main.py        # App setup, CORS and routes
```

## Run it locally

You need Python 3.10+ and a PostgreSQL database (a free [Neon](https://neon.tech) database works, or local Postgres).

```bash
git clone https://github.com/Muhammad-Zaheeb/campusflow.git
cd campusflow

python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt

cp .env.example .env            # then fill in DATABASE_URL and SECRET_KEY
uvicorn app.main:app --reload
```

The API runs on http://localhost:8000, with interactive docs at http://localhost:8000/docs. Tables are created automatically on first start.

### Environment variables

| Variable | Description |
|---|---|
| `DATABASE_URL` | PostgreSQL connection string |
| `SECRET_KEY` | Secret used to sign tokens (keep it private) |
| `ALGORITHM` | JWT signing algorithm, e.g. `HS256` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | How long a login lasts (default 30) |

## Deployment

- **API:** Render web service (entry point: `wsgi.py`)
- **Database:** PostgreSQL on Neon
- **Frontend:** Vercel. The allowed frontend origins are listed in `app/main.py` (CORS).

## Roadmap

- Automated tests (pytest) and CI with GitHub Actions
- Docker and docker-compose for the full stack
- Database migrations with Alembic
- Email verification and password reset
- Rate limiting on login

## Author

**Muhammad Zaheeb**, BSCS student at FAST-NUCES
[GitHub](https://github.com/Muhammad-Zaheeb) · [LinkedIn](https://www.linkedin.com/in/zaheeb-qureshi-22814b190/)
