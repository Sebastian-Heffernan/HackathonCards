# Styling / Assets
CSS: NES.css framework
Playing Cards: https://opengameart.org/content/playing-cards-pack

# HackathonCards
UQ gamejam hackathon project

# Build Instructions
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt

run the backend:
uvicorn backend.main:app --reload
run the frontend:
cd frontend
npm run dev