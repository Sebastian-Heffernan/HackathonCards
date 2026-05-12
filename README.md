# Cardssembly

UQ Game Jam 2026 Hackathon project

Cardssembly is a multiplayer platform, which connects players to new card games through custom byte-code (*Cardssembly*)
To Get Started as a Player:
You can go to the base url, and join a lobby
The player will read the *Cardssembly* byte-code of the lobby
All of the players will play following the new byte-code

To Get Started as a Host: 
A host can press the *plus* icon on base url, and see a modal
On the modal, the user will copy and paste their code and the server will parse it
From there, the host will wait for the players to join
If theres enough players, the game will start with the players and host

## Styling / Assets

- **CSS:** NES.css framework
- **Playing Cards:** <https://opengameart.org/content/playing-cards-pack>

## Build Instructions

### Backend

#### Create and activate a virtual environment:
##### MACOS
```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
```

##### WINDOWS
```bash
cd backend
python3 -m venv .venv
source .\.venv\Scripts\Activate
```

Install Python dependencies:

```bash
cd backend
python -m pip install -r requirements.txt
```

Run the backend:

```bash
cd backend
uvicorn main:app --reload
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
