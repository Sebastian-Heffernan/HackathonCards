from db.cache import games, lobby_codes, rules_store


def get_game(lobby_id: str):
    game_id = lobby_codes[lobby_id]
    game_info = games[game_id].copy()  # to allow modifying without intruding

    del game_info["engine"]
    return game_info
