# RoamReady

RoamReady is a two-part local travel application for IST 402. The Vue frontend searches hotel stays and manages reservation history through a typed FastAPI API. Hotel and trip search data remains in CSV files; traveler and booking records are seeded into SQLite for persistent CRUD operations.

## Project structure

```text
backend/app/        FastAPI routes, models, and data repository
backend/data/       CSV source data and generated travel.db
backend/tests/      API integration tests
frontend/src/       Vue 3 interface and styles
handoffs/current.md Design decisions and handoff status
submissions/        Separate Part 1 and Part 2 report.md files
```

The four files in `backend/data/` are the official fictional classroom dataset. Their text IDs and leading zeros are preserved, and the backend reads UTF-8 files with or without a byte-order mark.

## Run locally

Backend (Python 3.11 or newer):

```powershell
cd backend
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
uvicorn app.main:app --reload
```

Frontend (Node 22.18 or newer), in a second terminal:

```powershell
cd frontend
npm install
npm run dev
```

Open `http://localhost:5173`. The frontend uses `http://localhost:8000` by default; set `VITE_API_URL` to override it.

## Verify

```powershell
cd backend
pytest
cd ..\frontend
npm run build
npm run lint
```

Search is case-insensitive and accepts partial city or hotel names. New and edited bookings persist across server restarts in `backend/data/travel.db`. Delete that generated file to reseed all four tables from the official CSV files.
