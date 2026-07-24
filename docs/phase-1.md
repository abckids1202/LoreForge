# Phase 1 Completion Notes

## Phase objective

Create the stable full-stack base for LoreForge: repository setup, FastAPI backend, SQLAlchemy database configuration, Alembic migration, authentication, ownership checks, world CRUD, frontend shell, login/register pages, dashboard, and world dashboard.

## Files created

See the repository root for backend, frontend, docs, Docker, and environment files.

## Database migrations

The initial migration is `backend/alembic/versions/0001_initial.py`. It creates users, worlds, lore-entry foundation tables, relationships, tags, notes, contradictions, and audit logs.

## Setup commands

```bash
npm install
cd backend
pip install -r requirements.txt
alembic upgrade head
python -m app.seed
uvicorn app.main:app --reload
```

In another terminal:

```bash
cd frontend
npm run dev
```

## Environment variables

Copy `.env.example` to `.env` and update `SECRET_KEY` before using a deployed environment.

## Expected UI behavior

Users can register, sign in, create private worlds, browse their world library, and open a world dashboard. The dashboard shows Phase 1 statistics from the database and uses seeded demo lore when `python -m app.seed` has been run.

## Common errors

- `401 Authentication required`: sign in again or clear the stored browser token.
- Empty dashboard: run `python -m app.seed` or create a new world.
- PostgreSQL connection refused: start Docker Compose or use the SQLite default.

## Completion checklist

- Backend API starts
- Register/login works
- World CRUD works
- Owner isolation enforced
- World dashboard returns stats
- Frontend build passes
- Backend tests pass

## Next phase

Phase 2 adds generic lore entry CRUD, Markdown editing, tags, filters, search, and entry detail pages.
