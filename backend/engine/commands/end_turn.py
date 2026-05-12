from errors.BuildError import BuildError
from backend.engine.classesOld.deck import Deck
from backend.engine.classesOld.instruction import Instruction
from backend.engine.classesOld.states import *
from engine.engine import GameEngine

# END_TURN [NEXT PLAYER INDEX | None]
def execute(instruction: Instruction, engine: GameEngine):
    if engine.debug:
        print("[ENDING TURN]")
    gameState: GameState = engine.gameState
    player_count = int(gameState.variables.get("$playerCount", 1))

    if len(instruction.args) == 0:
        return "break"
    elif len(instruction.args) == 1:
        val = engine.gameState.resolve_variable(instruction.args[0])
        gameState.variables["$turnPlayer"] = int(val) % player_count
    elif len(instruction.args) == 3:
        try:
            left = engine.gameState.resolve_variable(instruction.args[0])
            right = engine.gameState.resolve_variable(instruction.args[2])
            operator = instruction.args[1]
            if operator == "+":
                res = left + right
            elif operator == "-":
                res = left - right
            else:
                res = left # Fallback
            gameState.variables["$turnPlayer"] = res % player_count
        except (ValueError, TypeError):
                # If math fails, don't crash the engine, just break the turn
                print(f"ERROR: END_TURN math failed with args {instruction.args}")
    return "break"

