# Architecture

LoreForge is a full-stack monorepo.

The backend keeps routers thin and places business logic in services. Reusable dependencies handle authentication and ownership checks. SQLAlchemy models define the persistent structure and Alembic tracks migrations.

The frontend is a Vite React application with strict TypeScript. Zustand stores the auth token, TanStack Query handles API state, and React Router separates public auth pages from protected app pages.

Phase 1 intentionally exposes only authentication and world management, while the schema is ready for lore entries, relationships, contradictions, notes, tags, and audit logs.
