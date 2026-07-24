# Deployment

## Local production-like run

```bash
docker compose up --build
```

The compose stack starts PostgreSQL, the FastAPI API, and the Vite frontend.

## Required production changes

- Set a strong `SECRET_KEY`
- Use managed PostgreSQL or a persistent Docker volume
- Run `alembic upgrade head` during release
- Serve the frontend behind HTTPS
- Restrict CORS origins to the deployed frontend domain
- Add object storage before supporting user uploads
