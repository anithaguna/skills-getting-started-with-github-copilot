<!-- Copilot instructions for agents working on this repo -->
# Project overview

This repository is a minimal FastAPI single-process app that serves a small in-memory
dataset of extracurricular activities and a static frontend. Key characteristics:

- API implemented in `src/app.py` (FastAPI app instance named `app`).
- Static frontend assets live in `src/static/` and are mounted at `/static`.
- Dependencies are listed in `requirements.txt` (`fastapi`, `uvicorn`).
- Tests: none included, but `pytest.ini` sets `pythonpath = .`.

# Big picture / architecture

- Single FastAPI app (no separate backend service). The app mounts `src/static/` and
  returns HTML at `/` via a redirect to `/static/index.html`.
- Data is stored in-process in the `activities` dict inside `src/app.py` (in-memory).
  This means state is ephemeral and shared across requests in the same process.

# Quick start (how to run locally)

1. Create and activate a virtual environment.
2. Install dependencies and run Uvicorn with reload for development:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m uvicorn src.app:app --reload --host 0.0.0.0 --port 8000
```

Open: http://127.0.0.1:8000/static/index.html

Example API call:

```bash
curl http://127.0.0.1:8000/activities
```

# Development patterns & conventions

- Add HTTP handlers directly in `src/app.py` using FastAPI decorators, e.g. `@app.get(...)`
  or `@app.post(...)` — follow existing function style (simple synchronous defs).
- Static assets should be placed under `src/static/` and referenced from `index.html`.
- To add dependencies, update `requirements.txt` and re-run `pip install -r requirements.txt`.

# Project-specific notes and gotchas

- In-memory state: `activities` is mutated in-place (lists appended on signups).
  Be mindful of concurrency and persistence requirements; this repo is intentionally
  minimal and not production-ready for concurrent writes.
- The app uses synchronous route functions but runs under Uvicorn; keep handlers
  simple to avoid blocking the event loop for long-running tasks.
- `pytest.ini` sets `pythonpath = .`, so tests (if added) can import `src.app` as `src.app`.

# Testing & debugging

- No tests currently included. To run tests after adding them:

```bash
pip install pytest
pytest
```

- For runtime debugging, run Uvicorn with `--reload`. Use logs from Uvicorn for errors.

# What an agent should do first when modifying code

1. Read `src/app.py` to understand current routes and the in-memory `activities` structure.
2. If adding new routes that mutate state, consider whether in-memory storage needs
   conversion to a simple file or DB (document this in the PR).
3. Update `requirements.txt` for new packages and include a short usage example in
   the PR description (how to run locally with the new code).

# Files to inspect for common tasks

- `src/app.py` — API and entrypoint
- `src/static/index.html` — frontend entry
- `src/static/app.js` — frontend behavior
- `requirements.txt` — runtime deps
- `pytest.ini` — test config

# If something is unclear

Ask for a short description of the intended feature or the desired change. If the change
affects persistent state or concurrency, propose a minimal reproducible approach and
preferred storage (file, sqlite, etc.) and include a short migration plan.

---
Please review this guidance and tell me if you'd like more detail on running, testing,
or on converting the in-memory store to a persistent backend.
