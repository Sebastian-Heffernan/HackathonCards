from backend.BuildError import BuildError
from backend.engine.classes.instruction import Instruction
from backend.engine.engine import GameEngine

# Sets x = x + y for COMPARE x + y
# COMPARE [x][operator][y]
def execute(instruction : Instruction, engine: GameEngine):
    if len(instruction.args) < 3:
        raise BuildError()
    left = engine.gameState.resolve_variable(instruction.args[0])
    right = engine.gameState.resolve_variable(instruction.args[3])
    operator = instruction.args[1]