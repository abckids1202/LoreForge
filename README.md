# LoreForge

## Overview

LoreForge is a private worldbuilding and lore-management platform for writers, tabletop game masters, comic creators, game developers, and anyone building a large fictional universe.

Tagline: **Build worlds, connect lore, and keep your universe consistent.**

This first implementation completes Phase 1: repository setup, FastAPI backend foundation, database configuration, authentication, ownership checks, world CRUD, frontend shell, login/register pages, main dashboard, and world dashboard.

## Problem

Large fictional universes quickly become hard to keep consistent. Characters, factions, locations, timelines, secret canon, and contradictions tend to sprawl across documents and disconnected notes.

## Solution

LoreForge starts as a structured world workspace. Users can register, log in, create private worlds, track genre/tone/themes/premise, and inspect dashboard statistics. The codebase is designed for the later lore-entry, relationship, timeline, graph, export, and AI-assistance phases.

## Key Features

- Secure register/login flow with hashed passwords and bearer tokens
- Ownership-ready API dependencies
- World CRUD with private-by-default visibility
- Polished demo world: **The Ashen Meridian**
- World dashboard with entry, relationship, contradiction, draft, and recent activity statistics
- Responsive React UI with authenticated routes
- SQLAlchemy models and Alembic migration scaffolding
- Docker Compose with PostgreSQL, API, and frontend services
- Backend tests for auth, world ownership, dashboard, and validation

## Technology Stack

- Frontend: Vite, React, TypeScript, React Router, TanStack Query, Zustand, Recharts, Tailwind CSS, lucide-react
- Backend: FastAPI, SQLAlchemy 2.0, Pydantic, Alembic, passlib, python-jose
- Database: PostgreSQL in Docker, SQLite-friendly local/test default
- Testing: Pytest and FastAPI TestClient

## Architecture

```text
frontend/        React app, API client, auth store, pages, components
backend/         FastAPI app, routers, schemas, models, services, policies
backend/alembic/ Database migrations
docs/            Product, architecture, database, roadmap, deployment notes
```

## Database Design

Phase 1 includes `users`, `worlds`, `lore_entries`, `relationships`, `tags`, `entry_tags`, `notes`, `contradictions`, and `audit_logs` tables. Later phases add specialized profile tables for characters, factions, locations, events, and artifacts.

## Entity and Relationship System

The schema already centers on a shared `lore_entries` table and first-class `relationships`. Phase 1 seeds relationship-ready demo data so the dashboard can show the eventual operating model.

## Timeline System

The timeline is planned for Phase 5. Phase 1 includes the world and lore-entry structure needed for event entries and year-based chronology.

## Graph System

The relationship graph is planned for Phase 5. Relationship records are already modeled with source, target, type, strength, status, visibility, and directionality.

## Canon and Visibility

Worlds and entries are private by default. Entry status values include `DRAFT`, `CANON`, `RUMOR`, `UNCONFIRMED`, `CONTRADICTED`, and `ARCHIVED`. Visibility values include `PRIVATE`, `SPOILER`, `DM_ONLY`, `SHARED`, and `PUBLIC_READY`.

## Installation

```bash
npm install
```

Backend:

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
alembic upgrade head
python -m app.seed
uvicorn app.main:app --reload
```

Frontend:

```bash
cd frontend
npm run dev
```

## Environment Variables

See `.env.example`.

## Database Migrations

Alembic is configured in `backend/alembic.ini`. The initial migration creates the Phase 1 schema.

```bash
cd backend
alembic upgrade head
```

## Seed Demo World

```bash
cd backend
python -m app.seed
```

Demo user:

- Email: `demo@loreforge.local`
- Password: `DemoPass123!`

## Testing

```bash
cd backend
python -m pytest tests
```

Frontend typecheck:

```bash
npm run build
```

## Deployment

Use Docker Compose for local production-like services:

```bash
docker compose up --build
```

## Screenshots

Add screenshots after launching the local app and capturing the login page, dashboard, and world dashboard.

## Limitations

- The MVP does not include real-time collaboration.
- The timeline uses simplified year-based chronology in the planned phases.
- Map creation is not included.
- AI suggestions may be inaccurate.
- AI does not automatically become canon.
- Large graphs may need filtering.
- Public publishing is not implemented.
- File storage is local in development.
- Advanced calendar systems are deferred.

## Roadmap

Phase 2 adds lore entries, Markdown editing, tags, filters, and entry detail pages. Later phases add structured profiles, relationships, timeline, graph, contradictions, exports, and optional AI assistance.
