from backend.BuildError import BuildError
from backend.engine.classes.instruction import Instruction
from backend.engine.engine import GameEngine

# DRAW [Deck Name][Player ID][Number]
def execute(instruction : Instruction, engine: GameEngine):
    if len(instruction.args) < 2:
        raise BuildError("DRAW requires 3 arguments")
    deck_name = instruction.args[0]
    player_id = engine.gameState.resolve_variable(instruction.args[1])
    count = engine.gameState.resolve_variable(instruction.args[2])
    target_deck = engine.get_deck(deck_name)
    # check that deck exits
    if not target_deck:
        raise BuildError(f"Deck '{deck_name}' not found.")