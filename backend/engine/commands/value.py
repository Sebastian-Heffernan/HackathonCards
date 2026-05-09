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
    player_idx = engine.gameState.resolve_variable(instruction.args[PLAYER_IDX])
    card_idx = engine.gameState.resolve_variable(instruction.args[CARD_IDX])

    if player_idx >= len(engine.playerStates) or card_idx >= len(
        engine.playerStates[player_idx].hand
    ):
        raise BuildError("Player Index out of Bounds for player states")

    var_value = engine.playerStates[player_idx].hand[card_idx].value
    engine.gameState.variables[var_name] = var_value  # set the value
