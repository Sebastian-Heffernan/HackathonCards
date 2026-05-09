from fastapi import APIRouter

from backend.db.cache import games, lobby_codes, rules_store

router = APIRouter()


@router.get("/lobbies")
async def get_lobbies():
    summary = []

    for lobby_id, game_id in lobby_codes.items():
        # Get the game object using the game_id
        game_data = games.get(game_id)
        print(lobby_id)

        if game_data:
            # Count the players in that specific game
            player_count = len(game_data.get("players", {}))

            # Create the formatted string
            summary.append(
                {
                    "lobby_id": lobby_id,
                    "lobby_info": f"Lobby {lobby_id} (Game: {game_id})",
                    "player_count": player_count,
                }
            )

    return summary


@router.websocket("/ws/{lobby_id}")
async def lobby_websocket():
    pass


@router.websocket("/ws/{lobby_id}/{player_id}")
async def player_spec_websocket():
    pass
