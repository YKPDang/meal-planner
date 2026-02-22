# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Build & Run Commands

### Docker Compose (full stack)

```bash
docker compose up
# Frontend: http://localhost:5173
# API docs: http://localhost:5173/api/docs
```

### Local Development (no Docker)

```bash
# Backend (from repo root)
cd backend
pip install -r requirements.txt
python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload

# Frontend (from repo root)
cd frontend
pnpm install
set VITE_API_URL=http://localhost:8000/api   # Windows
pnpm run dev
```

### Tests

```bash
# Backend tests
pytest backend/tests

# Single backend test
pytest backend/tests/test_api.py::test_name

# Frontend tests
cd frontend && pnpm run test
```

### Build frontend

```bash
cd frontend && pnpm run build
```

## Architecture

Fullstack monorepo: Vue 3 SPA frontend + FastAPI backend + SQLite database.

### Backend (`backend/`)

Layered architecture: **Routers → Services → Repositories → SQLite**

- `app/main.py` — FastAPI app factory, CORS middleware, mounts all routers under `/api` prefix
- `app/db.py` — SQLite connection management, schema initialization (raw SQL, no ORM)
- `app/config.py` — Environment variable configuration
- `app/schemas.py` — Pydantic request/response models
- `app/routers/` — Endpoint handlers (recipes, tags, meal_plan, health)
- `app/services/` — Business logic (meal plan randomization with 3 modes: random, smart, filtered)
- `app/repositories/` — Data access layer with raw SQL queries

Database connections are injected via FastAPI's `Depends()`. Schema is auto-created on app startup via lifespan context manager. Foreign keys enabled with `PRAGMA foreign_keys = ON`; cascade deletes on recipes → ingredients/recipe_tags.

### Frontend (`frontend/`)

Vue 3 Composition API + Vuetify + TypeScript, built with Vite.

- `src/app/App.vue` — Root component, holds application state (no Vuex/Pinia)
- `src/app/components/` — UI components (MealPlanBoard, RecipeForm, RecipeList, TagList)
- `src/app/composables/` — `useApi.ts` (fetch wrapper), `useMealPlan.ts` (meal plan logic)
- `src/app/utils/` — Date formatting, ingredient/tag parsing
- `src/app/types/` — TypeScript type definitions
- Path alias: `@` → `./src`

### API Proxy

In Docker Compose, only port 5173 (frontend) is published. Vite proxies `/api/*` to the backend container. In local dev, set `VITE_API_URL` to point directly at the backend.

## Environment Variables

| Variable                     | Where    | Default                 | Purpose                                   |
| ---------------------------- | -------- | ----------------------- | ----------------------------------------- |
| `DATABASE_PATH`              | Backend  | `/data/meal_planner.db` | SQLite file path                          |
| `SMART_RANDOM_LOOKBACK_DAYS` | Backend  | `7`                     | Days to look back for smart randomization |
| `CORS_ORIGINS`               | Backend  | `*`                     | Comma-separated allowed origins           |
| `VITE_API_URL`               | Frontend | `/api`                  | API base URL                              |
