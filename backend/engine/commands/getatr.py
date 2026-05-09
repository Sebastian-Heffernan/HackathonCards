from backend import BuildError
from backend.engine.classes.instruction import Instruction
from backend.engine.engine import GameEngine

# GETATR [VAR] [ARGS]
def execute(instruction : Instruction, engine : GameEngine):
    path = instruction.args[0]
    try:
        value = engine.resolve_path(engine, path)
        print(f"DEBUG: gameState.{path} = {value}")
    except:
        raise BuildError("GETATR Incorrect path")