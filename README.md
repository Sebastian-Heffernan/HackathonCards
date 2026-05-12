# Cardssembly - Card Game Engine
UQCS GameJam 2026 Hackathon project.

Cardssembly is a card game engine where you can program your own card games and play them with your friends! 
Hosts are able to program their own card games, and then host said game for players to join! All the players will play whatever the host has created.

## Screenshots
![Lobby Screen](thumbnails\AlphaLobbyScreen.png)
![Documentation](thumbnails\DocumentationV1.png)
![In-Game](thumbnails\GameV1.png)

## To Get Started as a Host:
- Open Up [this link](https://cardssembly-alpha-production.up.railway.app/) and either create or join a lobby.
![LobbyCreation](thumbnails\LobbyCreation.png)
- The lobby host can then create their game using our text and game description editor and create a lobby.
- On default, "Showdown" is the default game. Create your own game, or check out our [Documentation Page](https://cardssembly-alpha-production.up.railway.app/docs/overview) for game exemplars.

## To Get Started as a Player:
- Open Up [this link](https://cardssembly-alpha-production.up.railway.app/) and join a lobby from the code, or our public lobbies list.


## Styling / Assets
- **CSS:** NES.css Framework, Tailwind CSS
- **Playing Cards:** <https://opengameart.org/content/playing-cards-pack>
- **Font:** Press Start 2P

## Build Instructions
### Backend
#### 1. Create and activate a virtual environment:
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

#### 2. Install Python dependencies:

```bash
cd backend
python -m pip install -r requirements.txt
```

#### 3. Run the backend

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

# Future Plans
- Rework the Game Engine to be more robust
- Implement in Visualisation of Code Execution
- Implement in Custom Cards
- Implement in a more robust text editor.