import random
import string
from uuid import uuid4

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from pydantic import BaseModel

from backend.compiler.compiler import Compiler
from backend.compiler.compiler import CompilationError
from backend.db.cache import games, lobby_codes, rules_store
from backend.engine.engine import *
from backend.engine.engine import GameEngine
from backend.routers import lobby
from backend.routers.processors.client_side import ClientSideGenerator

app = FastAPI()
command_list = GameEngine.load_commands()


# app.include_router(lobby.router)


class CreateLobby(BaseModel):
    rule_id: str
    host_name: str


class JoinLobby(BaseModel):
    name: str


class GetRules(BaseModel):
    source: str


def create_code():
    code = ""

    for i in range(5):
        code += random.choice("ABCDEFGHIJKLMNOPQRSTUVWQYZ1234567890")

    if code not in lobby_codes:
        return code
    else:
        return create_code()


@app.get("/")
def root():
    return {"message": "Backend is running"}

# send lobby data to client
@app.get("/api/lobbies")
def get_lobbies():
    summary = []

    for lobby_code, game_id in lobby_codes.items():
        game_data = games.get(game_id)

        if game_data and not game_data.get("started", False):
            summary.append({
                "id": lobby_code,
                "name": lobby_code,
                "playerCount": len(game_data.get("players", {})),
                "started": game_data.get("started", False),
            })

    return {
        "ok": True,
        "lobbies": summary
    }

# recieve the rules from the client
@app.post("/api/rules")
def get_rules(rules: GetRules):
    source = rules.source
    try:
        compiled_rules = Compiler.compile(source, command_list)
    except CompilationError as error:
        return {
            "ok": False,
            "error": str(error)
        }
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
        "players": {host_id: {"name": request.host_name}},
        "engine": GameEngine(rules_store[request.rule_id], command_list),
    }

    code = create_code()
    lobby_codes[code] = game_id

    return {"ok": True, "gameId": game_id, "lobbyCode": code, "playerId": host_id}


# player joins lobby
# make sure to open websocket on client if joined and then use the websocket to tell server we joined
@app.post("/api/lobbies/{lobby_code}/join")
def join_lobby(lobby_code: str, request: JoinLobby):
    player_id = str(uuid4())
    # add player to game
    game_id = lobby_codes[lobby_code]
    games[game_id]["players"][player_id] = {"name": request.name}

    return {
        "ok": True,
        "gameId": game_id,
        "lobbyCode": lobby_code,
        "playerId": player_id,
    }


def client_side_to_dict(client_side):
    if hasattr(client_side, "model_dump"):
        return client_side.model_dump()
    if hasattr(client_side, "dict"):
        return client_side.dict()
    return vars(client_side)


def get_client_side_for_player(game, player_id):
    engine = game["engine"]
    client_sides = ClientSideGenerator.generate_client_sides(engine)

    for idx, player_state in enumerate(engine.playerStates):
        if player_state.uuid == player_id:
            client_side = client_side_to_dict(client_sides[idx])
            opponent_names = []
            for other_player_state in engine.playerStates:
                if other_player_state.uuid == player_id:
                    continue
                opponent_name = game["players"][other_player_state.uuid]["name"]
                opponent_names.append(opponent_name)
            client_side["opponent_names"] = opponent_names
            return client_side

    return None

def get_visible_game_vars(engine):
    visible_vars = {}
    for var_name in engine.gameState.showVars:
        visible_vars[var_name] = engine.gameState.variables.get(var_name)
    return visible_vars

def get_player_names(game):
    names = []
    for player_state in game["engine"].playerStates:
        player_id = player_state.uuid
        names.append(game["players"].get(player_id, {}).get("name", "Unknown"))
    return names

def remove_lobby_code_for_game(game_id: str):
    for lobby_code, stored_game_id in list(lobby_codes.items()):
        if stored_game_id == game_id:
            lobby_codes.pop(lobby_code, None)

async def broadcast_lobby_players(game_id: str):
    if game_id not in games:
        return
    message = {
        "type": "UPDATE_PLAYERS",
        "players": games[game_id]["players"]
    }
    for player_socket in list(games[game_id]["connections"].values()):
        try:
            await player_socket.send_json(message)
        except Exception:
            pass

async def close_game_for_everyone(game_id: str):
    if game_id not in games:
        return
    game = games[game_id]
    for player_socket in list(game["connections"].values()):
        try:
            await player_socket.send_json({
                "type": "GO_HOME"
            })
        except Exception:
            pass

        try:
            await player_socket.close()
        except Exception:
            pass
    remove_lobby_code_for_game(game_id)
    games.pop(game_id, None)

