from backend import BuildError
from backend.engine.classes.instruction import Instruction
from backend.engine.classes.states import *
from backend.engine.engine import GameEngine

"""
HANDLEN:
    Stores hand length of player, 'p' in VAR
"""

VAR_NAME = 0
PLAYER_IDX = 1


# VALUE [VAR][p: int][c: int]
def execute(instruction: Instruction, engine: GameEngine):
    if len(instruction.args) != 3:
        raise BuildError("VALUE requires 3 args")

    var_name = instruction.args[VAR_NAME]
    player_idx = instruction.args[PLAYER_IDX]

    if player_idx >= len(engine.playerStates):
        raise BuildError("Player Index out of Bounds for player states")

    engine.gameState.variables[var_name] = len(
        engine.playerStates[player_idx].hand
    )  # set the value
