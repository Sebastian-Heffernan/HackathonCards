from backend.BuildError import BuildError
from backend.engine.classes.instruction import Instruction
from backend.engine.classes.states import *
from backend.engine.engine import GameEngine

# Adds variable to showVars array, shown to every client
# SHOW_VAR [NAME]
def execute(instruction: Instruction, engine: GameEngine):
    if len(instruction.args) != 1:
        raise BuildError("SHOW_VAR [NAME] (Usage)")
    if instruction.args[0] not in engine.gameState.variables:
        raise BuildError("SHOW_VAR Requires valid variable")
    engine.gameState.showVars.append(instruction.args[0])