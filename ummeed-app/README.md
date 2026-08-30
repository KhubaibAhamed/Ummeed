# Ummeed

Multilingual, RAG-grounded farmer advisory assistant. See `/docs` conversation history
(product-forge phases 1-6) for full PRD/TRD/architecture — this file just covers running it.

## Backend (FastAPI)

```
cd backend
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
cp .env.example .env        # then fill in real API keys
.venv/bin/uvicorn app.main:app --reload
```
Runs at http://localhost:8000 — check http://localhost:8000/health

Tests: `.venv/bin/pytest -v`
Lint: `.venv/bin/ruff check .`

## Frontend (React + Vite)

```
cd frontend
npm install
cp .env.example .env
npm run dev
```
Runs at http://localhost:5173

Tests: `npm test`
Lint: `npm run lint`
Build: `npm run build`

## Termux-specific notes (mobile dev)

- Termux ships Python 3.12+ and Node via `pkg install python nodejs`.
- `python3 -m venv .venv` works the same in Termux as any Linux environment.
- If `pip install` hits a build-from-source wall on a package with C extensions, add
  `--only-binary=:all:` or install `clang`/`make` via `pkg install clang make`.
- Push to GitHub from Termux with the normal `git` CLI (`pkg install git` if not present) —
  Vercel/Render both auto-deploy on push once connected to the repo.

## Deployment

- Frontend → Vercel, connect the repo, root directory `frontend/`, build command `npm run build`.
- Backend → Render, connect the repo, root directory `backend/`, start command
  `uvicorn app.main:app --host 0.0.0.0 --port $PORT`.
- Set all `.env` keys in each platform's dashboard — never commit `.env` itself.
