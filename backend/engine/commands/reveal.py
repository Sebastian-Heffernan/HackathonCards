from errors.BuildError import BuildError
from backend.engine.classesOld.deck import Deck
from backend.engine.classesOld.instruction import Instruction
from backend.engine.classesOld.states import *
from engine.engine import GameEngine

# REVEAL [PLAYER]
def execute(instruction: Instruction, engine: GameEngine):
    if len(instruction.args) != 1:
        raise BuildError("REVEAL [PLAYER] (Usage)")

    try:
        player_index = engine.gameState.resolve_variable(instruction.args[0])
    except (ValueError, TypeError):
        raise BuildError(f"REVEAL: Player index must be an integer. Got: {instruction.args[0]}")
    if not (0 <= player_index < len(engine.playerStates)):
        raise BuildError(f"REVEAL: Player index {player_index} is out of bounds.")

    player : PlayerState = engine.playerStates[player_index]

    if not player.hand:
        return True

    ### add lastmode card to revealed
    engine.gameState.global_revealed[player_index][-1] = True
