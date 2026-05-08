from uuid import uuid4

from fastapi import FastAPI, WebSocket
from pydantic import BaseModel

import backend.engine
import backend.compiler

app = FastAPI()

# the objects storing the different rules and games
games = {}
rules_store = {}


class CreateLobby(BaseModel):
    rule_id: str
    host_name: str


class JoinLobby(BaseModel):
    name: str


class GetRules(BaseModel):
    source: str


@app.get("/")
def root():
    return {"message": "Backend is running"}

# recieve the rules from the client
@app.post("/api/rules")
def get_rules(rules: GetRules):
    source = rules.source
    # pass them to the json compiler
    compiled_rules = backend.compiler.compile(source)
    # store in dict to reference when game starts
    rule_id = str(uuid4())
    rules_store[rule_id] = compiled_rules

    return {
        "ok": True,
        "ruleId": rule_id
    }

# player starts the game lobby
@app.post("/api/lobbies")
def start_game(request: CreateLobby):
    game_id = str(uuid4())
    host_id = str(uuid4())
    games[game_id] = {
        "rules": rules_store[request.rule_id],
        "started": False,
        "hostId": host_id,
        "connections": {},
        "players": {
            host_id : {"name": request.host_name}
        },
        "state": {

        }
    }

    return {
        "ok": True,
        "gameId": game_id,
        "playerId": host_id
    }

# player joins lobby
# make sure to open websocket on client if joined and then use the websocket to tell server we joined
@app.post("/api/lobbies/{game_id}/join")
def join_lobby(game_id: str, request: JoinLobby):
    player_id = str(uuid4())
    # add player to game
    games[game_id]["players"][player_id] = {"name": request.name}

    return {
        "ok": True,
        "gameId": game_id,
        "playerId": player_id
    }

# socket for game
@app.websocket("/ws/{game_id}/{player_id}")
async def websocket_endpoint(websocket: WebSocket, game_id: str, player_id: str):
    await websocket.accept()
    # save the connected players
    games[game_id]["connections"][player_id] = websocket

    while True:
        # recieve the players action
        action = await websocket.receive_json()

        # first if the game isn't started, 
        if (not games[game_id]["started"]):
            # see if the player is host and action is start game
            if (player_id == games[game_id]["hostId"] and action["type"] == "START_GAME"):
                games[game_id]["started"] = True
                for player_socket in games[game_id]["connections"].values():
                    await player_socket.send_json({
                        # what to send to every client to start game?
                        "type": "START_GAME",
                        "players": games[game_id]["players"],
                        "state": games[game_id]["state"]
                    })
            # if a new player joins, send the playerlist to the client if not started
            elif (action["type"] == "JOIN_GAME"):
                for player_socket in games[game_id]["connections"].values():
                    await player_socket.send_json({
                        "type": "UPDATE_PLAYERS",
                        "players": games[game_id]["players"]
                    })
        else:
            pass
            # ======= game loop =======
            # run the action through engine, should take the rules and the players action
            backend.engine.run_command(games[game_id]["rules"], action["type"])

            # get state and build player specific state to send to each player

            # send state to each player
