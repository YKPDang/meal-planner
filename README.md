# Meal Planner

Fullstack meal planner with Vue 3 frontend, FastAPI backend, and SQLite persistence.

## How It Works

1. The frontend (Vue 3 + Vuetify) loads recipes, tags, and the current week plan from the FastAPI backend.
2. Recipes include a name, description, ingredients, and tags. Ingredients are stored as unit + item pairs.
3. The weekly meal plan stores one recipe per day (or none). You can assign a recipe manually or use randomization.
4. Randomization modes:
   - `random`: any recipe.
   - `smart`: avoids recipes used in the last N days (lookback).
   - `filtered`: only recipes matching selected tags.
5. The backend persists everything in SQLite; the frontend talks to `/api/*` endpoints via proxy in dev or Compose.

## Run with Docker Compose

```bash
export GHCR_OWNER=<owner>
docker compose up
```

- Frontend: http://localhost:5173
- Backend API docs (via frontend proxy): http://localhost:5173/api/docs
- Docker Compose publishes only the frontend port (`5173`). The frontend proxies `/api/*` to the backend container internally.

If `GHCR_OWNER` is not set, Compose defaults image names to `ghcr.io/<owner>/...`; set it to your GitHub org/user that publishes the images.

## Test

Backend unit tests:

```bash
pip install -r backend/requirements.txt
pytest backend/tests
```

Frontend unit tests:

```bash
cd frontend
pnpm install
pnpm run test
```

## Local Development (No Docker)

Backend:

```bash
cd backend
python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload
```

Frontend:

```bash
cd frontend
set VITE_API_URL=http://localhost:8000/api
pnpm run dev
```

## CI/CD

- Pull requests run backend and frontend unit tests.
- Pushes to `main` run tests and then build + push backend/frontend Docker images to GitHub Container Registry (GHCR).
- Images are pushed as:
  - `ghcr.io/<owner>/meal-planner-backend:latest`
  - `ghcr.io/<owner>/meal-planner-frontend:latest`
- Repository owner is normalized to lowercase in the workflow so mixed-case GitHub usernames/org names work correctly for GHCR image naming.

## Project Structure

- `frontend/`: Vue 3 (Composition API) app with weekly calendar planner.
- `backend/`: FastAPI app with SQLite schema + randomization logic.
- `docker-compose.yml`: container orchestration and persistent DB volume.
- `.github/workflows/ci.yml`: CI pipeline for tests and GHCR image build/push.
