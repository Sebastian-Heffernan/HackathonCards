from backend import BuildError
from backend.engine.classes.instruction import Instruction
from backend.engine.classes.states import *
from backend.engine.engine import GameEngine

"""
VALUE:
    Stores VALUE of the card of player, 'p', in the hand at 'c'
"""

VAR_NAME = 0
PLAYER_IDX = 1
CARD_IDX = 2


# VALUE [VAR][p: int][c: int]
def execute(instruction: Instruction, engine: GameEngine):
    if len(instruction.args) != 3:
        raise BuildError("VALUE requires 3 args")

    var_name = instruction.args[VAR_NAME]
    try:
        player_id = int(engine.gameState.resolve_variable(instruction.args[PLAYER_IDX]))
        card_id = int(engine.gameState.resolve_variable(instruction.args[CARD_IDX]))
    except (ValueError, TypeError):
        raise BuildError(f"VALUE: Player ID and Card ID must be integers. "
                         f"Got: {instruction.args[1]}, {instruction.args[2]}")

    if not (0 <= player_id < len(engine.playerStates)):
        raise BuildError(f"SUIT: Player index {player_id} out of range.")
    target_player = engine.playerStates[player_id]
    if not (0 <= card_id < len(target_player.hand)):
        raise BuildError(f"SUIT: Card index {card_id} out of range for Player {player_id}.")
    
    card_obj = target_player.hand[card_id]
    var_value = card_obj["value"]
    engine.gameState.variables[var_name] = var_value  # set the value
