from backend.errors.BuildError import BuildError
from backend.engine.classes.deck import *
from backend.engine.classes.instruction import Instruction
from backend.engine.classes.states import *
from backend.engine.engine import GameEngine


# SUIT [VAR][PlayerID][CardID]
def execute(instruction: Instruction, engine: GameEngine):
    if len(instruction.args != 3):
        raise BuildError("SUIT [VAR][PLAYER ID][CARD ID]")

    var = instruction.args[0]
    try:
        player_id = engine.gameState.resolve_variable(instruction.args[1])
        card_id = engine.gameState.resolve_variable(instruction.args[2])
    except (ValueError, TypeError):
        raise BuildError(f"SUIT: Player ID and Card ID must be integers. "
                         f"Got: {instruction.args[1]}, {instruction.args[2]}")
    
    if not (0 <= player_id < len(engine.playerStates)):
        raise BuildError(f"SUIT: Player index {player_id} out of range.")
    target_player = engine.playerStates[player_id]
    if not (0 <= card_id < len(target_player.hand)):
        raise BuildError(f"SUIT: Card index {card_id} out of range for Player {player_id}.")
    
    card_obj = target_player.hand[card_id]

    if hasattr(card_obj, 'suit'):
        suit_value = card_obj.suit
    elif isinstance(card_obj, dict) and 'suit' in card_obj:
        suit_value = card_obj['suit']
    else:
        # Fallback
        suit_value = "UNKNOWN"
    engine.gameState.variables[var] = suit_value  # set value in ram

