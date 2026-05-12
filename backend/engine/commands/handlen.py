from errors.BuildError import BuildError
from engine.classes.deck import Deck
from engine.classes.instruction import Instruction
from engine.classes.states import *
from engine.engine import GameEngine

VAR_NAME = 0
PLAYER_IDX = 1


# HANDLEN [VAR_NAME] [PLAYER_IDX]
def execute(instruction: Instruction, engine: GameEngine):
    if len(instruction.args) != 2:
        raise BuildError("HANDLEN requires 2 args")

    var_name = instruction.args[VAR_NAME]
    player_idx = engine.gameState.resolve_variable(instruction.args[PLAYER_IDX])

    if player_idx < 0 or player_idx >= len(engine.playerStates):
        raise BuildError("Player index out of bounds for HANDLEN")

    engine.gameState.variables[var_name] = len(
        engine.playerStates[player_idx].hand
    )