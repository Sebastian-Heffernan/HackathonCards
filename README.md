# HackathonCards

UQ Game Jam hackathon project.

## Styling / Assets

- **CSS:** NES.css framework
- **Playing Cards:** <https://opengameart.org/content/playing-cards-pack>

## Build Instructions

### Backend

Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install Python dependencies:

```bash
python -m pip install -r requirements.txt
```

Run the backend:

```bash
uvicorn backend.main:app --reload
```

### Frontend

In a separate terminal:

```bash
cd frontend
npm install
npm run dev
```

## Local URLs

- Frontend: <http://localhost:5173>
- Backend: <http://localhost:8000>