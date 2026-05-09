from backend.engine.classes.instruction import Instruction
from backend.engine.engine import GameEngine

# (DEBUG) PRINT [ARGS]
def execute(instruction : Instruction, engine : GameEngine):
    path = instruction.args[0]
    value = engine.resolve_path(engine, path)
    print(f"DEBUG: gameState.{path} = {value}")