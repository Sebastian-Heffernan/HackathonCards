### reveal
### specify which players card you are revealing, the card itself, and then also  and append it to global_revealed
### get the player who has their current turn from the game state, and then from there
### everyones card is revealed at the same time
###
### reveal lastmost (i - 1 card)
# REVEAL [PLAYER][card]

from backend.BuildError import BuildError
from backend.engine.classes.instruction import Instruction
from backend.engine.classes.states import *
from backend.engine.engine import GameEngine


# REVEAL [PLAYER]
def execute(instruction: Instruction, engine: GameEngine):
    if len(instruction.args) != 1:
        raise BuildError("REVEAL [PLAYER] (Usage)")

    try:
        player_index = int(instruction.args[0])
    except (ValueError, TypeError):
        raise BuildError(f"REVEAL: Player index must be an integer. Got: {instruction.args[0]}")
    if not (0 <= player_index < len(engine.playerStates)):
        raise BuildError(f"REVEAL: Player index {player_index} is out of bounds.")

    player : PlayerState = engine.playerStates[player_index]

    if not player.hand:
        return True

    ### add lastmode card to revealed
    engine.gameState.global_revealed[player_index][-1] = True