# socket for game
@app.websocket("/ws/{game_id}/{player_id}")
async def websocket_endpoint(websocket: WebSocket, game_id: str, player_id: str):
    await websocket.accept()
    # save the connected players
    games[game_id]["connections"][player_id] = websocket

    try: 
        while True:
            # recieve the players action
            action = await websocket.receive_json()

            # first if the game isn't started,
            if not games[game_id]["started"]:
                # see if the player is host and action is start game
                if player_id == games[game_id]["hostId"] and action["type"] == "START_GAME":
                    game = games[game_id]

                    try:
                        # reset engine so repeated failed starts do not duplicate players
                        game["engine"] = GameEngine(game["rules"], command_list)

                        for connected_player_id in game["connections"].keys():
                            game["engine"].add_player(connected_player_id)

                        game["engine"].run_script("SETUP")

                    except BuildError as error:
                        message = str(error) or "Setup failed. Check player count or player indexes."

                        for player_socket in game["connections"].values():
                            await player_socket.send_json({
                                "type": "LOBBY_ERROR",
                                "message": message
                            })

                        continue

                    game["started"] = True
                    for lobby_code, stored_game_id in list(lobby_codes.items()):
                            if stored_game_id == game_id:
                                lobby_codes.pop(lobby_code, None)

                    for connected_player_id, player_socket in game["connections"].items():
                        await player_socket.send_json({
                            "type": "START_GAME",
                            "players": game["players"],
                            "playerState": get_client_side_for_player(
                                game,
                                connected_player_id
                            ),
                            "gameVars": get_visible_game_vars(game["engine"]),
                            "playerNames": get_player_names(game),
                        })
                # if a new player joins, send the playerlist to the client if not started
                elif action["type"] == "JOIN_GAME":
                    for player_socket in games[game_id]["connections"].values():
                        await player_socket.send_json(
                            {"type": "UPDATE_PLAYERS", "players": games[game_id]["players"]}
                        )
            else:
                if action["type"] == "START_GAME":
                    continue

                if action["type"] == "GO_HOME":
                    for player_socket in games[game_id]["connections"].values():
                        await player_socket.send_json({
                            "type": "GO_HOME"
                        })
                    for lobby_code, stored_game_id in list(lobby_codes.items()):
                            if stored_game_id == game_id:
                                lobby_codes.pop(lobby_code, None)
                    games.pop(game_id, None)
                    continue

                # remake game storage logic
                if action["type"] == "RESTART_GAME":
                    #old_engine = games[game_id]["engine"]
                    games[game_id]["engine"] = GameEngine(
                        games[game_id]["rules"],
                        #old_engine.commandList
                        command_list
                    )
                    for connected_player_id in games[game_id]["connections"].keys():
                        games[game_id]["engine"].add_player(connected_player_id)
                    games[game_id]["engine"].run_script("SETUP")
                    for connected_player_id, player_socket in games[game_id]["connections"].items():
                        await player_socket.send_json({
                            "type": "START_GAME",
                            "players": games[game_id]["players"],
                            "playerState": get_client_side_for_player(
                                games[game_id],
                                connected_player_id
                            ),
                            "gameVars": get_visible_game_vars(games[game_id]["engine"]),
                            "playerNames": get_player_names(games[game_id]),
                        })
                    continue
                # ======= game loop =======
                # run the action through engine, should take the rules and the players action
                if player_id == games[game_id]["engine"].get_current_player_uuid():
                    # get state and build player specific state to send to each player
                    # check if valid in near future
                    games[game_id]["engine"].gameState.variables["$selectedCardId"] = (
                        action["selectedCardId"]
                    )
                    games[game_id]["engine"].run_script(action["type"])
                    # send state to each player

                    for connected_player_id, player_socket in games[game_id][
                        "connections"
                    ].items():
                        await player_socket.send_json(
                            {
                                "type": "GAME_STATE",
                                "playerState": get_client_side_for_player(games[game_id], connected_player_id),
                                "gameVars": get_visible_game_vars(games[game_id]["engine"]),
                                "playerNames": get_player_names(games[game_id]),
                            }
                        )

    except WebSocketDisconnect:
        if game_id not in games:
            return
        if player_id == games[game_id]["hostId"]:
            await close_game_for_everyone(game_id)
            return
        games[game_id]["connections"].pop(player_id, None)
        if not games[game_id]["started"]:
            games[game_id]["players"].pop(player_id, None)
            await broadcast_lobby_players(game_id)