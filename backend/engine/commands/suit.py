from backend.BuildError import BuildError
from backend.engine.classes.deck import *
from backend.engine.classes.instruction import Instruction
from backend.engine.classes.states import *
from backend.engine.engine import GameEngine


# SUIT [VAR][PlayerID][CardID]
def execute(instruction: Instruction, engine: GameEngine):
    if len(instruction.args != 3):
        raise BuildError()

    var = instruction.args[0]
    player_id = engine.gameState.resolve_variable(instruction.args[1])
    card_id = engine.gameState.resolve_variable(instruction.args[2])

    if player_id >= len(engine.playerStates) or card_id >= len(
        engine.playerStates[player_id].hand
    ):
        raise BuildError()

    suit_value = engine.playerStates[player_id].hand[card_id].suit
    engine.gameState.variables[var] = suit_value  # set value in ram

